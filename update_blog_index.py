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
    match = re.match(r"(\d{4}-\d{2}-\d{2})-(.*)\.html", filename)
    if match:
        date_str, title = match.groups()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date = None
        title = title.replace("-", " ").strip() or date_str
        return (date, date_str, title)
    return (None, filename, filename)

posts_info = [extract_date_title(f) for f in posts]
posts_info = [p for p in posts_info if p[0] is not None]
posts_info.sort(reverse=True)

# Build post list HTML
post_list = ""
for date, date_str, title in posts_info:
    post_list += f'    <a class="Right" href="{date_str}-{title.replace(" ", "-")}.html">{date_str}: {title}</a>\n'

# Read template and replace marker
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    template = f.read()

new_content = re.sub(r'<!-- BLOG_POST_LIST -->', post_list.strip(), template)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Blog index updated with {len(posts_info)} posts.")
