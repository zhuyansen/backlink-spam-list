"""The list itself: one CSV, read and written in one place so every script agrees on it."""
from __future__ import annotations

import csv
import io
import re
from datetime import date
from pathlib import Path

LIST = Path(__file__).resolve().parent.parent / "list.csv"
FIELDS = ["domain", "category", "family", "evidence", "evidence_url", "first_listed", "last_checked", "status", "source"]
CATEGORIES = {
    "link-network": "one operator's sites: a shared page template, analytics or ads account, or checkout link",
    "link-seller": "selling links is its business: PBN, DR and DA packages, guest posts for sale",
    "hacked": "a page injected into a hacked site, such as a checkout link for gambling or adult products",
    "shortener": "a URL shortener used to make bulk 'backlinks'",
}
STATUSES = ("listed", "disputed", "removed")
DOMAIN = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:[a-z]{2,24}|xn--[a-z0-9-]{2,59})$")
MEMBERS_MAX = 30                 # other sites of one network a report can add


def domain_of(text: str) -> str:
    """"https://www.Example.com/path" -> "example.com"; "" when it is no domain."""
    host = re.sub(r"^[a-z]+://", "", text.strip().lower()).split("/")[0].split(":")[0]
    host = host[4:] if host.startswith("www.") else host
    return host if DOMAIN.match(host) else ""


def read(path: Path | None = None) -> list[dict]:
    path = path or LIST              # looked up at call time, so a test can point LIST elsewhere
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8")))) if path.exists() else []


def write(rows: list[dict], path: Path | None = None) -> None:
    path = path or LIST
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(sorted(rows, key=lambda r: (r["domain"])))
    path.write_text(out.getvalue(), encoding="utf-8")


def problems(rows: list[dict]) -> list[str]:
    """What is wrong with the list, one line each; empty when it is fine."""
    out, seen = [], set()
    for i, r in enumerate(rows, start=2):
        d = r.get("domain", "")
        if domain_of(d) != d:
            out.append(f"line {i}: '{d}' is not a bare domain (lower case, no www., no path)")
        if d in seen:
            out.append(f"line {i}: {d} is listed twice")
        seen.add(d)
        if r.get("category") not in CATEGORIES:
            out.append(f"line {i}: {d}: category '{r.get('category')}' is not one of {sorted(CATEGORIES)}")
        if r.get("status") not in STATUSES:
            out.append(f"line {i}: {d}: status '{r.get('status')}' is not one of {STATUSES}")
        if not r.get("evidence", "").strip() or not r.get("evidence_url", "").startswith(("http://", "https://")):
            out.append(f"line {i}: {d}: an entry needs evidence and a public URL where anyone can see it")
        for f in ("first_listed", "last_checked"):
            try:
                date.fromisoformat(r.get(f, ""))
            except ValueError:
                out.append(f"line {i}: {d}: {f} '{r.get(f)}' is not a date (YYYY-MM-DD)")
    if [r["domain"] for r in rows] != sorted(r["domain"] for r in rows):
        out.append("the list is not sorted by domain (scripts/lib.write sorts it)")
    return out


def form_fields(body: str) -> dict[str, str]:
    """The answers of a GitHub issue form: "### Label\\n\\nanswer" blocks, "_No response_" read as empty."""
    fields = {}
    for m in re.finditer(r"^### (.+?)\s*\n(.*?)(?=^### |\Z)", body or "", re.S | re.M):
        value = m.group(2).strip()
        fields[m.group(1).strip().lower()] = "" if value == "_No response_" else value
    return fields


def members_of(form: dict[str, str], main: str) -> list[str]:
    """The other sites of the same network a report names, as bare domains: no repeats, not the reported one."""
    out: list[str] = []
    for word in re.split(r"[\s,]+", form.get("other sites of the same network", "")):
        domain = domain_of(word)
        if domain and domain != main and domain not in out:
            out.append(domain)
    return out[:MEMBERS_MAX]
