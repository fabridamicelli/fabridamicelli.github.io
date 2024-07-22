import json
from pathlib import Path
import yaml

PLATFORMS = (
    "twitter",
    "reddit",
    "linkedin",
    "mastodon",
)


POSTS_PATH = Path(__file__).parent.parent / "posts"
SHARE_BLOCK_PATH = Path(__file__).parent / "share.txt"
share_block_lines = SHARE_BLOCK_PATH.read_text().splitlines()

nb_paths = [p for p in POSTS_PATH.iterdir() if p.name.endswith(".ipynb")]


def get_config(nb: dict):
    yml = "".join(nb["cells"][0]["source"][1:-1]) # remove --- at start and end (invalid yaml)
    return yaml.safe_load(yml)


def make_permalink(out_file: str):
    return f"https://fabridamicelli.github.io/posts/{out_file}"


def make_description(title, desc):
    return f"{title}. {desc}"


def update_config(config, permalink, description):
    share = {
        "filters": [
            "social-share"
        ],
        "share": {
            "permalink": permalink,
            "description": description,
        }
        | {p: True for p in PLATFORMS},
    }
    return config | share


for path in nb_paths:
    print(f"Adding share block to {path.name}")
    nb = json.loads(path.read_text())
    cfg = get_config(nb)

    desc = make_description(cfg["title"], cfg["description"])
    permalink = make_permalink(cfg["output-file"])
    new_cfg = update_config(config=cfg, permalink=permalink, description=desc)
    new_cfg_lines = f"---\n{yaml.dump(new_cfg)}\n---".split("\n")
    nb["cells"][0]["source"] = [f"{line}\n" for line in new_cfg_lines]
    path.write_text(json.dumps(nb))
