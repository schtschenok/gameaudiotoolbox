powershell.exe -Command ^
if (!(Test-Path 'requirements.txt')) { Write-Warning 'Please create a requirements.txt file'; exit };^
$PythonVersion = Get-Content python_version.txt -First 1;^
$PythonVersion = $PythonVersion -Replace ' ';^
$PythonExe = 'python-{0}/python.exe' -f $PythonVersion;^
$PipExe = 'python-{0}/Scripts/pip.exe' -f $PythonVersion;^
$PipCommand = '{0} install -U --no-cache-dir --no-warn-script-location -r requirements.txt' -f $PipExe;^
Invoke-Expression $PipCommand;

pause