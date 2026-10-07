$ErrorActionPreference = 'Stop'
$obsilFrontend = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../frontend'))
Push-Location $obsilFrontend
try {
    & node.exe node_modules/next/dist/bin/next dev --hostname 127.0.0.1 --port 3000
} finally { Pop-Location }
