---
WeekName: <% tp.system.prompt("Title", "") %>
Week: <% tp.file.creation_date("ww") %>
Year: <% tp.file.creation_date("YYYY") %>
StartDate: <% tp.date.weekday("YYYY-MM-DD", 1) %>
---
