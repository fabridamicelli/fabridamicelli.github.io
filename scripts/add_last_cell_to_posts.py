import json
from pathlib import Path

POSTS_PATH = Path(".").resolve().parent/"posts"
LAST_CELL_PATH = Path(".")/"fin.json"
last_cell = json.loads(LAST_CELL_PATH.read_text())

nb_paths = [p for p in POSTS_PATH.iterdir() if p.name.endswith(".ipynb")]

for path in nb_paths:
    print(f"Adding last cell to {path.name}")
    nb = json.loads(path.read_text())
    nb["cells"][-1] = last_cell
    path.write_text(json.dumps(nb))

