param(
    [Parameter(Mandatory = $true)]
    [string]$CliPath,

    [Parameter(Mandatory = $true)]
    [string]$VpkPath,

    [string]$Pattern = ".*"
)

$ErrorActionPreference = "Stop"

$resolvedCli = (Resolve-Path -LiteralPath $CliPath).Path
$resolvedVpk = (Resolve-Path -LiteralPath $VpkPath).Path

if ([System.IO.Path]::GetExtension($resolvedVpk) -ne ".vpk") {
    throw "VpkPath must resolve to a .vpk file: $resolvedVpk"
}

try {
    $matcher = [regex]::new($Pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
}
catch {
    throw "Invalid regex Pattern '$Pattern': $($_.Exception.Message)"
}

$groups = @(
    @{ Evidence = "raw-source"; Extension = "xml" },
    @{ Evidence = "raw-source"; Extension = "css" },
    @{ Evidence = "raw-source"; Extension = "js" },
    @{ Evidence = "compiled-identity-only"; Extension = "vxml_c" },
    @{ Evidence = "compiled-identity-only"; Extension = "vcss_c" },
    @{ Evidence = "compiled-identity-only"; Extension = "vjs_c" }
)

foreach ($group in $groups) {
    $entries = & $resolvedCli -i $resolvedVpk --vpk_list -e $group.Extension -f "panorama/"
    if ($LASTEXITCODE -ne 0) {
        throw "VPK listing failed for extension '$($group.Extension)' with exit code $LASTEXITCODE"
    }

    foreach ($entry in $entries) {
        if ($matcher.IsMatch($entry)) {
            [pscustomobject]@{
                Evidence  = $group.Evidence
                Extension = $group.Extension
                Entry     = $entry
            }
        }
    }
}
