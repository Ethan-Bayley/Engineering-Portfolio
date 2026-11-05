[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Inspect", "ApplyPlan", "Render")]
    [string]$Action,

    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [string]$OutputPath,
    [string]$PlanPath,
    [string]$ReportPath,
    [string]$Slides = "",
    [switch]$AllowOverwrite
)

$ErrorActionPreference = "Stop"

function Convert-ToWindowsPath([string]$PathValue) {
    if ($PathValue -match '^/mnt/([a-zA-Z])/(.*)$') {
        $drive = $Matches[1].ToUpper()
        $rest = $Matches[2] -replace '/', '\'
        return "${drive}:\$rest"
    }
    return $PathValue
}

function Get-FullWindowsPath([string]$PathValue, [bool]$MustExist) {
    if ([string]::IsNullOrWhiteSpace($PathValue)) {
        throw "A required path was not provided."
    }
    $windowsPath = Convert-ToWindowsPath $PathValue
    if ($MustExist -and -not (Test-Path -LiteralPath $windowsPath)) {
        throw "File or directory not found: $windowsPath"
    }
    return [System.IO.Path]::GetFullPath($windowsPath)
}

function Release-ComObject($Value) {
    if ($null -ne $Value -and [Runtime.InteropServices.Marshal]::IsComObject($Value)) {
        [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($Value)
    }
}

function Get-TextShapeRecords($Shapes, [string]$Prefix = "") {
    $records = @()
    for ($index = 1; $index -le $Shapes.Count; $index++) {
        $shape = $Shapes.Item($index)
        try {
            $qualifiedName = if ($Prefix) { "$Prefix/$($shape.Name)" } else { $shape.Name }
            if ($shape.Type -eq 6) {
                $records += Get-TextShapeRecords $shape.GroupItems $qualifiedName
            }
            if ($shape.HasTable -eq -1) {
                for ($row = 1; $row -le $shape.Table.Rows.Count; $row++) {
                    for ($column = 1; $column -le $shape.Table.Columns.Count; $column++) {
                        $cellShape = $shape.Table.Cell($row, $column).Shape
                        try {
                            if ($cellShape.HasTextFrame -eq -1 -and $cellShape.TextFrame.HasText -eq -1) {
                                $records += [ordered]@{
                                    name = "$qualifiedName[r${row}c${column}]"
                                    type = "table_cell"
                                    left = [math]::Round([double]$cellShape.Left, 2)
                                    top = [math]::Round([double]$cellShape.Top, 2)
                                    width = [math]::Round([double]$cellShape.Width, 2)
                                    height = [math]::Round([double]$cellShape.Height, 2)
                                    text = [string]$cellShape.TextFrame.TextRange.Text
                                }
                            }
                        }
                        finally { Release-ComObject $cellShape }
                    }
                }
            }
            if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $records += [ordered]@{
                    name = $qualifiedName
                    type = [int]$shape.Type
                    left = [math]::Round([double]$shape.Left, 2)
                    top = [math]::Round([double]$shape.Top, 2)
                    width = [math]::Round([double]$shape.Width, 2)
                    height = [math]::Round([double]$shape.Height, 2)
                    text = [string]$shape.TextFrame.TextRange.Text
                }
            }
        }
        finally {
            Release-ComObject $shape
        }
    }
    return $records
}

function Get-NotesText($Slide) {
    $parts = @()
    $notesPage = $Slide.NotesPage
    try {
        for ($index = 1; $index -le $notesPage.Shapes.Count; $index++) {
            $shape = $notesPage.Shapes.Item($index)
            try {
                if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                    $text = [string]$shape.TextFrame.TextRange.Text
                    if (-not [string]::IsNullOrWhiteSpace($text)) {
                        $parts += $text.Trim()
                    }
                }
            }
            finally {
                Release-ComObject $shape
            }
        }
    }
    finally {
        Release-ComObject $notesPage
    }
    return ($parts -join "`n")
}

