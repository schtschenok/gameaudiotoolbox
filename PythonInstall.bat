powershell.exe -Command ^
if (!(Test-Path 'python_version.txt')) { Write-Warning 'Please create a python_version.txt file with the Python version number you want to install in this format: 3.8.5'; exit };^
$PythonVersion = Get-Content python_version.txt -First 1;^
$PythonVersion = $PythonVersion -Replace ' ';^
$PythonVersionShort = $PythonVersion -Replace '\.', '';^
$PythonVersionShort = $PythonVersionShort.Substring(0, 2);^
$PythonUrl = 'https://www.python.org/ftp/python/{0}/python-{0}-embed-amd64.zip' -f $PythonVersion;^
$PythonZip = 'python-{0}.zip' -f $PythonVersion;^
$PythonFolder = 'python-{0}' -f $PythonVersion;^
$PythonExe = 'python-{0}/python.exe' -f $PythonVersion;^
$Pth = 'python-{0}/python{1}._pth' -f $PythonVersion, $PythonVersionShort;^
$PthContents = 'import site';^
$Sitecustomize = 'python-{0}/sitecustomize.py' -f $PythonVersion;^
$SitecustomizeContents = 'import sys{0}sys.path.insert(0, \"\")' -f [Environment]::NewLine;^
$GetPipUrl = 'https://bootstrap.pypa.io/get-pip.py';^
$GetPip = 'get-pip.py';^
Invoke-WebRequest $PythonUrl -OutFile $PythonZip;^
Expand-Archive -LiteralPath $PythonZip -DestinationPath $PythonFolder;^
Remove-Item -LiteralPath $PythonZip;^
Add-Content -Path $Pth -Value $PthContents;^
New-Item -Path $PythonFolder -Name "sitecustomize.py" -ItemType "file" -Value $SitecustomizeContents;^
Invoke-WebRequest $GetPipUrl -OutFile $GetPip;^
& $PythonExe $GetPip;^
Remove-Item -LiteralPath $GetPip;

pause