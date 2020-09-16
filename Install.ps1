# Check if .\python_version.txt exists
if (!(Test-Path "$( $PSScriptRoot )\python_version.txt")) {
    Write-Host "Please create the .\python_version.txt file with the Python version in the following format: 3.8.5"
    exit
}

# Get Python versions
$PythonVersionParsed = $null
$PythonVersion = (Get-Content -Path "$( $PSScriptRoot )\python_version.txt" -Raw).replace("`n", "").replace("`r", "").replace("`t", "").replace(" ", "")
if (!([System.Version]::TryParse($PythonVersion, [ref]$PythonVersionParsed))) {
    Write-Host "Please specify the Python version in the format of '3.8.5' (without quotes) in the .\python_version.txt file"
    exit
}
$PythonVersionShort = $PythonVersionParsed.Major, $PythonVersionParsed.Minor -join "";

# Download Python embeddable ZIP archive
try {
    Write-Host "Downloading the Python embeddable ZIP archive";
    if (Test-Path "$( $PSScriptRoot )\python-$( $PythonVersion ).zip") {
        Write-Host "Python embeddable ZIP archive already exists: $( $PSScriptRoot )\python-$( $PythonVersion ).zip$( [Environment]::NewLine )Please delete it manually"
        exit
    }
    Invoke-WebRequest "https://www.python.org/ftp/python/$( $PythonVersion )/python-$( $PythonVersion )-embed-amd64.zip" -OutFile "$( $PSScriptRoot )\python-$( $PythonVersion ).zip"
}
catch {
    Write-Host "Can't download the Python embeddable ZIP archive"
    exit
}

# Unpack Python embeddable ZIP archive
try {
    if (Test-Path "$( $PSScriptRoot )\python-$( $PythonVersion )") {
        Write-Host "Python embeddable folder already exists: $( $PSScriptRoot )\python-$( $PythonVersion )$( [Environment]::NewLine )Please delete it manually"
        exit
    }
    Write-Host "Unpacking the Python embeddable ZIP archive"
    Expand-Archive -LiteralPath "$( $PSScriptRoot )\python-$( $PythonVersion ).zip" -DestinationPath "$( $PSScriptRoot )\python-$( $PythonVersion )"
}
catch {
    Write-Host "Can't unpack the Python embeddable ZIP archive"
    exit
}

# Delete Python embeddable ZIP archive
try {
    Write-Host "Deleting the Python embeddable ZIP archive"
    Remove-Item -LiteralPath "$( $PSScriptRoot )\python-$( $PythonVersion ).zip"
}
catch {
    Write-Host "Can't delete the Python embeddable ZIP archive"
    exit
}

# Create sitecustomize.py
try {
    Write-Host "Creating sitecustomize.py"
    New-Item -Path "$( $PSScriptRoot )\python-$( $PythonVersion )" -Name "sitecustomize.py" -ItemType File -Value "import sys$( [Environment]::NewLine )sys.path.insert(0, '')";
}
catch {
    Write-Host "Can't create sitecustomize.py"
    exit
}

# Modify ._pth file
try {
    Write-Host "Modifying ._pth file"
    Add-Content -Path "$( $PSScriptRoot )\python-$( $PythonVersion )\python$( ($PythonVersionShort) )._pth" -Value "import site";
}
catch {
    Write-Host "Can't modify ._pth file"
    exit
}

# Download get-pip.py
try {
    Write-Host "Downloading the get-pip.py";
    if (Test-Path "$( $PSScriptRoot )\get-pip.py") {
        Write-Host "get-pip.py already exists: $( $PSScriptRoot )\get-pip.py$( [Environment]::NewLine )Please delete it manually"
        exit
    }
    Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "$( $PSScriptRoot )\get-pip.py"
}
catch {
    Write-Host "Can't download the get-pip.py"
    exit
}

# Run get-pip.py
try {
    Write-Host "Running the get-pip.py"
    & "$( $PSScriptRoot )\python-$( $PythonVersion )\python.exe" "$( $PSScriptRoot )\get-pip.py"
}
catch {
    Write-Host "Can't run the get-pip.py"
    exit
}

# Delete get-pip.py
try {
    Write-Host "Running the get-pip.py"
    Remove-Item -LiteralPath "$( $PSScriptRoot )\get-pip.py"
}
catch {
    Write-Host "Can't delete the get-pip.py"
    exit
}

# Install Pyhon packages
try {
    if (!(Test-Path "$( $PSScriptRoot )\requirements.txt")) {
        Write-Host "Can't find the requirements.txt file"
        exit
    }
    Invoke-Expression "$( $PSScriptRoot )\python-$( $PythonVersion )\Scripts\pip.exe install -U --no-cache-dir --no-warn-script-location -r $( $PSScriptRoot )\requirements.txt"
}
catch {
    Write-Host "Can't install Python packages from the requirements.txt file"
    exit
}


# Generate Batch files
try {
    Get-ChildItem -LiteralPath $PSScriptRoot -Directory | ForEach-Object {
        if (Test-Path "$( $PSScriptRoot )\$( $_.Name )\$( $_.Name ).py") {
            Write-Output "Creating $( $PSScriptRoot )\BatchFiles\$( $_.Name ).bat file"
            New-Item -Path "$( $PSScriptRoot )\BatchFiles\$( $_.Name ).bat" -ItemType File -Force -Value """$( $PSScriptRoot )\python-$( $PythonVersion)\python.exe"" ""$( $PSScriptRoot )\$( $_.Name)\$( $_.Name).py"" %*"
        }
    }
}
catch {
    Write-Host "Can't create batch files"
    exit
}