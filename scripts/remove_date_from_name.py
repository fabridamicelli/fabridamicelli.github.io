import json
from pathlib import Path
import yaml
import re


POSTS_PATH = Path(__file__).parent.parent / "posts"

nb_paths = [p for p in POSTS_PATH.iterdir() if p.name.endswith(".ipynb")]


def get_config(nb: dict):
    yml = "".join(
        nb["cells"][0]["source"][1:-1]
    )  # remove --- at start and end (invalid yaml)
    return yaml.safe_load(yml)


def startswith_date(s: str):
    match = re.match(r"\d\d\d\d-\d\d-\d\d-", s)
    if match:
        return True
    return False


def update_config(config):
    old_out_file = config["output-file"]

    new_out_file = old_out_file.replace("_", "-")

    if not startswith_date(new_out_file):
        print("no date", new_out_file)
        return config

    print(new_out_file)
    new_out_file = new_out_file[11:]  # remove date len(YYYY-mm-dd-) = 11

    # Keep old out_file as alias to let old links still work
    old_aliases = config.get("aliases", [])
    aliases = {"aliases": old_aliases + [f"/posts/{old_out_file}"]}
    out_file = {"output-file": new_out_file}
    print("old name:", old_out_file)
    print("new name:", new_out_file)
    print("aliases:", aliases)
    return config | out_file | aliases


for path in nb_paths:
    print(f"Removing date from name for {path.name}")
    nb = json.loads(path.read_text())
    cfg = get_config(nb)

    new_cfg = update_config(config=cfg)
    new_cfg_lines = f"{yaml.dump(new_cfg)}".split("\n")
    nb["cells"][0]["source"] = [
        f"{line}\n" for line in ["---"] + new_cfg_lines + ["---"]
    ]
    path.write_text(json.dumps(nb))
    print("-----------------------------------------------------")
