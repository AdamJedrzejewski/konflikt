$ErrorActionPreference = 'Stop'
$obsilBackend = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../backend'))
$obsilPython = Join-Path $obsilBackend '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $obsilPython)) { throw 'Brak środowiska backend/.venv.' }
Push-Location $obsilBackend
try {
    & $obsilPython -m uvicorn app.main:app --host 127.0.0.1 --port 8001
} finally { Pop-Location }