function Write-JsonFile($Value, [string]$PathValue) {
    $directory = [System.IO.Path]::GetDirectoryName($PathValue)
    if (-not [string]::IsNullOrWhiteSpace($directory)) {
        [System.IO.Directory]::CreateDirectory($directory) | Out-Null
    }
    $json = $Value | ConvertTo-Json -Depth 12
    [System.IO.File]::WriteAllText($PathValue, $json, (New-Object System.Text.UTF8Encoding($false)))
}

function Get-SlideByReference($Presentation, $Reference, $Aliases) {
    $number = 0
    if ([int]::TryParse([string]$Reference, [ref]$number)) {
        if ($number -lt 1 -or $number -gt $Presentation.Slides.Count) {
            throw "Slide number out of range: $number"
        }
        return $Presentation.Slides.Item($number)
    }
    $alias = [string]$Reference
    if (-not $Aliases.ContainsKey($alias)) {
        throw "Unknown slide alias: $alias"
    }
    $slideId = [int]$Aliases[$alias]
    for ($index = 1; $index -le $Presentation.Slides.Count; $index++) {
        $candidate = $Presentation.Slides.Item($index)
        if ($candidate.SlideID -eq $slideId) {
            return $candidate
        }
        Release-ComObject $candidate
    }
    throw "Slide alias no longer resolves: $alias"
}

function Replace-InTextRange($TextRange, [string]$Find, [string]$Replacement, [bool]$MatchCase) {
    if ([string]::IsNullOrEmpty($Find)) {
        throw "Replacement find text cannot be empty."
    }
    $comparison = if ($MatchCase) { [StringComparison]::Ordinal } else { [StringComparison]::OrdinalIgnoreCase }
    $text = [string]$TextRange.Text
    $positions = New-Object System.Collections.Generic.List[int]
    $offset = 0
    while ($offset -lt $text.Length) {
        $found = $text.IndexOf($Find, $offset, $comparison)
        if ($found -lt 0) { break }
        $positions.Add($found)
        $offset = $found + $Find.Length
    }
    for ($index = $positions.Count - 1; $index -ge 0; $index--) {
        $segment = $TextRange.Characters($positions[$index] + 1, $Find.Length)
        try { $segment.Text = $Replacement } finally { Release-ComObject $segment }
    }
    return $positions.Count
}

function Replace-InShapes($Shapes, [string]$Find, [string]$Replacement, [bool]$MatchCase) {
    $count = 0
    for ($index = 1; $index -le $Shapes.Count; $index++) {
        $shape = $Shapes.Item($index)
        try {
            if ($shape.Type -eq 6) {
                $count += Replace-InShapes $shape.GroupItems $Find $Replacement $MatchCase
            }
            if ($shape.HasTable -eq -1) {
                for ($row = 1; $row -le $shape.Table.Rows.Count; $row++) {
                    for ($column = 1; $column -le $shape.Table.Columns.Count; $column++) {
                        $cellShape = $shape.Table.Cell($row, $column).Shape
                        try {
                            if ($cellShape.HasTextFrame -eq -1 -and $cellShape.TextFrame.HasText -eq -1) {
                                $range = $cellShape.TextFrame.TextRange
                                try { $count += Replace-InTextRange $range $Find $Replacement $MatchCase }
                                finally { Release-ComObject $range }
                            }
                        }
                        finally { Release-ComObject $cellShape }
                    }
                }
            }
            if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $range = $shape.TextFrame.TextRange
                try { $count += Replace-InTextRange $range $Find $Replacement $MatchCase } finally { Release-ComObject $range }
            }
        }
        finally {
            Release-ComObject $shape
        }
    }
    return $count
}

