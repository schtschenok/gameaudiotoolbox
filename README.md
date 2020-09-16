# Game Audio Toolbox
Game Audio Toolbox is a small and ever-changing collection of scripts that may help with building game audio pipelines.

## Disclaimer
I'm not a professional programmer, so don't expect any production-ready code here. Use it at your own risk.

## Installing
1. Download the repository either via `git clone` or as a ZIP archive;
2. Run `Install.bat` script to create and configure a local Python 3 environment, install dependencies and generate executable `.bat` files for each script;
5. Use generated batch files from the `BatchFiles` folder following the instructions for each script.

## FAQ
**Q**: Where I can find the instructions for scripts?<br>
**A**: In `README.md` files in their respective folders. 

**Q**: Can I move generated scripts from the `./BatchFiles` to somewhere else?<br>
**A**: Yes!

**Q**: Can I move the Python installation from the project folder?<br>
**A**: No, it won't work, but you can move `Install.bat`, `Install.pc1`, `python_version.txt`, and `requirements.txt` to any folder on your PC and generate the Python environment there. Batch script generation will break though, so I don't recommend doing this.

## TODO
* Rewrite scripts with a much better and more uniform script structure
