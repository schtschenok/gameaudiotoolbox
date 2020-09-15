powershell.exe -Command ^
if (!(Test-Path 'python_version.txt')) { Write-Warning 'Please create a python_version.txt file with the Python version number you want to install in this format: 3.8.5'; exit };^
$PythonVersion = Get-Content python_version.txt -First 1;^
$PythonVersion = $PythonVersion -Replace ' ';^
$PythonFolder = 'python-{0}' -f $PythonVersion;^
Remove-Item -LiteralPath $PythonFolder;^
Remove-Item -LiteralPath 'BatchFiles';^
Remove-Item -LiteralPath $PythonFolder;

pause