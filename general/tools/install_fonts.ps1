# Install the static fonts for this Windows user (no admin needed). Run once per computer:
#   powershell -NoProfile -ExecutionPolicy Bypass -File general/tools/install_fonts.ps1
# export_pdf.py renames a deck's font to "Inter Static" so PowerPoint can embed it in the PDF; that needs these two
# files. A project's own static fonts in project/design/fonts/ (any depth) are installed too.
$src = Join-Path $PSScriptRoot "..\design\fonts\InterStatic"
$dst = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Fonts"
$key = "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts"
New-Item -ItemType Directory -Force $dst | Out-Null

function Install-Font($file, $regName) {
  $target = Join-Path $dst $file.Name
  if ((Test-Path $target) -and ((Get-Item $target).Length -eq $file.Length)) { "already installed " + $file.Name; return }
  Copy-Item $file.FullName $target -Force
  New-ItemProperty -Path $key -Name $regName -Value $target -PropertyType String -Force | Out-Null
  "installed " + $file.Name
}

Install-Font (Get-Item (Join-Path $src "InterStatic-Regular.ttf")) "Inter Static Regular (TrueType)"
Install-Font (Get-Item (Join-Path $src "InterStatic-Bold.ttf")) "Inter Static Bold (TrueType)"
$proj = Join-Path $PSScriptRoot "..\..\project\design\fonts"
if (Test-Path $proj) {
  foreach ($f in Get-ChildItem $proj -Recurse -Filter *.ttf) { Install-Font $f (($f.BaseName -replace "-", " ") + " (TrueType)") }
}
"Done. Restart PowerPoint if it is open (export_pdf.py also loads the fonts into the session each run)."
