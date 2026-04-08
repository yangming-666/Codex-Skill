$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidPath = Join-Path $scriptDir "lark-mcp.pid"

function Get-LarkProcesses {
    $procs = Get-CimInstance Win32_Process |
        Where-Object {
            $_.Name -eq "node.exe" -and
            $_.CommandLine -and
            $_.CommandLine -like "*lark-mcp*"
        }

    return @($procs)
}

$killed = @()
$allRunning = Get-LarkProcesses
foreach ($proc in $allRunning) {
    Stop-Process -Id ([int]$proc.ProcessId) -Force -ErrorAction SilentlyContinue
    $killed += [int]$proc.ProcessId
}

Remove-Item -LiteralPath $pidPath -Force -ErrorAction SilentlyContinue

if ($killed.Count -eq 0) {
    Write-Output "lark-mcp is not running"
    exit 0
}

Write-Output ("lark-mcp stopped, pids={0}" -f (($killed | Sort-Object) -join ","))
