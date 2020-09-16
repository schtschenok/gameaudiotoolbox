# Check if .\python_version.txt exists
if (!(Test-Path "$( $PSScriptRoot )\python_version.txt")) {
    Write-Host "Please create the .\python_version.txt file with the Python version in the following format: 3.8.5"
    pause
    exit
}

# Get Python versions
$PythonVersionParsed = $null
$PythonVersion = (Get-Content -Path "$( $PSScriptRoot )\python_version.txt" -Raw).replace("`n", "").replace("`r", "").replace("`t", "").replace(" ", "")
if (!([System.Version]::TryParse($PythonVersion, [ref]$PythonVersionParsed))) {
    Write-Host "Please specify the Python version in the format of '3.8.5' (without quotes) in the .\python_version.txt file"
    pause
    exit
}

# Remove Python and BatchFiles folders
Remove-Item -Force -Recurse -LiteralPath "$( $PSScriptRoot )\python-$( $PythonVersion )"
Remove-Item -Force -Recurse -LiteralPath "$( $PSScriptRoot )\BatchFiles"
