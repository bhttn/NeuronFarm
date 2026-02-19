param(
    [string]$RootPath = "C:\Users\ben\OneDrive\Codex\NeuronFarm\NeuronFarm\bōchord\blæd",
    [string]$OutputFile = "index.md"
)

# Build a tree of folders and markdown files
function Build-Tree($path) {
    $node = [ordered]@{
        Name = Split-Path $path -Leaf
        Path = $path
        Files = @()
        Children = @()
    }

    # Add .md files (excluding index.md)
    $mdFiles = Get-ChildItem -Path $path -Filter *.md -File |
               Where-Object { $_.Name -ne "index.md" }

    foreach ($file in $mdFiles) {
        $node.Files += $file
    }

    # Recurse into subfolders
    $subDirs = Get-ChildItem -Path $path -Directory
    foreach ($dir in $subDirs) {
        $node.Children += Build-Tree $dir.FullName
    }

    return $node
}

# Render the tree into markdown
function Render-Tree($node, $indentLevel = 0) {
    $indent = " " * ($indentLevel * 2)
    $output = ""

    # Folder heading (only for root)
    if ($indentLevel -eq 0) {
        $output += "# $($node.Name)`n`n"
    } else {
        $output += "$indent- **$($node.Name)**`n"
    }

    # Files in this folder
    foreach ($file in $node.Files) {
        $relative = Resolve-Path -Relative $file.FullName
        $output += "$indent  - [$($file.BaseName)]($relative)`n"
    }

    # Children
    foreach ($child in $node.Children) {
        $output += Render-Tree $child ($indentLevel + 1)
    }

    return $output
}

# Build and write the index
$tree = Build-Tree (Resolve-Path $RootPath)
$markdown = Render-Tree $tree
Set-Content -Path (Join-Path $RootPath $OutputFile) -Value $markdown -Encoding UTF8

Write-Host "Nested index.md created at $RootPath"
