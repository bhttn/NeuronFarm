---
title: Baking
Cat:
SubCat: Index
---
```dataview
LIST rows.file.link
FROM "Recipies/Codex" 
WHERE contains(Cat, "Baking")
FLATTEN SubCat AS SubCategory
GROUP BY SubCategory
```

[[Recipies]]

