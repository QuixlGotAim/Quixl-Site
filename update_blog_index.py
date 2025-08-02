"""
Quixl Blog Index Generator
This script scans the Blog folder for HTML posts and updates Blog/index.html
Usage: Run from the Quixl-Site directory: python update_blog_index.py
"""
import os
import re
from datetime import datetime

BLOG_DIR = "Blog"
INDEX_PATH = os.path.join(BLOG_DIR, "index.html")

# Get all blog post files (exclude index.html)
posts = [f for f in os.listdir(BLOG_DIR) if f.endswith(".html") and f != "index.html"]

# Sort by date in filename (assumes YYYY-MM-DD at start)
def extract_date_title(filename):
    # Try ISO format first
    match_iso = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.*)\.html", filename)
    if match_iso:
        year, month, day, title = match_iso.groups()
        try:
            date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
        except ValueError:
            date = None
        nz_date = f"{day}-{month}-{year}"
        title = title.replace("-", " ").strip() or nz_date
        return (date, nz_date, title, filename)
    # Try NZ format
    match_nz = re.match(r"(\d{2})-(\d{2})-(\d{4})-(.*)\.html", filename)
    if match_nz:
        day, month, year, title = match_nz.groups()
        try:
            date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
        except ValueError:
            date = None
        nz_date = f"{day}-{month}-{year}"
        title = title.replace("-", " ").strip() or nz_date
        return (date, nz_date, title, filename)
    return (None, filename, filename, filename)

posts_info = [extract_date_title(f) for f in posts]
posts_info = [p for p in posts_info if p[0] is not None]
posts_info.sort(reverse=True)

# Build post list HTML
post_list = ""
for date, nz_date, title, filename in posts_info:
    post_list += f'  <li><a class="Right" href="{filename}">{nz_date}: {title}</a></li>\n'

# Read template and replace marker
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    template = f.read()

new_content = re.sub(r'<!-- BLOG_POST_LIST -->', post_list.strip(), template)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Blog index updated with {len(posts_info)} posts.")
