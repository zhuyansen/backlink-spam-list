"""The families of the list as a Markdown table, for the README: doorways, storefront, the shared title."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402


def table(rows: list[dict]) -> str:
    fam = defaultdict(lambda: {"doors": 0, "store": "", "title": ""})
    for r in rows:
        if r["status"] != "listed" or not r["family"]:
            continue
        f = fam[r["family"]]
        if r["category"] == "link-seller":
            f["store"] = r["domain"]
        else:
            f["doors"] += 1
            f["title"] = f["title"] or r["evidence"].split('"')[1][:70] if '"' in r["evidence"] else f["title"]
    lines = ["| Family | Doorway domains | Storefront | Shared title |", "|---|---|---|---|"]
    for name, f in sorted(fam.items(), key=lambda kv: -kv[1]["doors"]):
        lines.append(f"| {name} | {f['doors']} | {f['store'] or '–'} | {f['title'].replace('|', '¦')} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(table(lib.read()))
