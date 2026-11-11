# Live progress for the final render: frames done, speed, time left.
$dir = Join-Path $env:USERPROFILE "blender-forest\render\final_2k"
$total = 390
$host.UI.RawUI.WindowTitle = "Forest render - progress"
$start = Get-Date
$startDone = $null
while ($true) {
    $files = @(Get-ChildItem $dir -Filter "f*.png" -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 0 } | Sort-Object LastWriteTime)
    $done = $files.Count
    if ($null -eq $startDone) { $startDone = $done }
    Clear-Host
    Write-Host ""
    Write-Host "  FOREST CLIP - FINAL 2K RENDER (2560x1440, 128 samples + OIDN)" -ForegroundColor Cyan
    Write-Host "  ---------------------------------------------------------------"
    $pct = [math]::Round(100 * $done / $total, 1)
    $bar = ("#" * [int]($pct / 2.5)).PadRight(40, ".")
    Write-Host ("  [{0}] {1}%" -f $bar, $pct)
    Write-Host ("  Frames done : {0} / {1}" -f $done, $total)
    if ($files.Count -ge 3) {
        $recent = $files | Select-Object -Last ([math]::Min(20, $files.Count))
        $span = ($recent[-1].LastWriteTime - $recent[0].LastWriteTime).TotalSeconds
        $per = $span / [math]::Max(1, $recent.Count - 1)
        $left = ($total - $done) * $per
        $eta = (Get-Date).AddSeconds($left)
        Write-Host ("  Speed       : {0:N1} s per frame" -f $per)
        Write-Host ("  Time left   : {0}h {1:D2}m" -f [int][math]::Floor($left / 3600), [int][math]::Floor(($left % 3600) / 60))
        Write-Host ("  Finishes at : {0:HH:mm}" -f $eta)
        Write-Host ("  Last frame  : {0}  ({1:HH:mm:ss})" -f $files[-1].Name, $files[-1].LastWriteTime)
    } else {
        Write-Host "  Speed       : measuring... (first frame loads the forest, ~1 min)"
    }
    $gpu = (nvidia-smi --query-gpu=utilization.gpu,memory.used,temperature.gpu --format=csv,noheader 2>$null)
    if ($gpu) { Write-Host ("  GPU         : {0}  (util, VRAM, temp)" -f $gpu) }
    $running = Get-Process blender -ErrorAction SilentlyContinue
    Write-Host ("  Blender     : {0}" -f $(if ($running) { "rendering" } else { "not running" }))
    if ($done -ge $total) { Write-Host "`n  DONE - all frames rendered." -ForegroundColor Green }
    elseif (-not $running) { Write-Host "`n  Stopped (power cut?). Restart the render; it resumes from the last frame." -ForegroundColor Yellow }
    Write-Host "`n  (this window only watches; closing it does not stop the render)"
    Start-Sleep 10
}
