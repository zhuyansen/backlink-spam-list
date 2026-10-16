# backlink-spam-list：垃圾外链来源库

[English](README.md) · [在线查看](https://jasonzhu.ai/zh/backlink-spam-list)

一份大家共同维护的名单：专门制造或出售垃圾外链的网站，每一条都附有任何人都能在公开网页上核实的证据。在把你的网站提交到某个地方之前，或者发现一批奇怪的外链指向你时，可以先来这里查一下这个域名。

`list.csv` 里现有 **568 条**，大部分是 11 个站群的门户域名，它们都跳转到几个卖外链的店面：

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

最大的一群是 126 个纯数字的 `.xyz` 域名，全部跳转到同一个网站，那个网站提供「删除外链，或者挣到相关外链」的服务，每个页面上都挂着同样的两条 Stripe 收款链接。

## 收什么

| 类别 | 含义 | 需要的证据 |
|---|---|---|
| `link-network` | 同一个人运营的一批站 | 和其他已收录站共用的页面标题、跳转、收款链接或统计账号 |
| `link-seller` | 以卖链接为业 | 它自己页面上的 PBN、DR/DA 套餐、出售客座文章，或者站群跳转过去的店面 |
| `hacked` | 被黑网站里被注入的页面 | 被注入的页面或链接，比如博彩、成人产品的收款链接 |
| `shortener` | 被拿来批量刷「外链」的短链服务 | 网站本身 |

每一条都带着证据和一个任何人都能打开查看的公开网址，以及首次收录和最近核实的日期。工具给出的分数（垃圾分、「SPAM」标记）本身不算证据，这里也不公开。

不收的：出售传权重收录、但本身是真实网站的目录站（那是需要权衡的政策风险，不是站群；用 [backlink-guard](https://github.com/zhuyansen/backlink-guard) 能看到），以及已经打不开的站。

## 举报

[提交举报](../../issues/new?template=report.yml)：填域名、类别、一个网址和它显示了什么。提交后会自动检查，并在 issue 里评论看到了什么：用 backlink-guard 读一遍对方的页面，再看你引用的原文在不在证据页面上。维护者随后回复 `/approve <类别>` 收录，或 `/reject <原因>` 驳回。

## 申诉

如果某一条错了或过时了，比如域名已经换了主人，请[提交申诉](../../issues/new?template=dispute.yml)。维护者会回复 `/remove`（移除）或 `/keep`（保留）。被移除的条目会保留那一行，状态改为 `removed` 并记下是哪个 issue 移除的，历史不会丢。

## 怎么用

`list.csv` 的列：`domain, category, family, evidence, evidence_url, first_listed, last_checked, status, source`。只有状态为 `listed` 的才是当前有效的。

```bash
curl -s https://raw.githubusercontent.com/zhuyansen/backlink-spam-list/main/list.csv | grep ',listed,'
```

[backlink-guard](https://github.com/zhuyansen/backlink-guard) 每次 `vet` 都会读这份名单：已收录的站直接判 avoid，并附上条目里的证据。

## 第一批是怎么找到的

568 个域名，来自 2026-10-16 审查过的外链来源。先用第三方的垃圾分挑出要看哪些站；真正让它们进入名单的，是它们自己页面上显示的东西：和几十个其他域名共用的标题、跳转到卖外链的店面、整个站群共用的收款链接或统计账号，或者标题里就写着 DR、DA、PBN 套餐。已经打不开的站没有收录。

## 许可

脚本用 MIT（[LICENSE](LICENSE)）。名单用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)：可以随便用，注明出处即可。