function Find-ShapeByName($Shapes, [string]$TargetName, [string]$Prefix = "") {
    for ($index = 1; $index -le $Shapes.Count; $index++) {
        $shape = $Shapes.Item($index)
        $qualifiedName = if ($Prefix) { "$Prefix/$($shape.Name)" } else { $shape.Name }
        if ($shape.Name -eq $TargetName -or $qualifiedName -eq $TargetName) {
            return $shape
        }
        if ($shape.HasTable -eq -1) {
            for ($row = 1; $row -le $shape.Table.Rows.Count; $row++) {
                for ($column = 1; $column -le $shape.Table.Columns.Count; $column++) {
                    if ("$qualifiedName[r${row}c${column}]" -eq $TargetName) {
                        $cellShape = $shape.Table.Cell($row, $column).Shape
                        Release-ComObject $shape
                        return $cellShape
                    }
                }
            }
        }
        if ($shape.Type -eq 6) {
            $match = Find-ShapeByName $shape.GroupItems $TargetName $qualifiedName
            if ($null -ne $match) {
                Release-ComObject $shape
                return $match
            }
        }
        Release-ComObject $shape
    }
    return $null
}

function Set-SlideNotes($Slide, [string]$Text) {
    $notesPage = $Slide.NotesPage
    try {
        for ($index = 1; $index -le $notesPage.Shapes.Count; $index++) {
            $shape = $notesPage.Shapes.Item($index)
            try {
                if ($shape.Type -eq 14 -and $shape.PlaceholderFormat.Type -eq 2 -and $shape.HasTextFrame -eq -1) {
                    $shape.TextFrame.TextRange.Text = $Text
                    return
                }
            }
            finally {
                Release-ComObject $shape
            }
        }
    }
    finally {
        Release-ComObject $notesPage
    }
    throw "Could not find the speaker-notes body placeholder."
}

function Parse-SlideSelection([string]$Selection, [int]$Maximum) {
    if ([string]::IsNullOrWhiteSpace($Selection)) {
        return 1..$Maximum
    }
    $result = New-Object System.Collections.Generic.SortedSet[int]
    foreach ($part in $Selection.Split(',')) {
        $token = $part.Trim()
        if ($token -match '^(\d+)-(\d+)$') {
            $start = [int]$Matches[1]
            $end = [int]$Matches[2]
            if ($start -gt $end) { throw "Invalid descending slide range: $token" }
            foreach ($number in $start..$end) { [void]$result.Add($number) }
        }
        elseif ($token -match '^\d+$') {
            [void]$result.Add([int]$token)
        }
        else {
            throw "Invalid slide selection token: $token"
        }
    }
    foreach ($number in $result) {
        if ($number -lt 1 -or $number -gt $Maximum) { throw "Slide number out of range: $number" }
    }
    return @($result)
}

$inputFile = Get-FullWindowsPath $InputPath $true
$powerPoint = $null
$presentation = $null

