"""The scripts on made-up issues: no network, the list in a temporary file."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import apply_command  # noqa: E402
import check_report  # noqa: E402
import lib  # noqa: E402

REPORT = """### Domain

https://www.Rank-Shop.example/pricing

### Category

link-seller (selling links is its business - PBN, DR and DA packages)

### Evidence URL

https://rank-shop.example/pricing

### What the page shows

"DR 50+ dofollow backlinks for $29"

### How you came across it

_No response_
"""


@pytest.fixture(autouse=True)
def temp_list(tmp_path, monkeypatch):
    monkeypatch.setattr(lib, "LIST", tmp_path / "list.csv")
    lib.write([])


def test_the_form_and_the_domain_are_read():
    form = lib.form_fields(REPORT)
    assert form["category"].startswith("link-seller") and form["how you came across it"] == ""
    assert lib.domain_of(form["domain"]) == "rank-shop.example" and lib.domain_of("not a domain") == ""


def test_problems_name_what_is_wrong():
    good = {"domain": "a.example", "category": "link-network", "family": "", "evidence": "shared title",
            "evidence_url": "https://a.example/", "first_listed": "2026-10-16", "last_checked": "2026-10-16",
            "status": "listed", "source": "seed"}
    assert lib.problems([good]) == []
    bad = {**good, "domain": "www.B.example", "category": "spam", "evidence_url": "a.example", "last_checked": "soon"}
    found = " | ".join(lib.problems([good, bad]))
    assert "not a bare domain" in found and "category 'spam'" in found and "needs evidence" in found and "not a date" in found


def test_approve_adds_reject_does_not():
    rows = []
    reply, changed = apply_command.apply("approve", "", lib.form_fields(REPORT), ["report"], "12", "2026-10-16", rows)
    assert changed and rows[0]["domain"] == "rank-shop.example" and rows[0]["category"] == "link-seller" and rows[0]["source"] == "#12"
    reply, changed = apply_command.apply("reject", "no price on the page", lib.form_fields(REPORT), ["report"], "13", "2026-10-16", [])
    assert not changed and "no price on the page" in reply
    reply, changed = apply_command.apply("remove", "", lib.form_fields(REPORT), ["report"], "14", "2026-10-16", rows)
    assert not changed and "for disputes" in reply


def test_remove_keeps_the_line_and_says_why(monkeypatch, tmp_path):
    rows = []
    apply_command.apply("approve", "link-network", lib.form_fields(REPORT), ["report"], "12", "2026-10-16", rows)
    dispute = "### Domain\n\nrank-shop.example\n\n### Why the entry is wrong\n\nIt changed hands; no links for sale.\n"
    reply, changed = apply_command.apply("remove", "new owner", lib.form_fields(dispute), ["dispute"], "20", "2026-11-01", rows)
    assert changed and rows[0]["status"] == "removed" and "removed in #20" in rows[0]["source"] and rows[0]["category"] == "link-network"


def test_only_maintainers_are_obeyed(monkeypatch, tmp_path):
    out = tmp_path / "out.txt"
    monkeypatch.setenv("COMMENT_BODY", "/approve link-seller")
    monkeypatch.setenv("COMMENT_ASSOCIATION", "NONE")
    monkeypatch.setenv("ISSUE_BODY", REPORT)
    monkeypatch.setenv("ISSUE_LABELS", json.dumps(["report"]))
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("OUT", str(tmp_path / "c.md"))
    apply_command.main()
    assert "commit=false" in out.read_text() and lib.read() == []
    monkeypatch.setenv("COMMENT_ASSOCIATION", "OWNER")
    apply_command.main()
    assert "commit=true" in out.read_text() and lib.read()[0]["domain"] == "rank-shop.example"


def test_the_check_says_what_it_saw():
    text = check_report.comment(lib.form_fields(REPORT), None,
                                {"title": "Rank Shop", "flags": [{"flag": "paid_follow", "level": "caution", "evidence": "$29 dofollow"}]}, True)
    assert "`rank-shop.example`" in text and "paid_follow" in text and "**is** on the evidence page" in text
    assert "`/approve link-seller`" in text
    assert check_report.quoted('"DR 50+ dofollow backlinks for $29"', "Buy now: DR 50+ dofollow backlinks for $29 today")
