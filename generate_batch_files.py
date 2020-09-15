import sys
import os
from pathlib import Path

current_dir = Path(os.getcwd()).resolve()
python_executable = Path(sys.executable).resolve()
batch_dir = current_dir / "BatchFiles"

for item in current_dir.glob("*"):
    if item.is_dir():
        if (python_script := (item / (item.name + ".py"))).is_file():
            with open(batch_dir / (item.name + ".bat"), "w+") as f:
                f.write(f"\"{python_executable}\" \"{python_script}\" %*")
