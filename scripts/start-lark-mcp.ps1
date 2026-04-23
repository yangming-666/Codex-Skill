param(
    [switch]$ForceRestart
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$configPath = Join-Path $scriptDir "lark-mcp.config.json"
$pidPath = Join-Path $scriptDir "lark-mcp.pid"
$logsDir = Join-Path $scriptDir "logs"
$stdoutPath = Join-Path $logsDir "lark-mcp.stdout.log"
$stderrPath = Join-Path $logsDir "lark-mcp.stderr.log"
$packageRoot = "C:\Users\ym199\.codex\vendor\lark-mcp"
$cliPath = Join-Path $packageRoot "node_modules\@larksuiteoapi\lark-mcp\dist\cli.js"

function Invoke-LarkLocalRequest {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Uri,

        [Parameter(Mandatory = $true)]
        [string]$Method,

        [int]$TimeoutSec = 3
    )

    $handler = [System.Net.Http.HttpClientHandler]::new()
    $handler.UseProxy = $false
    $client = [System.Net.Http.HttpClient]::new($handler)
    $client.Timeout = [TimeSpan]::FromSeconds($TimeoutSec)

    try {
        $request = [System.Net.Http.HttpRequestMessage]::new(
            [System.Net.Http.HttpMethod]::new($Method),
            $Uri
        )
        return $client.SendAsync($request).GetAwaiter().GetResult()
    } finally {
        $client.Dispose()
        $handler.Dispose()
    }
}

function Get-StoredLocalAccessToken {
    param(
        [string]$AppId
    )

    if (-not $AppId) {
        return $null
    }

    $script = @"
const { authStore } = require('C:/Users/ym199/.codex/vendor/lark-mcp/node_modules/@larksuiteoapi/lark-mcp/dist/auth/store.js');
authStore.getLocalAccessToken(process.argv[1])
  .then(token => {
    if (token) {
      process.stdout.write(token);
    }
    process.exit(0);
  })
  .catch(err => {
    process.stderr.write(String(err || 'failed_to_read_local_access_token'));
    process.exit(1);
  });
"@

    try {
        $token = & $nodePath -e $script $AppId
        if ($LASTEXITCODE -ne 0) {
            return $null
        }
        $token = [string]$token
        if ($token) {
            $token = $token.Trim()
        }
        if ($token) {
            return $token
        }
    } catch {
        return $null
    }

    return $null
}

function Get-ConfiguredProcess {
    if (-not (Test-Path $pidPath)) {
        return $null
    }

    $rawPid = Get-Content -Path $pidPath -Raw -ErrorAction SilentlyContinue
    if ($null -eq $rawPid) {
        return $null
    }
    $rawPid = $rawPid.Trim()
    if (-not $rawPid) {
        return $null
    }

    $proc = Get-Process -Id ([int]$rawPid) -ErrorAction SilentlyContinue
    if (-not $proc) {
        return $null
    }

    return $proc
}

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

function Get-ProcessIdValue {
    param(
        [Parameter(Mandatory = $true)]
        $ProcessObject
    )

    if ($null -ne $ProcessObject.Id) {
        return [int]$ProcessObject.Id
    }

    if ($null -ne $ProcessObject.ProcessId) {
        return [int]$ProcessObject.ProcessId
    }

    return $null
}

function Stop-LarkProcesses {
    param(
        [Parameter(Mandatory = $true)]
        [array]$Processes
    )

    foreach ($proc in $Processes) {
        Stop-Process -Id ([int]$proc.ProcessId) -Force -ErrorAction SilentlyContinue
    }
}

function Test-LarkEndpoint {
    param(
        [string]$BindHost,
        [int]$Port
    )

    try {
        $response = Invoke-LarkLocalRequest -Uri ("http://{0}:{1}/mcp" -f $BindHost, $Port) -Method "GET" -TimeoutSec 3
        return [int]$response.StatusCode -eq 405
    } catch {
        $response = $_.Exception.Response
        if ($response -and $response.StatusCode) {
            return [int]$response.StatusCode -eq 405
        }
        return $false
    }
}

