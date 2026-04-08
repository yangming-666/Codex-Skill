$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$configPath = Join-Path $scriptDir "lark-mcp.config.json"
$pidPath = Join-Path $scriptDir "lark-mcp.pid"

function Get-LarkProcesses {
    $procs = Get-CimInstance Win32_Process |
        Where-Object {
            $_.Name -eq "node.exe" -and
            $_.CommandLine -and
            $_.CommandLine -like "*lark-mcp*"
        } |
        Sort-Object CreationDate

    return @($procs)
}

if (-not (Test-Path $configPath)) {
    throw "Missing config file: $configPath"
}

$config = Get-Content -Path $configPath -Raw | ConvertFrom-Json
$proc = $null
$portOwnerPid = $null
if (Test-Path $pidPath) {
    $rawPid = Get-Content -Path $pidPath -Raw -ErrorAction SilentlyContinue
    if ($null -ne $rawPid) {
        $rawPid = $rawPid.Trim()
    }
    if ($rawPid) {
        $proc = Get-Process -Id ([int]$rawPid) -ErrorAction SilentlyContinue
    }
}

if (-not $proc) {
    $allRunning = Get-LarkProcesses
    if ($allRunning.Count -gt 0) {
        $proc = $allRunning[-1]
    }
}

$portOwner = Get-NetTCPConnection -LocalAddress $config.host -LocalPort ([int]$config.port) -State Listen -ErrorAction SilentlyContinue |
    Select-Object -First 1
if ($portOwner -and $portOwner.OwningProcess) {
    $portOwnerPid = [int]$portOwner.OwningProcess
    if (-not $proc) {
        $proc = Get-Process -Id $portOwnerPid -ErrorAction SilentlyContinue
    }
}

$alive = $false
try {
    $response = Invoke-WebRequest -Uri ("http://{0}:{1}/mcp" -f $config.host, $config.port) -Method Get -UseBasicParsing -TimeoutSec 3
    $alive = $response.StatusCode -eq 405
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $alive = $statusCode -eq 405
}

[pscustomobject]@{
    running = [bool]$proc
    pid = if ($proc) { if ($null -ne $proc.Id) { $proc.Id } else { $proc.ProcessId } } else { $null }
    process_count = (Get-LarkProcesses).Count
    port_owner_pid = $portOwnerPid
    endpoint_ready = $alive
    url = "http://$($config.host):$($config.port)/mcp"
    tools = [string]$config.tools
    oauth = [bool]$config.oauth
} | ConvertTo-Json -Depth 4
