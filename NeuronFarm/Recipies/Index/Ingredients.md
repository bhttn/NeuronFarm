---
title: Ingredients
Cat:
SubCat: Index
---
```dataview
LIST rows.file.link
FROM "Recipies/Codex"
WHERE contains(Cat, "Ingredients")
FLATTEN SubCat AS SubCategory
GROUP BY SubCategory
```
[[Recipies]]