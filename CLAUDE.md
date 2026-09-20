# ANT Lab Website — Claude Code Instructions

## Core architecture

Routine content is maintained through structured data:

- Members: `_data/people.yml`
- Publications: `_data/publications.yml`
- Homepage News: `_data/news.yml`
- Member photos: `assets/images/people/`

Templates render these files. During routine sync, do not modify HTML/CSS/JS unless explicitly requested.

## General safety

- Use explicit source data as facts.
- Do not invent names, dates, emails, awards, publications, DOI, URLs, PDF paths, status, volume/pages, or other facts.
- Report ambiguity instead of guessing.
- Do not commit/push unless explicitly requested.
- Validate edited YAML and show relevant `git diff`.

Placeholder-only public content such as `XXXX`, `XXXX奖`, `待定`, or `待补充` must not be published.

---

## People

Authoritative source: Tencent Docs `成果收集表`

- file_id: `aQscqvIUVkPI`
- Sheet: `Sheet1`
- sheet_id: `000001`

Columns: 姓名, 学位或职称, 入学/入组年份, 邮箱, 个人博客网址, 研究方向, 教育经历, 发表论文, 获奖情况, 个人照片.

Source of truth: `_data/people.yml`.

Allowed title order:

```yaml
title_order:
  教授: 1
  副教授: 2
  讲师: 3
  博士后: 4
  博士(已毕业): 5
  博士研究生: 6
  硕士(已毕业): 7
  硕士研究生: 8
  本科生: 9
```

Sort by title order, year ascending, Chinese name.

Do not invent English names. Convert Chinese names to standard pinyin (`Given Name + Family Name`) unless ambiguous.

Photos are manually maintained at `assets/images/people/<id>.jpg`; only check whether they exist.

People-page publications contain only venue counts, not titles.

---

## Global Publications

Source of truth: `_data/publications.yml`.

`publications.html` renders structured records.
`assets/js/publications.js` is search/filter only and must not parse citations.

Required fields:

```yaml
- id: "2026-example-paper"
  year: 2026
  venue_group: "IEEE S&P"
  authors: "Author A, Author B, Zhiping Cai"
  title: "Complete paper title"
  venue_short: "IEEE S&P"
  publication_info: "IEEE Symposium on Security and Privacy, 2026."
  pdf: ""
```

Rules:

- `title` and `year` are required.
- `authors` may temporarily be empty.
- `venue_short` may be empty if unknown.
- `venue_group` controls grouping; normally use `venue_short`.
- `pdf` may be empty.
- optional `date` must be explicit and use `YYYY-MM-DD`.
- preserve complete title punctuation, including colons/subtitles.
- never invent missing bibliographic facts.

### Additional venue abbreviation normalization

Use these established/common abbreviations when the source venue is unambiguous:

- Computer Networks -> `Comput. Networks`
- Computers & Security -> `Comput. Secur.`
- IEEE Internet Computing -> `IEEE Internet Comput.`
- Sensors -> `Sensors`
- International Conference on Computer Engineering and Networks -> `CENet`
- 计算机科学与探索 / Journal of Frontiers of Computer Science and Technology -> `JFCST`

Do not invent an acronym when no reliable abbreviation is known.

### Publication display order

The Publications page is **year-first**, matching the reference style.

Required order:

1. year descending (`2026`, then `2025`, then `2024`, ...);
2. within each year, venue groups ordered by `venue_priorities`;
3. all papers from the same `venue_group` must stay contiguous;
4. within the same venue in the same year:
   - explicit date descending when available;
   - otherwise stable title order.

Example:

```text
2026
1. [IEEE S&P] ...
2. [IEEE S&P] ...
3. [USENIX Security] ...
4. [ICML] ...
5. [ICML] ...
6. [AAAI] ...

2025
1. [IEEE S&P] ...
2. [CCS] ...
3. [TIFS] ...
...
```

Do **not** group the page by research category.

`venue_priorities` in `_data/publications.yml` is the authoritative website display order.

It is a site presentation preference, not a claim of universal academic ranking.

When a new venue appears:

- reuse an existing priority if present;
- if priority is unclear, place it conservatively near the end and report it for review.

After every publication sync run:

```bash
python3 scripts/sort_publications.py
```

Deduplicate by DOI when known, otherwise normalized title + year.

Do not remove historical publications merely because they are absent from the current Tencent Sheet.

---

## Homepage News

Source of truth: `_data/news.yml`.

News is sorted **only by event date descending**.

Do not group News by venue, research category, or publication priority.

Only create dated News when the source explicitly supplies the date.
Never substitute today's date for an unknown event date.

Homepage should render:

```liquid
{% assign sorted_news = site.data.news.news | sort: "date" | reverse %}
{% for item in sorted_news limit:6 %}
```

---

## Routine workflows

### 同步课题组成员信息

- read all non-empty Tencent rows;
- update `_data/people.yml`;
- sort correctly;
- recompute People venue counts;
- convert placeholder-only awards to `awards: []`;
- validate YAML;
- check member photos;
- show `git diff -- _data/people.yml`.

### 同步论文与新闻

- read member publication fields;
- semantically extract structured publication records;
- deduplicate;
- update/add `_data/publications.yml`;
- assign/reuse `venue_group`;
- run `python3 scripts/sort_publications.py`;
- recompute affected People venue counts;
- update News only for explicitly dated events;
- validate YAML;
- report added/updated/duplicate/ambiguous records;
- show `git diff -- _data/publications.yml _data/people.yml _data/news.yml`.

### 同步课题组网站

Run People sync, publication sync + sorting, awards, News, YAML validation, photo/path checks, duplicate checks, then show final summary and diff.

---

## Files not to touch during routine sync

Unless explicitly requested, do not modify:

- `index.html`
- `people.html`
- `publications.html`
- `research.html`
- `assets/css/*`
- `assets/js/*`
- `_config.yml`

## Git safety

Unless explicitly requested:

- do not commit;
- do not push;
- do not force-push;
- do not rewrite unrelated files.
