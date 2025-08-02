# Quixl Blog Index Generator
# This script scans the Blog folder for HTML posts and updates Blog/index.html
# Usage: Run in PowerShell from the Quixl-Site directory

$blogFolder = "Blog"
$indexPath = "$blogFolder/index.html"

# Get all blog post files (exclude index.html)
$posts = Get-ChildItem -Path $blogFolder -Filter *.html | Where-Object { $_.Name -ne "index.html" }

# Sort by date in filename (assumes YYYY-MM-DD at start)
$posts = $posts | Sort-Object { $_.BaseName }
$posts = $posts | Sort-Object { $_.BaseName } -Descending

# Build post list HTML
$postList = ""
foreach ($post in $posts) {
    $date = $post.BaseName -split "-" | Select-Object -First 3 -Join "-"
    $title = $post.BaseName.Substring($date.Length + 1)
    if ($title) { $title = $title.Replace("-", " ") } else { $title = $date }
    $postList += "    <li><a class=\"Right\" href=\"$($post.Name)\">$date: $title</a></li>`n"
}

# Read template and replace marker
$template = Get-Content $indexPath -Raw
$template = $template -replace "<!-- BLOG_POST_LIST -->", $postList.TrimEnd()

# Write updated index
Set-Content -Path $indexPath -Value $template
Write-Host "Blog index updated with $($posts.Count) posts."
