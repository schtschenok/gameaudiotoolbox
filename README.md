# Game Audio Toolbox
Game Audio Toolbox is a small and ever-changing collection of scripts that may help with building game audio pipelines.

## Disclaimer
I'm not a professional programmer, so don't expect any production-ready code here. Use it at your own risk.

## Installing
1. Download the repository either via `git clone` or as a ZIP archive;
2. Run `PythonInstall.bat` script to create and configure a local Python 3 environment;
3. Run `PythonInstallPackages.bat` script to install all dependencies;
4. Run `GenerateBatchFiles.bat` script to generate executable `.bat` files for each script;
5. Use generated batch files from `BatchFiles` folder following the instructions for each script.

## FAQ
**Q**: Where I can find the instructions for scripts?<br>
**A**: In `README.md` files in their respective folders. 

**Q**: Can I move generated scripts from the `./BatchFiles` to somewhere else?<br>
**A**: Yes!

**Q**: Can I move the Python installation from the project folder?<br>
**A**: No, it won't work, but you can move `PythonInstall.bat`, `PythonInstallPackages.bat`, `python_version.txt`, and `requirements.txt` to any folder on your PC and generate the Python environment there.

## TODO
* Rewrite Batch scripts to the proper PowerShell, while still avoiding execution policy restrictions;
* Move Batch scripts to another folder or a single file (get rid of three separate scripts to run);
* Write much better and more uniform script structure;
