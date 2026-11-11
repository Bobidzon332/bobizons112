# Clean render progress panel: reads render\status.json written by the render scripts.
# Shows job, progress bar, current item, time per frame, finish time and the last finished image. Closing it does NOT stop the render.
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$root = if ($env:FILM_ROOT) { $env:FILM_ROOT } else { "$env:USERPROFILE\blender-film" }
$status = "$root\render\status.json"
$bg = [Drawing.Color]::FromArgb(18, 18, 20); $fg = [Drawing.Color]::FromArgb(235, 235, 235); $dim = [Drawing.Color]::FromArgb(140, 140, 150)
$accent = [Drawing.Color]::FromArgb(0, 214, 230)

$f = New-Object Windows.Forms.Form
$f.Text = "Drone night - render"; $f.Size = New-Object Drawing.Size(560, 520); $f.BackColor = $bg; $f.ForeColor = $fg
$f.FormBorderStyle = "FixedSingle"; $f.MaximizeBox = $false; $f.StartPosition = "Manual"; $f.Location = New-Object Drawing.Point(2860, 40)
$f.TopMost = $true

function L($text, $size, $y, $color, $bold) {
  $l = New-Object Windows.Forms.Label; $l.Text = $text; $l.ForeColor = $color; $l.AutoSize = $false
  $l.Size = New-Object Drawing.Size(520, [int]($size * 2.1)); $l.Location = New-Object Drawing.Point(18, $y)
  $style = if ($bold) { [Drawing.FontStyle]::Bold } else { [Drawing.FontStyle]::Regular }
  $l.Font = New-Object Drawing.Font("Segoe UI", $size, $style); $f.Controls.Add($l); return $l
}
$title = L "DRONE NIGHT  -  FINAL RENDER" 13 14 $fg $true
$job = L "" 10 46 $dim $false
$pct = L "0%" 30 74 $accent $true
$bar = New-Object Windows.Forms.Panel; $bar.Location = New-Object Drawing.Point(20, 140); $bar.Size = New-Object Drawing.Size(510, 10); $bar.BackColor = [Drawing.Color]::FromArgb(45, 45, 52); $f.Controls.Add($bar)
$fill = New-Object Windows.Forms.Panel; $fill.Location = New-Object Drawing.Point(0, 0); $fill.Size = New-Object Drawing.Size(0, 10); $fill.BackColor = $accent; $bar.Controls.Add($fill)
$cur = L "" 11 160 $fg $false
$eta = L "" 11 188 $fg $false
$pic = New-Object Windows.Forms.PictureBox; $pic.Location = New-Object Drawing.Point(20, 222); $pic.Size = New-Object Drawing.Size(510, 257)
$pic.SizeMode = "Zoom"; $pic.BackColor = [Drawing.Color]::Black; $f.Controls.Add($pic)
$note = L "You can use the PC.  Closing this window does not stop the render." 8 484 $dim $false
$f.Height = 545
$lastShown = ""

$timer = New-Object Windows.Forms.Timer; $timer.Interval = 2000
$timer.Add_Tick({
  try {
    $s = Get-Content $status -Raw | ConvertFrom-Json
    if ($s.title) { $title.Text = "$($s.title)" }
    $job.Text = "$($s.job)"
    $p = if ($s.total -gt 0) { [math]::Round(100 * $s.done / $s.total) } else { 0 }
    $pct.Text = "$p%    $($s.done) / $($s.total)"
    $fill.Width = [int](510 * $p / 100)
    $cur.Text = if ($s.done -ge $s.total) { "Finished" } else { "Now: $($s.current)" }
    if ($s.avg) {
      $left = ($s.total - $s.done) * $s.avg
      $finish = (Get-Date).AddSeconds($left).ToString("HH:mm")
      $eta.Text = ("{0:N0} s per image    about {1:N0} min left    done ~{2}" -f $s.avg, ($left / 60), $finish)
    } else { $eta.Text = "Measuring speed..." }
    if ($s.done -ge $s.total) { $eta.Text = "All done"; $fill.BackColor = [Drawing.Color]::FromArgb(70, 200, 110) }
    if ($s.last -and ($s.last -ne $lastShown) -and (Test-Path $s.last)) {
      $bytes = [IO.File]::ReadAllBytes($s.last); $ms = New-Object IO.MemoryStream(, $bytes)
      $old = $pic.Image; $pic.Image = [Drawing.Image]::FromStream($ms); if ($old) { $old.Dispose() }
      $script:lastShown = $s.last
    }
  } catch { }
})
$timer.Start()
[void]$f.ShowDialog()
