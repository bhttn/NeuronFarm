---
tags:
title: Typst
categories:
  - Wizardry
---
# Overview
[Typst Documentation](https://typst.app/docs)

Typst is a markup-based typesetting system that combines powerful automation and high-quality typography with speed and ease of use. This makes it suitable for documents of any complexity. Typst is a great alternative to both word processors and LaTeX.

# Guides
## Templates
[Typst Template for Pandoc](https://imaginarytext.ca/posts/2025/typst-templates-for-pandoc/)
## PDF

```PowerShell
Pandoc .\Untitled.md -o .\Test.pdf --pdf-engine=typst -V template=./article.typ
```

https://www.reddit.com/r/typst/comments/1odtf6h/does_typst_work_with_pandoc/
## Epub

https://github.com/alexmodrono/typst-pandoc#building-with-the-makefile

```PowerShell
pandoc .\Untitled.md -o .\Test.epub --to=epub3 --split-level=1
```

## Invoice Maker
Generate beautiful invoices from a simple data record

https://github.com/ad-si/invoice-maker