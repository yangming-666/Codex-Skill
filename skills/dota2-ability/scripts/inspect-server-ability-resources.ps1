[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Query,

    [string]$DllPath,

    [ValidateRange(1024, 1048576)]
    [int]$Radius = 16384,

    [ValidateRange(1, 64)]
    [int]$MaxHits = 8,

    [switch]$AllHits
)

$ErrorActionPreference = "Stop"

function Add-ServerDllCandidate {
    param(
        [System.Collections.Generic.List[string]]$Candidates,
        [string]$Path
    )

    if (-not [string]::IsNullOrWhiteSpace($Path)) {
        $Candidates.Add([System.IO.Path]::GetFullPath($Path))
    }
}

function Add-ContentRootCandidate {
    param(
        [System.Collections.Generic.List[string]]$Candidates,
        [string]$ContentRoot
    )

    if ([string]::IsNullOrWhiteSpace($ContentRoot)) {
        return
    }

    $resolved = [System.IO.Path]::GetFullPath($ContentRoot)
    $contentDir = Split-Path -Parent $resolved
    $installRoot = Split-Path -Parent $contentDir
    Add-ServerDllCandidate $Candidates (
        Join-Path $installRoot "game\dota\bin\win64\server.dll"
    )
}

$candidates = [System.Collections.Generic.List[string]]::new()
if ($DllPath) {
    Add-ServerDllCandidate $candidates $DllPath
} else {
    Add-ServerDllCandidate $candidates $env:DOTA2_SERVER_DLL
    if ($env:DOTA2_GAME_ROOT) {
        Add-ServerDllCandidate $candidates (
            Join-Path $env:DOTA2_GAME_ROOT "bin\win64\server.dll"
        )
    }
    Add-ContentRootCandidate $candidates $env:DOTA2_CONTENT_ROOT
    Add-ContentRootCandidate $candidates $env:DOTA2_VANILLA_CONTENT_ROOT

    Get-PSDrive -PSProvider FileSystem | ForEach-Object {
        Add-ServerDllCandidate $candidates (
            Join-Path $_.Root "Steam\steamapps\common\dota 2 beta\game\dota\bin\win64\server.dll"
        )
        Add-ServerDllCandidate $candidates (
            Join-Path $_.Root "SteamLibrary\steamapps\common\dota 2 beta\game\dota\bin\win64\server.dll"
        )
    }
}

$resolvedDll = $candidates |
    Select-Object -Unique |
    Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
    ForEach-Object { Get-Item -LiteralPath $_ } |
    Sort-Object LastWriteTimeUtc -Descending |
    Select-Object -First 1

if (-not $resolvedDll) {
    throw "server.dll not found. Set DOTA2_SERVER_DLL, DOTA2_GAME_ROOT, DOTA2_CONTENT_ROOT, or pass -DllPath."
}

$bytes = [System.IO.File]::ReadAllBytes($resolvedDll.FullName)
$text = [System.Text.Encoding]::ASCII.GetString($bytes)
$comparison = [System.StringComparison]::OrdinalIgnoreCase
$hits = [System.Collections.Generic.List[int]]::new()
$hitSet = [System.Collections.Generic.HashSet[int]]::new()

if (-not $Query.StartsWith("CDOTA_Ability_", $comparison)) {
    $normalizedQuery = ($Query -replace '[^A-Za-z0-9]', '').ToLowerInvariant()
    if ([string]::IsNullOrWhiteSpace($normalizedQuery)) {
        throw "Query must contain at least one letter or number."
    }
    $classPrefix = "CDOTA_Ability_"
    $classSearchFrom = 0

    while ($hits.Count -lt $MaxHits) {
        $classHit = $text.IndexOf($classPrefix, $classSearchFrom, $comparison)
        if ($classHit -lt 0) {
            break
        }

        $classEnd = $classHit + $classPrefix.Length
        while ($classEnd -lt $text.Length -and
            $text[$classEnd] -match '[A-Za-z0-9_]') {
            $classEnd++
        }

        $className = $text.Substring($classHit, $classEnd - $classHit)
        $normalizedClass = (
            $className.Substring($classPrefix.Length) -replace '[^A-Za-z0-9]', ''
        ).ToLowerInvariant()
        if ($normalizedClass -eq $normalizedQuery -or
            $normalizedClass.EndsWith($normalizedQuery)) {
            if ($hitSet.Add($classHit)) {
                $hits.Add($classHit)
            }
        }
        $classSearchFrom = $classEnd
    }
}

