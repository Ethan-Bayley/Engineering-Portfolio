# Render slides to PNG with PowerPoint and report layout problems (off-slide shapes, text overflowing its box,
# anything past a design-system box, tables that grow into what is placed below them).
# Usage: powershell -File general/tools/render_check.ps1 -Deck <pptx> -OutDir project/outputs/renders/<name> [-Only 1,3] [-Width 2000]
# Writes sNNN.png and report.txt in OutDir. Read-only on the deck. An empty report is not proof the slide looks right: look at the PNGs.
param([Parameter(Mandatory)][string]$Deck, [Parameter(Mandatory)][string]$OutDir, [string]$Only = "", [int]$Width = 2000)
$Deck = (Resolve-Path -LiteralPath $Deck).Path
New-Item -ItemType Directory -Force $OutDir | Out-Null
$OutDir = (Resolve-Path -LiteralPath $OutDir).Path
Get-ChildItem $OutDir -Filter s*.png -ErrorAction SilentlyContinue | Remove-Item
$pp = New-Object -ComObject PowerPoint.Application
$p = $pp.Presentations.Open($Deck, $true, $false, $false)
try {
  $W = $p.PageSetup.SlideWidth; $H = $p.PageSetup.SlideHeight
  $Height = [int]($Width * $H / $W)
  $sel = @(); if ($Only -ne "") { $sel = $Only.Split(',') | ForEach-Object { [int]$_ } }
  $report = @()
  foreach ($sl in $p.Slides) {
    $i = $sl.SlideIndex
    if ($sel.Count -gt 0 -and -not ($sel -contains $i)) { continue }
    $sl.Export((Join-Path $OutDir ("s{0:D3}.png" -f $i)), "PNG", $Width, $Height)
    # design-system boxes: the white panel ("Box NN panel") is the area everything in the box must stay inside
    $panels = @($sl.Shapes | Where-Object { $_.Name -match '^Box \d+ panel$' })
    $tables = @()
    foreach ($sh in $sl.Shapes) {
      if ($sh.Left -lt -1 -or $sh.Top -lt -1 -or ($sh.Left + $sh.Width) -gt ($W + 1) -or ($sh.Top + $sh.Height) -gt ($H + 1)) { $report += "$i OFFSLIDE $($sh.Name)" }
      $bottom = $sh.Top + $sh.Height
      if ($sh.HasTable) {
        # PowerPoint grows a row to fit its text when it draws, but COM still reports the set height: measure each row's text
        $need = 0
        foreach ($row in $sh.Table.Rows) {
          $rh = $row.Height
          foreach ($cell in $row.Cells) {
            $tf = $cell.Shape.TextFrame2
            if ($tf.HasText) { $rh = [Math]::Max($rh, $tf.TextRange.BoundHeight + $tf.MarginTop + $tf.MarginBottom) }
          }
          $need += $rh
        }
        $bottom = [Math]::Max($bottom, $sh.Top + $need)
        $tables += ,@($sh, [Math]::Max($sh.Top + $sh.Height, $sh.Top + $need))
        if ($need -gt $sh.Height + 2) { $report += "$i TABLE-GROWS '$($sh.Name)' rows need $([int]$need)pt, frame $([int]$sh.Height)pt" }
      }
      if ($sh.HasTextFrame -and $sh.TextFrame2.HasText) {
        $tr = $sh.TextFrame2.TextRange
        if ($tr.BoundHeight -gt $sh.Height + 4) { $report += "$i OVERFLOW-H $($sh.Name) text=$([int]$tr.BoundHeight)pt box=$([int]$sh.Height)pt '$($tr.Text.Substring(0,[Math]::Min(40,$tr.Text.Length)))'" }
        if ($tr.Font.Size -gt 0 -and $tr.Font.Size -lt 12) { $report += "$i SMALL-TEXT $($sh.Name) $($tr.Font.Size)pt" }
        $bottom = [Math]::Max($bottom, $sh.Top + $tr.BoundTop - $sh.Top + $tr.BoundHeight)
      }
      # PAST-BOX: anything (a table whose rows grew, a picture, text) that starts inside a box but ends in its padding or below
      if ($sh.Name -notmatch '^Box \d+ (panel|back)$') {
        $cx = $sh.Left + $sh.Width / 2
        foreach ($pn in $panels) {
          if ($cx -gt $pn.Left -and $cx -lt ($pn.Left + $pn.Width) -and $sh.Top -ge $pn.Top - 1 -and $sh.Top -lt ($pn.Top + $pn.Height)) {
            $over = $bottom - ($pn.Top + $pn.Height - 5)     # content must end at least 5 pt inside the white panel
            if ($over -gt 0.5) {
              $kind = if ($sh.HasTable) { "table" } elseif ($sh.Type -eq 13) { "picture" } else { "shape" }
              $report += "$i PAST-BOX $kind '$($sh.Name)' in '$($pn.Name)' by $([int]$over)pt"
            }
          }
        }
      }
    }
    # OVERLAP: a table that grew into a text box or picture placed below it (same column)
    foreach ($t in $tables) {
      $tb = $t[0]; $grown = $t[1]
      foreach ($o in $sl.Shapes) {
        if ($o.Name -eq $tb.Name -or $o.Name -match '^Box \d+ ' -or $o.HasTable) { continue }
        $xo = [Math]::Min($o.Left + $o.Width, $tb.Left + $tb.Width) - [Math]::Max($o.Left, $tb.Left)
        # nothing may start inside a table's drawn area (COM reports a table's height after its rows have grown)
        if ($xo -gt 5 -and $o.Top -gt ($tb.Top + 2) -and $o.Top -lt ($grown - 1)) {
          $report += "$i OVERLAP table '$($tb.Name)' runs $([int]($grown - $o.Top))pt into '$($o.Name)'"
        }
      }
    }
  }
} finally { $p.Close(); if ($pp.Presentations.Count -eq 0) { $pp.Quit() } }   # never quit a PowerPoint the user has open
$report | Out-File -Encoding utf8 (Join-Path $OutDir "report.txt")
if ($report.Count -eq 0) { "no layout flags" } else { $report }
