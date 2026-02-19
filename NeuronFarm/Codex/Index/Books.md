
## Notes

```dataview
TABLE Author
FROM "Codex/Books" AND #Notes 
SORT Author, Title
```

## Reading List

```dataview
TABLE Author, EndDate AS "End Date"
FROM "Codex/Books"
WHERE StartDate
SORT StartDate
```

## Books

```dataview
TABLE Author
FROM "Codex/Books"
SORT Author, Title
```