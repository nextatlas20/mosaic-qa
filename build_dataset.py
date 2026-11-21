"""Build the MosaicQA release bundle from the annotation shards."""

import argparse
import json
from pathlib import Path


def load_shard(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def build(languages, source_dir="annotations", out_dir="data"):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for lang in languages:
        shard = load_shard(Path(source_dir) / f"{lang}.json")
        target = out / f"mosaicqa_{lang}.jsonl"
        with target.open("w", encoding="utf-8") as fh:
            for row in shard["items"]:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"{lang}: {len(shard['items'])} questions -> {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", default="en")
    parser.add_argument("--out", default="data")
    args = parser.parse_args()
    build(args.languages.split(","), out_dir=args.out)
