"""Execute from the repository root using this interpreter; retain outputs on failure."""
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parent
path = root / 'assignment7.ipynb'
notebook = nbformat.read(path, as_version=4)
client = NotebookClient(notebook, timeout=1200, resources={'metadata': {'path': str(root)}})
try:
    client.execute()
finally:
    nbformat.write(notebook, path)
