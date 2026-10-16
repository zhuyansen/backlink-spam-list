"""Check list.csv: bare domains, once each, known categories and statuses, evidence with a public URL, dates."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402

if __name__ == "__main__":
    rows = lib.read()
    found = lib.problems(rows)
    print("\n".join(found) if found else f"list.csv: {len(rows)} entries, fine")
    sys.exit(1 if found else 0)
