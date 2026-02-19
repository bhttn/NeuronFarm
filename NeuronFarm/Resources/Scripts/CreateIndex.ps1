param(
    [string]$RootPath = "."
)

function Get-FrontMatter {
    param([string]$FilePath)

    if (-not (Test-Path $FilePath)) { return "" }

    $lines = Get-Content $FilePath

    return ($lines)
}

function Build-Index {
    param(
        [string]$FolderPath,
        [string]$RootPath,
        [int]$IndentLevel = 0
    )

    $folderName = Split-Path $FolderPath -Leaf
    $indexPath = Join-Path $FolderPath "index.md"

    # Heading level based on depth
    $headingLevel = $IndentLevel + 1
    if ($headingLevel -lt 1) { $headingLevel = 1 }
    if ($headingLevel -gt 6) { $headingLevel = 6 }

    $headingPrefix = "#" * $headingLevel

    # Breadcrumbs
    $relativeToRoot = Resolve-Path -Relative $FolderPath
    $parts = $relativeToRoot -split "[\\/]"
    $breadcrumb = ""
    $pathSoFar = "."

    for ($i = 0; $i -lt $parts.Length; $i++) {
        if ($parts[$i] -eq ".") { continue }
        $pathSoFar = Join-Path $pathSoFar $parts[$i]
        $breadcrumb += "[${parts[$i]}]($pathSoFar/index.md) / "
    }

    $breadcrumb = $breadcrumb.TrimEnd(" / ")

    # Merge front matter file if exists
    $frontMatterFile = Join-Path $FolderPath "$folderName.md"
    $frontMatter = Get-FrontMatter $frontMatterFile

    # Build header
    $content = ""

    if ($frontMatter) {
    foreach ($line in $frontMatter) {
        $content += "$line`n"
    }
    $content += "`n"
    }       
    else {
        $content += "---`n"
        $content += "tags: Index`n"
        $content += "title: $folderName Index`n"
        $content += "categories:`n"
        $content += "---`n"
        $content += "`n"
    }


    $content += "$headingPrefix $folderName`n`n"
    #$content += "**$breadcrumb**`n`n"

    # Markdown files (excluding index.md and folderName.md)
    $mdFiles = Get-ChildItem -Path $FolderPath -Filter *.md -File |
               Where-Object { $_.Name -notin @("index.md", "$folderName.md") }

    foreach ($file in $mdFiles) {
        $relative = "./$($file.Name)"
        $content += "- [$($file.BaseName)]($relative)`n"
    }

    # Subfolders as headings
    $subFolders = Get-ChildItem -Path $FolderPath -Directory

    foreach ($sub in $subFolders) {
        $subHeadingLevel = $IndentLevel + 2
        if ($subHeadingLevel -gt 6) { $subHeadingLevel = 6 }
        $subHeadingPrefix = "#" * $subHeadingLevel

        $relativeFolder = "./$($sub.Name)/index.md"

        $content += "`n$subHeadingPrefix [$($sub.Name)]($relativeFolder)`n"

        $subMdFiles = Get-ChildItem -Path $sub -Filter *.md -File |
               Where-Object { $_.Name -notin @("index.md", "$($sub.Name).md") }

        foreach ($file in $subMdFiles) {
            $relative = "./$($file.Name)"
            $content += "- [$($file.BaseName)]($relative)"
    }
    }

    # Write index.md
    Set-Content -Path $indexPath -Value $content -Encoding UTF8

    # Recurse
    foreach ($sub in $subFolders) {
        Build-Index -FolderPath $sub.FullName -RootPath $RootPath -IndentLevel ($IndentLevel + 1)
    }
}

# Build all folder indexes
Build-Index -FolderPath (Resolve-Path $RootPath) -RootPath (Resolve-Path $RootPath)

Write-Host "All index.md files created with heading-based subfolders, breadcrumbs, and front-matter merging."