try {
    $powerPoint = New-Object -ComObject PowerPoint.Application

    if ($Action -eq "Inspect") {
        if ([string]::IsNullOrWhiteSpace($ReportPath)) { throw "Inspect requires -ReportPath." }
        $reportFile = Get-FullWindowsPath $ReportPath $false
        $presentation = $powerPoint.Presentations.Open($inputFile, $true, $false, $false)

        $designs = @()
        for ($designIndex = 1; $designIndex -le $presentation.Designs.Count; $designIndex++) {
            $design = $presentation.Designs.Item($designIndex)
            try {
                $layouts = @()
                for ($layoutIndex = 1; $layoutIndex -le $design.SlideMaster.CustomLayouts.Count; $layoutIndex++) {
                    $layout = $design.SlideMaster.CustomLayouts.Item($layoutIndex)
                    try { $layouts += [ordered]@{ index = $layoutIndex; name = [string]$layout.Name } }
                    finally { Release-ComObject $layout }
                }
                $designs += [ordered]@{ index = $designIndex; name = [string]$design.Name; layouts = $layouts }
            }
            finally { Release-ComObject $design }
        }

        $slideRecords = @()
        for ($slideIndex = 1; $slideIndex -le $presentation.Slides.Count; $slideIndex++) {
            $slide = $presentation.Slides.Item($slideIndex)
            try {
                $slideRecords += [ordered]@{
                    number = $slideIndex
                    slide_id = [int]$slide.SlideID
                    name = [string]$slide.Name
                    layout = [string]$slide.CustomLayout.Name
                    hidden = ($slide.SlideShowTransition.Hidden -eq -1)
                    text_shapes = @(Get-TextShapeRecords $slide.Shapes)
                    notes = Get-NotesText $slide
                }
            }
            finally { Release-ComObject $slide }
        }

        $inventory = [ordered]@{
            generated_at = [DateTime]::Now.ToString("o")
            source = $inputFile
            slide_width = [math]::Round([double]$presentation.PageSetup.SlideWidth, 2)
            slide_height = [math]::Round([double]$presentation.PageSetup.SlideHeight, 2)
            slide_count = [int]$presentation.Slides.Count
            designs = $designs
            slides = $slideRecords
        }
        Write-JsonFile $inventory $reportFile
        [ordered]@{ action = "Inspect"; slide_count = $presentation.Slides.Count; report = $reportFile } | ConvertTo-Json
    }
    elseif ($Action -eq "Render") {
        if ([string]::IsNullOrWhiteSpace($OutputPath)) { throw "Render requires -OutputPath as a directory." }
        $renderDirectory = Get-FullWindowsPath $OutputPath $false
        [System.IO.Directory]::CreateDirectory($renderDirectory) | Out-Null
        $presentation = $powerPoint.Presentations.Open($inputFile, $true, $false, $false)
        $selection = Parse-SlideSelection $Slides $presentation.Slides.Count
        $renderWidth = 1530
        $renderHeight = [int][math]::Round($renderWidth * ([double]$presentation.PageSetup.SlideHeight / [double]$presentation.PageSetup.SlideWidth))
        $files = @()
        foreach ($slideIndex in $selection) {
            $slide = $presentation.Slides.Item($slideIndex)
            try {
                $file = Join-Path $renderDirectory ("slide-{0:D3}.png" -f $slideIndex)
                $slide.Export($file, "PNG", $renderWidth, $renderHeight)
                $files += $file
            }
            finally { Release-ComObject $slide }
        }
        [ordered]@{ action = "Render"; rendered = $files.Count; output = $renderDirectory; files = $files } | ConvertTo-Json -Depth 4
    }
    else {
        if ([string]::IsNullOrWhiteSpace($OutputPath)) { throw "ApplyPlan requires -OutputPath." }
        if ([string]::IsNullOrWhiteSpace($PlanPath)) { throw "ApplyPlan requires -PlanPath." }
        $outputFile = Get-FullWindowsPath $OutputPath $false
        $planFile = Get-FullWindowsPath $PlanPath $true
        $sameFile = [string]::Equals($inputFile, $outputFile, [StringComparison]::OrdinalIgnoreCase)
        if ($sameFile -and -not $AllowOverwrite) {
            throw "Refusing to overwrite the input deck. Choose a different -OutputPath or explicitly pass -AllowOverwrite."
        }
        if ((Test-Path -LiteralPath $outputFile) -and -not $AllowOverwrite) {
            throw "Output already exists. Choose a new path or explicitly pass -AllowOverwrite: $outputFile"
        }
        $outputDirectory = [System.IO.Path]::GetDirectoryName($outputFile)
        [System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null
        if (-not $sameFile) { Copy-Item -LiteralPath $inputFile -Destination $outputFile -Force:$AllowOverwrite }

        $plan = Get-Content -LiteralPath $planFile -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($null -eq $plan.operations) { throw "Edit plan must contain an operations array." }
        $presentation = $powerPoint.Presentations.Open($outputFile, $false, $false, $false)
        $aliases = @{}
        $changes = @()

        foreach ($operation in $plan.operations) {
            $op = [string]$operation.op
            if ($op -eq "duplicate_slide") {
                $source = Get-SlideByReference $presentation $operation.source_slide $aliases
                try {
                    $duplicateRange = $source.Duplicate()
                    try { $newSlide = $duplicateRange.Item(1) } finally { Release-ComObject $duplicateRange }
                }
                finally { Release-ComObject $source }
                try {
                    if ($null -ne $operation.after_slide) {
                        $after = Get-SlideByReference $presentation $operation.after_slide $aliases
                        try { $newSlide.MoveTo($after.SlideIndex + 1) } finally { Release-ComObject $after }
                    }
                    if (-not [string]::IsNullOrWhiteSpace([string]$operation.id)) {
                        if ($aliases.ContainsKey([string]$operation.id)) { throw "Duplicate slide alias: $($operation.id)" }
                        $aliases[[string]$operation.id] = [int]$newSlide.SlideID
                    }
                    foreach ($replacement in @($operation.replacements)) {
                        $matchCase = ($replacement.match_case -eq $true)
                        $replaced = Replace-InShapes $newSlide.Shapes ([string]$replacement.find) ([string]$replacement.replace) $matchCase
                        if ($replaced -eq 0) { throw "Text not found on duplicated slide: $($replacement.find)" }
                    }
                    $changes += [ordered]@{ op = $op; slide = [int]$newSlide.SlideIndex; id = [string]$operation.id }
                }
                finally { Release-ComObject $newSlide }
            }
            elseif ($op -eq "replace_text") {
                $slide = Get-SlideByReference $presentation $operation.slide $aliases
                try {
                    $replaced = Replace-InShapes $slide.Shapes ([string]$operation.find) ([string]$operation.replace) ($operation.match_case -eq $true)
                    if ($replaced -eq 0) { throw "Text not found on slide $($slide.SlideIndex): $($operation.find)" }
                    $changes += [ordered]@{ op = $op; slide = [int]$slide.SlideIndex; replacements = $replaced }
                }
                finally { Release-ComObject $slide }
            }
            elseif ($op -eq "set_shape_text") {
                $slide = Get-SlideByReference $presentation $operation.slide $aliases
                try {
                    $shape = Find-ShapeByName $slide.Shapes ([string]$operation.shape)
                    if ($null -eq $shape) { throw "Shape not found on slide $($slide.SlideIndex): $($operation.shape)" }
                    try { $shape.TextFrame.TextRange.Text = [string]$operation.text } finally { Release-ComObject $shape }
                    $changes += [ordered]@{ op = $op; slide = [int]$slide.SlideIndex; shape = [string]$operation.shape }
                }
                finally { Release-ComObject $slide }
            }
            elseif ($op -eq "add_image") {
                $slide = Get-SlideByReference $presentation $operation.slide $aliases
                $imagePath = Get-FullWindowsPath ([string]$operation.path) $true
                try {
                    $picture = $slide.Shapes.AddPicture($imagePath, 0, -1, [double]$operation.left, [double]$operation.top, [double]$operation.width, [double]$operation.height)
                    try {
                        if (-not [string]::IsNullOrWhiteSpace([string]$operation.alt_text)) {
                            $picture.AlternativeText = [string]$operation.alt_text
                        }
                    }
                    finally { Release-ComObject $picture }
                    $changes += [ordered]@{ op = $op; slide = [int]$slide.SlideIndex; path = $imagePath }
                }
                finally { Release-ComObject $slide }
            }
            elseif ($op -eq "set_notes") {
                $slide = Get-SlideByReference $presentation $operation.slide $aliases
                try {
                    Set-SlideNotes $slide ([string]$operation.text)
                    $changes += [ordered]@{ op = $op; slide = [int]$slide.SlideIndex }
                }
                finally { Release-ComObject $slide }
            }
            else {
                throw "Unsupported edit operation: $op"
            }
        }

        $presentation.Save()
        [ordered]@{ action = "ApplyPlan"; output = $outputFile; changes = $changes } | ConvertTo-Json -Depth 6
    }
}
finally {
    if ($null -ne $presentation) {
        try { $presentation.Close() } catch { }
        Release-ComObject $presentation
    }
    if ($null -ne $powerPoint) {
        try { $powerPoint.Quit() } catch { }
        Release-ComObject $powerPoint
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
