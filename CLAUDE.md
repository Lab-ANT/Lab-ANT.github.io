# ANT Lab Website — Claude Code Instructions

## Project

This repository is the ANT Lab website hosted with GitHub Pages/Jekyll.

The People page is data-driven:

- Member data: `_data/people.yml`
- People page template: `people.html`
- People page CSS: `assets/css/people.css`
- Member photos: `assets/images/people/`

Do not manually duplicate member records inside `people.html`.

---

## People Sync Source

The authoritative member-information source is Tencent Docs.

- Document name: 成果收集表
- file_id: `aQscqvIUVkPI`
- Sheet name: `Sheet1`
- sheet_id: `000001`
- Document type: Tencent online Sheet (not SmartSheet)

Use the configured `tencent-docs` MCP connection to read it.

The first 10 columns are:

1. 姓名
2. 学位或职称
3. 入学/入组年份
4. 邮箱
5. 个人博客网址(没有则填无)
6. 研究方向
7. 教育经历(可以不填)
8. 发表论文(没有则填无)
9. 获奖情况(没有则填无)
10. 个人照片

Ignore blank rows.

---

## Photo Handling

Tencent Sheet MCP cannot read JPG images inserted with the Sheet's built-in image insertion feature.

Therefore:

- Do not treat an unreadable photo cell as an error.
- Do not attempt to modify the Tencent Sheet to work around this.
- Photos are manually placed in `assets/images/people/`.
- Generate the expected filename from the English-name ID:
  - 罗梦轩 -> Mengxuan Luo -> `mengxuan-luo.jpg`
- Store that filename in the member's `photo` field.
- Never invent a different photo extension unless the actual repository file uses it.

---

## Allowed Titles and Ordering

The only allowed Chinese title/status values are:

1. 教授
2. 副教授
3. 讲师
4. 博士后
5. 博士(已毕业)
6. 博士研究生
7. 硕士(已毕业)
8. 硕士研究生
9. 本科生

The YAML must preserve:

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

Sort `people` by:

1. `title_order`
2. `year` ascending (earlier joining/enrollment year first)
3. `name_zh` when year is equal

If a title is not in the allowed list, do not guess. Report it for manual confirmation.

---

## Field Conversion Rules

### name_zh

Copy the Tencent Sheet value exactly.

### name_en

Convert the Chinese personal name to standard pinyin in:

`Given Name + Family Name`

Example:

`罗梦轩 -> Mengxuan Luo`

Rules:

- capitalize normally;
- no tone marks;
- family name last;
- do not invent an unrelated English given name;
- if pronunciation is genuinely ambiguous, flag it for manual confirmation.

### id

Generate from `name_en`:

- lowercase;
- spaces become hyphens.

Example:

`Mengxuan Luo -> mengxuan-luo`

### title_zh

Copy exactly from Tencent Docs.

### title_en

Use only this mapping:

- 教授 -> Professor
- 副教授 -> Associate Professor
- 讲师 -> Lecturer
- 博士后 -> Postdoctoral Researcher
- 博士(已毕业) -> Ph.D.
- 博士研究生 -> Ph.D. Student
- 硕士(已毕业) -> Master's Degree
- 硕士研究生 -> Master's Student
- 本科生 -> Undergraduate Student

Do not freely rewrite these labels.

### year

Read directly from `入学/入组年份`.

It must not be inferred from education history.

### email

Copy exactly from Tencent Docs.

Do not correct, normalize, or guess an email address.

### homepage

Convert `无` or blank to:

```yaml
homepage: ""
```

Otherwise preserve the provided URL.

### research

Preserve Chinese research interests and create a faithful English translation.

Example:

```yaml
research:
  zh:
    - "具身智能安全"
  en:
    - "Embodied AI Safety"
```

If the source contains several interests separated by Chinese/English commas, semicolons, slashes, or line breaks, split them into separate list items when unambiguous.

Do not add research areas not present in the source.

### education

Split distinct education entries into separate items.

Use:

```yaml
education:
  - zh: "..."
    en: "..."
```

Allowed normalization:

- punctuation;
- spacing;
- faithful English translation;
- 至今 -> Present.

Never change or invent:

- dates;
- university;
- college/school;
- degree/status.

If blank:

```yaml
education: []
```

### publications

If source is `无` or blank:

```yaml
publications: []
```

Otherwise split clearly separate entries.

Do not search the internet or infer publications from the member's name.

### awards

If source is `无` or blank:

```yaml
awards: []
```

Otherwise split clearly separate awards.

Do not invent or web-search awards.

### photo

Set to:

`<id>.jpg`

unless an existing repository photo for that member uses a different extension.

---

## Expected Member Schema

```yaml
people:
  - id: "mengxuan-luo"
    name_zh: "罗梦轩"
    name_en: "Mengxuan Luo"

    title_zh: "博士研究生"
    title_en: "Ph.D. Student"
    year: 2025

    email: "luomengxuan21a@nudt.edu.cn"
    homepage: ""

    research:
      zh:
        - "具身智能安全"
      en:
        - "Embodied AI Safety"

    education:
      - zh: "2021.09–2025.06 国防科技大学计算机学院，学士"
        en: "2021.09–2025.06 B.S., College of Computer Science and Technology, National University of Defense Technology"

    publications: []
    awards: []

    photo: "mengxuan-luo.jpg"
```

---

## "同步课题组成员信息" Workflow

When the user asks to "同步课题组成员信息" or clearly requests a People-data sync:

1. Read the Tencent Sheet through `tencent-docs` MCP.
2. Read all member rows needed to obtain the complete current dataset.
3. Ignore the unreadable image-object content in column 10.
4. Convert records using all rules in this file.
5. Replace the `people` dataset in `_data/people.yml` with the current authoritative records from Tencent Docs.
6. Preserve `title_order` exactly.
7. Sort records using the required ordering.
8. Validate that `_data/people.yml` parses as valid YAML.
9. Check whether each expected `assets/images/people/<photo>` file exists and report missing photos; do not fabricate image files.
10. Show `git diff -- _data/people.yml`.

Unless the user explicitly asks otherwise:

- do not modify Tencent Docs;
- do not modify `people.html`;
- do not modify CSS;
- do not modify `_config.yml`;
- do not modify unrelated files;
- do not commit;
- do not push;
- do not force-push;
- do not web-search member information.

If source data is missing, ambiguous, or inconsistent, preserve known facts and report the issue rather than guessing.

---

## Website Rendering

`people.html` reads from `site.data.people.people` using Jekyll/Liquid.

Do not reintroduce hard-coded member entries in HTML.

When changing People data, prefer changes only to `_data/people.yml` unless the user explicitly requests a design/template change.
