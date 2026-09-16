import subprocess
from pathlib import Path

# Download the PyTorch docs from GitHub and save them to the data/raw/pytorch_docs directory.

OUTPUT_DIR = Path("data/raw/pytorch_docs")

OUTPUT_DIR.parent.mkdir(parents=True, exist_ok=True)

subprocess.run([
    "git",
    "clone",
    "--depth", "1",
    "--branch", "site",
    "https://github.com/pytorch/docs.git",
    str(OUTPUT_DIR)
])

print("PyTorch docs downloaded.")