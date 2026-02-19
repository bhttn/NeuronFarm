---
*Week <% tp.frontmatter.Week %> <% tp.date.weekday("ddd DD", 1) %> - <% tp.date.weekday("ddd DD MMM YYYY", 7) %>*

<% tp.file.rename("Week " + tp.frontmatter.Week + " - " + tp.frontmatter.WeekName) %>
