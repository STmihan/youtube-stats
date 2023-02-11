import os
import shutil
from pathlib import Path

if os.path.exists("__pycache__"):
    shutil.rmtree("__pycache__")

if os.path.exists("build"):
    shutil.rmtree("build")

if os.path.exists("dist"):
    shutil.rmtree("dist")

for path in Path(".").rglob("*.pyc"):
    os.remove(path)

for path in Path(".").rglob("*.spec"):
    os.remove(path)

