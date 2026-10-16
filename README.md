# backlink-spam-list

[中文](README.zh-CN.md) · [Browse the list](https://jasonzhu.ai/en/backlink-spam-list)

A shared list of sites that build or sell spam backlinks, each with evidence anyone can check on the public web. Before you submit your site somewhere, or when odd links start pointing at it, look the domain up here.

**568 entries** in `list.csv`, most of them doorway domains of eleven networks that redirect to a handful of storefronts selling backlinks:

| Family | Doorway domains | Storefront | Shared title |
|---|---|---|---|
| freerelevantlinks | 126 | freerelevantlinks.com | Free Relevant Links — Remove backlinks or earn relevant ones |
| rankzly | 89 | rankzly.com | Premium SEO Backlinks Services - Boost DR, DA & TF |
| skylinkseo | 78 | skylinkseo.com | SkyLinkSEO — SEO Services & Software House ¦ DR, DA, TF, PBN, Guest Po |
| backlinksnexa | 69 | backlinksnexa.com | BacklinksNexa — Buy High-Authority Backlinks, Guest Posts & Niche Edit |
| seoboost | 62 | seoboost.agency | SEO Boost Agency — SEO Authority & Backlink Services |
| cvgorilla | 50 | cvgorilla.com | Crawl Visibility SEO — Get Found on Page One ¦ CVGorilla |
| buyseolink | 29 | buyseolink.com | BuySEOLink — Premium SEO Authority Packages |
| link-baron | 19 | link-baron.com | LinkBaron — The Quiet Backlink Atelier |
| americanlegalguide-title | 12 | – | AmericanLegalGuide.com |
| toprankflow | 10 | toprankflow.com | Increase DR, DA, TF & Buy High Quality Backlinks 2026 ¦ TopRankFlow —  |
| seo-rank-boost | 5 | – | SEO Rank Boost |

The largest family is 126 numbered `.xyz` domains that all redirect to one site offering to "remove backlinks or earn relevant ones", with the same two Stripe checkout links on every page.

## What goes in

| Category | What it means | Evidence it needs |
|---|---|---|
| `link-network` | one operator's sites | a page title, a redirect, a checkout link or an analytics account shared with other listed sites |
| `link-seller` | selling links is its business | its own pages: PBN, DR and DA packages, guest posts for sale, or the storefront a network redirects to |
| `hacked` | a page injected into a hacked site | the injected page or link, such as a checkout link for gambling or adult products |
| `shortener` | a URL shortener used for bulk "backlinks" | the site itself |

Every entry carries its evidence and a public URL where anyone can see it, the date it was first listed and the date it was last checked. A tool's score (a spam score, a "SPAM" mark) is not evidence on its own, and is not published here.

What does not go in: a directory that sells followed listings but is otherwise a real site (that is a policy risk to weigh, not a network; [backlink-guard](https://github.com/zhuyansen/backlink-guard) shows it), and a site that no longer loads.

## Report a site

[Open a report](../../issues/new?template=report.yml): the domain, the category, a URL and what it shows. A check runs at once and comments what it saw: the site's own pages read by backlink-guard, and whether the words you quoted are on the evidence page. A maintainer then replies `/approve <category>` to add it, or `/reject <reason>`.

## Dispute an entry

[Open a dispute](../../issues/new?template=dispute.yml) if an entry is wrong or out of date, for example when a domain has changed hands. A maintainer replies `/remove` or `/keep`. A removed entry keeps its line with status `removed` and the issue that removed it, so the history stays.

## Use it

`list.csv` columns: `domain, category, family, evidence, evidence_url, first_listed, last_checked, status, source`. Only rows with status `listed` are current.

```bash
curl -s https://raw.githubusercontent.com/zhuyansen/backlink-spam-list/main/list.csv | grep ',listed,'
```

[backlink-guard](https://github.com/zhuyansen/backlink-guard) reads it on every `vet` from version 0.5: a listed site is marked avoid, with the entry's evidence.

## How the first entries were found

568 domains from link sources checked on 2026-10-16. A third-party spam score chose which sites to look at; what put each one here is what its own pages show: a title shared with dozens of other domains, a redirect to a storefront that sells backlinks, a checkout link or an analytics account shared across the family, or a title that sells DR, DA and PBN packages. Sites that no longer load were left out.

## License

The scripts are MIT ([LICENSE](LICENSE)). The list is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use it anywhere, and say where it came from.
