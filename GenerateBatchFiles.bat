powershell.exe -Command ^
if (!(Test-Path 'python_version.txt')) { Write-Warning 'Please create a python_version.txt file with the Python version number you want to install in this format: 3.8.5'; exit };^
$PythonVersion = Get-Content python_version.txt -First 1;^
$PythonVersion = $PythonVersion -Replace ' ';^
$PythonExe = 'python-{0}/python.exe' -f $PythonVersion;^
if (!(Test-Path 'BatchFiles')) { New-Item -Path '.' -Name 'BatchFiles' -ItemType 'directory' };^
$PythonScript = 'generate_batch_files.py';^
& $PythonExe $PythonScript;

pause