function Get-LarkPortOwner {
    param(
        [string]$BindHost,
        [int]$Port
    )

    $conn = Get-NetTCPConnection -LocalAddress $BindHost -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -First 1

    if ($conn -and $conn.OwningProcess) {
        return [int]$conn.OwningProcess
    }

    return $null
}

if (-not (Test-Path $configPath)) {
    throw "Missing config file: $configPath"
}

if (-not (Test-Path $cliPath)) {
    throw "Missing lark-mcp CLI: $cliPath"
}

$config = Get-Content -Path $configPath -Raw | ConvertFrom-Json
New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

$running = Get-ConfiguredProcess
if (-not $running) {
    $allRunning = Get-LarkProcesses
    if ($allRunning.Count -gt 0) {
        $running = $allRunning[-1]
        Set-Content -Path $pidPath -Value (Get-ProcessIdValue -ProcessObject $running)
    }
}

if ($running -and -not $ForceRestart) {
    if (Test-LarkEndpoint -BindHost $config.host -Port ([int]$config.port)) {
        $allRunning = Get-LarkProcesses
        if ($allRunning.Count -gt 1) {
            $runningPid = Get-ProcessIdValue -ProcessObject $running
            $extra = @($allRunning | Where-Object { (Get-ProcessIdValue -ProcessObject $_) -ne $runningPid })
            if ($extra.Count -gt 0) {
                Stop-LarkProcesses -Processes $extra
            }
        }
        $runningPid = Get-ProcessIdValue -ProcessObject $running
        Set-Content -Path $pidPath -Value $runningPid
        Write-Output ("lark-mcp already running, pid={0}" -f $runningPid)
        exit 0
    }
}

if ($running) {
    Stop-Process -Id (Get-ProcessIdValue -ProcessObject $running) -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 500
}

$stale = Get-LarkProcesses
if ($stale.Count -gt 0) {
    Stop-LarkProcesses -Processes $stale
    Start-Sleep -Milliseconds 500
}

$nodePath = (Get-Command node).Source
$args = @(
    $cliPath,
    "mcp",
    "-a", [string]$config.appId,
    "-s", [string]$config.appSecret,
    "-m", "streamable",
    "--host", [string]$config.host,
    "-p", [string]$config.port,
    "-l", [string]$config.language,
    "-t", [string]$config.tools
)

if ($config.tokenMode) {
    $args += "--token-mode"
    $args += [string]$config.tokenMode
}

if ($config.useStoredLocalAccessToken -eq $true) {
    $localAccessToken = Get-StoredLocalAccessToken -AppId ([string]$config.appId)
    if (-not $localAccessToken) {
        throw "No stored local access token found. Run lark-mcp login first."
    }
    $args += "--user-access-token"
    $args += $localAccessToken
}

if ($config.oauth -eq $true) {
    $args += "--oauth"
}

$proc = Start-Process -FilePath $nodePath -ArgumentList $args -WorkingDirectory $packageRoot -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath -PassThru -WindowStyle Hidden
Set-Content -Path $pidPath -Value $proc.Id

for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 500
    if ($proc.HasExited) {
        throw ("lark-mcp exited early, code={0}. stderr: {1}" -f $proc.ExitCode, (Get-Content -Path $stderrPath -Raw -ErrorAction SilentlyContinue))
    }
    if (Test-LarkEndpoint -BindHost $config.host -Port ([int]$config.port)) {
        $ownerPid = Get-LarkPortOwner -BindHost $config.host -Port ([int]$config.port)
        if ($ownerPid) {
            Set-Content -Path $pidPath -Value $ownerPid
        }
        Write-Output ("lark-mcp started, pid={0}, url=http://{1}:{2}/mcp" -f ($(if ($ownerPid) { $ownerPid } else { $proc.Id })), $config.host, $config.port)
        exit 0
    }
}

throw "lark-mcp did not become ready in time"
