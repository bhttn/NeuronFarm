---
title: Mains
Cat: 
SubCat: Index
---
```dataview
LIST rows.file.link
FROM "Recipies/Codex"
WHERE contains(Cat, "Mains")
FLATTEN SubCat AS SubCategory
GROUP BY SubCategory
```
[[Recipies]]