$searchFrom = 0
while ($hits.Count -lt $MaxHits) {
    $hit = $text.IndexOf($Query, $searchFrom, $comparison)
    if ($hit -lt 0) {
        break
    }
    if ($hitSet.Add($hit)) {
        $hits.Add($hit)
    }
    $searchFrom = $hit + [Math]::Max(1, $Query.Length)
}

if ($hits.Count -eq 0) {
    throw "Query '$Query' was not found in '$($resolvedDll.FullName)'. Try the exact CDOTA_Ability_* class name or raw ability name."
}

Write-Output "DLL=$($resolvedDll.FullName)"
Write-Output "QUERY=$Query"

$resourcePattern = '(?i)(^CDOTA_Ability_[A-Za-z0-9_]+$|^particles/.+\.vpcf$|^models/.+\.vmdl$|^soundevents/.+\.vsndevts$|^[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)+$|^npc_dota_[A-Za-z0-9_]+$)'
$contexts = [System.Collections.Generic.List[object]]::new()
$seenStarts = [System.Collections.Generic.HashSet[int]]::new()

foreach ($hit in $hits) {
    $contextStart = $hit
    $nearClass = $text.IndexOf("CDOTA_Ability_", $hit, $comparison)
    if ($nearClass -ge $hit -and $nearClass -le $hit + 512) {
        $contextStart = $nearClass
    }
    if (-not $seenStarts.Add($contextStart)) {
        continue
    }

    $nextClass = $text.IndexOf(
        "CDOTA_Ability_",
        $contextStart + "CDOTA_Ability_".Length,
        $comparison
    )
    $maxEnd = [Math]::Min($text.Length, $contextStart + $Radius)
    $contextEnd = if ($nextClass -gt $contextStart -and $nextClass -lt $maxEnd) {
        $nextClass
    } else {
        $maxEnd
    }
    $segment = $text.Substring($contextStart, $contextEnd - $contextStart)
    $records = [System.Collections.Generic.List[string]]::new()
    $score = 0

    foreach ($match in [System.Text.RegularExpressions.Regex]::Matches(
        $segment,
        '[ -~]{4,}'
    )) {
        $value = $match.Value
        if ($value -notmatch $resourcePattern -and
            $value.IndexOf($Query, $comparison) -lt 0) {
            continue
        }

        $offset = $contextStart + $match.Index
        $kind = if ($value -match '^CDOTA_Ability_') {
            "class"
        } elseif ($value -match '^particles/') {
            "particle"
        } elseif ($value -match '^models/') {
            "model"
        } elseif ($value -match '^soundevents/') {
            "soundfile"
        } elseif ($value -match '^npc_dota_') {
            "unit"
        } else {
            "symbol"
        }

        if ($kind -in @("particle", "model", "soundfile")) {
            $score += 10
        } elseif ($kind -eq "symbol") {
            $score += 1
        }
        $records.Add(("0x{0:X8} [{1}] {2}" -f $offset, $kind, $value))
    }

    $contexts.Add([pscustomobject]@{
        Hit = $hit
        Start = $contextStart
        Score = $score
        Records = $records
    })
}

$selectedContexts = if ($AllHits) {
    $contexts | Sort-Object Score -Descending
} else {
    $contexts | Sort-Object Score -Descending | Select-Object -First 1
}

foreach ($context in $selectedContexts) {
    Write-Output ""
    Write-Output (
        "HIT=0x{0:X8} BLOCK=0x{1:X8} SCORE={2}" -f
        $context.Hit,
        $context.Start,
        $context.Score
    )
    $context.Records | Write-Output
}
