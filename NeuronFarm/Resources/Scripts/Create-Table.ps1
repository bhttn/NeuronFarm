param(
    [Parameter(Mandatory)]
    [string]$CsvPath,

    [string]$OutputPath = "output.md",

    [string]$Title = "CSV Export"
)

# Import CSV
$rows = Import-Csv -Path $CsvPath

if (-not $rows) {
    Write-Error "CSV contains no data."
    exit 1
}

# Extract headers
$headers = $rows[0].PSObject.Properties.Name

# Remove Path column from the table
$headers = $headers | Where-Object { $_ -ne "Path" }

# Build Markdown
$md = @()
$md += "# $Title"
$md += ""
$md += "| " + ($headers -join " | ") + " |"
$md += "| " + (($headers | % { '---' }) -join " | ") + " |"

foreach ($row in $rows) {

    $values = foreach ($h in $headers) {

        if ($h -eq "Name") {
            $name = $row.Name
            $path = $row.Path -replace "\.md$", ""   # drop .md extension
            "[${name}](${path})"
        }
        else {
            ($row.$h -replace "\|", "\`|")
        }
    }

    $md += "| " + ($values -join " | ") + " |"
}

# Write file
Set-Content -Path $OutputPath -Value ($md -join "`n") -Encoding UTF8

Write-Host "Markdown table exported to $OutputPath"