# Keeps the monitor OFF whenever nobody has touched mouse/keyboard for 15 s.
# Notifications can't keep it on: it is switched off again within ~3 s.
# Runs up to 10 hours. To stop early: create the file render\stop_guard
Add-Type -TypeDefinition @"
using System; using System.Runtime.InteropServices;
public class G {
  [StructLayout(LayoutKind.Sequential)] public struct LII { public uint cbSize; public uint dwTime; }
  [DllImport("user32.dll")] public static extern bool GetLastInputInfo(ref LII p);
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
  public static uint IdleMs() { LII l = new LII(); l.cbSize = (uint)Marshal.SizeOf(l); GetLastInputInfo(ref l); return (uint)Environment.TickCount - l.dwTime; }
  public static void Off() { PostMessage((IntPtr)0xffff, 0x0112, (IntPtr)0xF170, (IntPtr)2); }
}
"@
$root = Join-Path $env:USERPROFILE "blender-forest\render"
$log = Join-Path $root "screen_guard.log"
$stop = Join-Path $root "stop_guard"
Remove-Item $stop -ErrorAction SilentlyContinue
"guard v2 started $(Get-Date)" | Out-File $log
$end = (Get-Date).AddHours(10)
while ((Get-Date) -lt $end -and -not (Test-Path $stop)) {
    if ([G]::IdleMs() -gt 15000) { [G]::Off() }   # PostMessage never blocks
    Start-Sleep -Seconds 3
}
"guard stopped $(Get-Date)" | Out-File $log -Append
