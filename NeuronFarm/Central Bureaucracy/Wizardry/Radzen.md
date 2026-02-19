## Setup
[Get Started](https://www.radzen.com/documentation/blazor/get-started/#installation)

### Installation
`dotnet add package Radzen.Blazor`
### Import Namespaces
`_Imports.razor`
```
@using Radzen
@using Radzen.Blazor
```

### Theme
`_Host.cshtml` (server-side Blazor) or `wwwroot/index.html` (client-side WebAssembly Blazor)

**Bootstrap**
```
<link rel="stylesheet" href="_content/Radzen.Blazor/css/default.css">
```

### JavaScript
`_Host.cshtml` (server-side Blazor) or `wwwroot/index.html` (WebAssembly Blazor)
