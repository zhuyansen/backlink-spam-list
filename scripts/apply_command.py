"""A maintainer's command in an issue comment, applied to list.csv.

  /approve [category]   (on a report)   add the reported site and the other sites it names, or refresh their check date
  /reject [reason]      (on a report)   leave the list as it is
  /remove [reason]      (on a dispute)  mark the entry removed; the line stays, so the history does
  /keep [reason]        (on a dispute)  leave the entry as it is

Env: COMMENT_BODY, COMMENT_ASSOCIATION, ISSUE_BODY, ISSUE_NUMBER, ISSUE_LABELS (JSON list), TODAY, OUT,
GITHUB_OUTPUT. Only the repository's owner, members and collaborators are obeyed.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402

MAINTAINERS = {"OWNER", "MEMBER", "COLLABORATOR"}
COMMAND = re.compile(r"^/(approve|reject|remove|keep)\b[ \t]*(.*)$", re.M)


def apply(command: str, arg: str, form: dict[str, str], labels: list[str], number: str, today: str,
          rows: list[dict]) -> tuple[str, bool]:
    """(the reply, whether the list changed). `rows` is changed in place."""
    domain = lib.domain_of(form.get("domain", ""))
    if not domain:
        return "No domain in this issue's form, so nothing was changed.", False
    entry = next((r for r in rows if r["domain"] == domain), None)
    if command in ("approve", "reject") and "report" not in labels:
        return f"`/{command}` is for reports.", False
    if command in ("remove", "keep") and "dispute" not in labels:
        return f"`/{command}` is for disputes.", False
    if command == "reject":
        return f"Not added: {arg or 'the evidence does not show it'}.", False
    if command == "keep":
        return f"`{domain}` stays listed: {arg or 'the evidence still holds'}.", False
    if command == "remove":
        if not entry:
            return f"`{domain}` is not in the list.", False
        entry.update(status="removed", last_checked=today, source=f"{entry['source']}; removed in #{number}")
        return f"`{domain}` is now marked removed ({arg or 'dispute upheld'}).", True
    category = arg.split()[0] if arg.split() and arg.split()[0] in lib.CATEGORIES else form.get("category", "").split(" ")[0]
    if category not in lib.CATEGORIES:
        return f"Say the category: `/approve <{'|'.join(lib.CATEGORIES)}>`.", False
    members = lib.members_of(form, domain)
    if members:
        return approve_network(domain, members, category, form, number, today, rows), True
    if entry:
        entry.update(category=category, status="listed", last_checked=today)
        return f"`{domain}` was already listed; its category and check date are updated.", True
    rows.append({"domain": domain, "category": category, "family": "", "evidence": form.get("what the page shows", "")[:400],
                 "evidence_url": form.get("evidence url", ""), "first_listed": today, "last_checked": today,
                 "status": "listed", "source": f"#{number}"})
    return f"Added `{domain}` as **{category}**.", True


def approve_network(domain: str, members: list[str], category: str, form: dict[str, str], number: str, today: str,
                    rows: list[dict]) -> str:
    """The reported site and the other sites of its network, one family named after the reported site; each other
    site's own home page is its evidence URL, since what they share shows there."""
    added, updated = [], []
    for site in [domain, *members]:
        entry = next((r for r in rows if r["domain"] == site), None)
        if entry:
            entry.update(category=category, status="listed", last_checked=today)
            updated.append(site)
            continue
        rows.append({"domain": site, "category": category, "family": domain, "evidence": form.get("what the page shows", "")[:400],
                     "evidence_url": form.get("evidence url", "") if site == domain else f"https://{site}/",
                     "first_listed": today, "last_checked": today, "status": "listed", "source": f"#{number}"})
        added.append(site)
    names = ", ".join(f"`{s}`" for s in added[:10]) + (f" and {len(added) - 10} more" if len(added) > 10 else "")
    said = [f"Added {len(added)} as **{category}**, the `{domain}` family: {names}." if added else "Nothing new to add."]
    return " ".join(said + ([f"{len(updated)} already listed: category and check date updated."] if updated else []))


def main() -> int:
    body = os.environ.get("COMMENT_BODY", "")
    m = COMMAND.search(body)
    out = {"say": "false", "close": "false", "commit": "false"}
    if m and os.environ.get("COMMENT_ASSOCIATION", "") in MAINTAINERS:
        rows = lib.read()
        reply, changed = apply(m.group(1), m.group(2).strip(), lib.form_fields(os.environ.get("ISSUE_BODY", "")),
                               json.loads(os.environ.get("ISSUE_LABELS", "[]")), os.environ.get("ISSUE_NUMBER", ""),
                               os.environ.get("TODAY", date.today().isoformat()), rows)
        if changed:
            problems = lib.problems(sorted(rows, key=lambda r: r["domain"]))
            if problems:
                reply, changed = "Not changed, the entry would break the list: " + "; ".join(problems[:3]), False
            else:
                lib.write(rows)
        Path(os.environ.get("OUT", "comment.md")).write_text(reply)
        out.update(say="true", close="true", commit="true" if changed else "false")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as f:
        f.writelines(f"{k}={v}\n" for k, v in out.items())
    return 0


if __name__ == "__main__":
    sys.exit(main())
