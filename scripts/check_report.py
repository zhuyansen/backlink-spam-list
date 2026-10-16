"""A new report: read the reported site and the evidence page (free), and say what was seen.

Env: ISSUE_BODY (the issue form), OUT (where the comment goes). Writes the comment; never changes the list.
The report form's answers arrive untrusted, so they are only read as text, never run.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402

UA = "Mozilla/5.0 (compatible; backlink-spam-list check; +https://github.com/zhuyansen/backlink-spam-list)"


def page_text(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as res:
            html = res.read(1_500_000).decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001 — any failure is reported as such
        return f"__failed__ {type(exc).__name__}"
    return " ".join(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", html, flags=re.S | re.I).split())


def quoted(evidence: str, text: str) -> bool:
    """Whether a quoted stretch of the evidence (text in quotes, or the first 60 characters) is on the page."""
    parts = re.findall(r"[\"“']([^\"”']{12,})[\"”']", evidence) or [evidence[:60]]
    norm = lambda s: " ".join(s.lower().split())  # noqa: E731
    return any(norm(p) in norm(text) for p in parts if p.strip())


def vet_free(domains: list[str]) -> list[dict]:
    """backlink-guard's free check of the sites in one run: their own pages, and the template or accounts they
    share, which only shows when they are checked together. [] when it is not installed or fails."""
    try:
        out = subprocess.run([sys.executable, "-m", "backlink_guard", "vet", *domains, "--free", "--json",
                              "--limit", str(len(domains))], capture_output=True, text=True, timeout=600)
        return json.loads(out.stdout)["rows"]
    except Exception:  # noqa: BLE001
        return []


def site_line(domain: str, entry: dict | None, row: dict | None) -> str:
    said = []
    if entry:
        said.append(f"already in the list as **{entry['category']}** ({entry['status']}, since {entry['first_listed']})")
    if row:
        found = [f"{f['flag']} ({f['evidence'][:80]})" for f in row.get("flags", []) if f.get("level") != "note"]
        said.append(f"title \"{row.get('title', '')[:80]}\"; " + ("; ".join(found) if found else "nothing found on its pages"))
    return f"- `{domain}`: " + ("; ".join(said) or "could not be checked") + "."


def comment(form: dict[str, str], listed: dict[str, dict], rows: list[dict], evidence_seen: bool | None) -> str:
    domain = lib.domain_of(form.get("domain", ""))
    if not domain:
        return "This does not look like a domain. Please edit the report with the bare domain, such as `example.com`."
    members, by_site = lib.members_of(form, domain), {r.get("domain"): r for r in rows}
    lines = [f"Checked `{domain}`" + (f" and {len(members)} other site(s) of the same network, in one run:" if members else ":")]
    lines += [site_line(d, listed.get(d), by_site.get(d)) for d in [domain, *members]]
    if evidence_seen is not None:
        lines.append("- The quoted evidence " + ("**is** on the evidence page." if evidence_seen else
                     "was **not** found on the evidence page (it may be drawn by a script; a maintainer looks by hand)."))
    category = form.get("category", "").split(" ")[0]
    lines += ["", f"A maintainer can reply `/approve {category if category in lib.CATEGORIES else '<category>'}` to add "
              + ("them all" if members else "it") + ", or `/reject <reason>`."]
    return "\n".join(lines)


def main() -> int:
    form = lib.form_fields(os.environ.get("ISSUE_BODY", ""))
    domain = lib.domain_of(form.get("domain", ""))
    sites = [domain, *lib.members_of(form, domain)] if domain else []
    listed = {r["domain"]: r for r in lib.read() if r["domain"] in sites}
    url = form.get("evidence url", "")
    text = page_text(url) if url.startswith(("http://", "https://")) else ""
    seen = None if not text or text.startswith("__failed__") else quoted(form.get("what the page shows", ""), text)
    Path(os.environ.get("OUT", "comment.md")).write_text(comment(form, listed, vet_free(sites) if sites else [], seen))
    return 0


if __name__ == "__main__":
    sys.exit(main())
