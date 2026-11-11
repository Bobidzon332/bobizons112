# Keeps the PC awake (no settings changed) while the final render runs, then makes the MP4.
Add-Type -TypeDefinition @"
using System; using System.Runtime.InteropServices;
public class Awake { [DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint f); }
"@
$ES_CONTINUOUS = [uint32]2147483648; $ES_SYSTEM_REQUIRED = [uint32]1
$root = Join-Path $env:USERPROFILE "blender-forest"
$log = Join-Path $root "render\stay_awake.log"
"started $(Get-Date)" | Out-File $log
[Awake]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED) | Out-Null
while (Get-CimInstance Win32_Process -Filter "Name='blender.exe'" | Where-Object { $_.CommandLine -like '*render_final.py*' }) {
    [Awake]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED) | Out-Null
    Start-Sleep 60
}
$n = (Get-ChildItem "$root\render\final_2k" -Filter "f*.png" | Where-Object Length -gt 0).Count
"render ended $(Get-Date), frames $n" | Out-File $log -Append
if ($n -ge 390) {
    & ffmpeg -loglevel error -y -framerate 30 -i "$root\render\final_2k\f%04d.png" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p "$root\render\forest_car_19-32s_2K.mp4"
    "mp4 done $(Get-Date)" | Out-File $log -Append
}
[Awake]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
