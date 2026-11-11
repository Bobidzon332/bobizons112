# Live render progress window. Closing this window does NOT stop the render.
$root = "$env:USERPROFILE\blender-car-film"
$shots = @(@("Shot 1  wide",1,91),@("Shot 2  headlight",92,151),@("Shot 3  wheel",152,211),@("Shot 4  driving",212,331),@("Shot 5  inside",332,436),@("Shot 6  house",437,600))
$Host.UI.RawUI.WindowTitle = "The Last Drive Home - render progress"
$t0 = Get-Date; $n0 = $null
while ($true) {
  $done = @(Get-ChildItem "$root\frames\f_*.png" | ?{ $_.Length -gt 0 } | %{ [int]($_.BaseName -replace 'f_','') })
  if ($n0 -eq $null) { $n0 = $done.Count }
  Clear-Host
  Write-Host "  THE LAST DRIVE HOME  -  rendering 600 frames (2560x1072, 30 fps)`n" -ForegroundColor Yellow
  foreach ($s in $shots) {
    $c = @($done | ?{ $_ -ge $s[1] -and $_ -le $s[2] }).Count; $tot = $s[2]-$s[1]+1
    $bar = ('#' * [int](30*$c/$tot)).PadRight(30,'.')
    $col = if ($c -eq $tot) {'Green'} elseif ($c -gt 0) {'Cyan'} else {'DarkGray'}
    $state = if ($c -eq $tot) {'done'} elseif ($c -gt 0) {'RENDERING'} else {'waiting'}
    Write-Host ("  {0,-18} [{1}] {2,3}/{3,-3} {4}" -f $s[0],$bar,$c,$tot,$state) -ForegroundColor $col
  }
  $left = 600 - $done.Count; $el = ((Get-Date)-$t0).TotalSeconds; $rate = if ($done.Count -gt $n0) { $el/($done.Count-$n0) } else { 7 }
  Write-Host ("`n  Total {0}/600   about {1:N0} min left" -f $done.Count, ($left*$rate/60))
  if (Test-Path "$root\video\last_drive_home_FINAL.mp4") { Write-Host "`n  FINISHED: video\last_drive_home_FINAL.mp4" -ForegroundColor Green }
  Write-Host "`n  You can use the PC. Closing this window does not stop the render." -ForegroundColor DarkGray
  Start-Sleep 5
}
