# Holds "system required" until the final film exists (max 3 h). No settings are changed; ends by itself.
Add-Type -Name P -Namespace W -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint f);'
$final = "$env:USERPROFILE\blender-car-film\video\last_drive_home_FINAL.mp4"
$end = (Get-Date).AddHours(3)
while (-not (Test-Path $final) -and (Get-Date) -lt $end) { [W.P]::SetThreadExecutionState(0x80000001) | Out-Null; Start-Sleep 30 }
[W.P]::SetThreadExecutionState(0x80000000) | Out-Null
