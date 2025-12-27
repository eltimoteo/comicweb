
# Repair Script to fix the major crash
with open('index.html', 'r') as f:
    content = f.read()

# 1. Fix the ID reference in JS
# content has: document.getElementById('tab-label').querySelector('span').innerText = labels[key];
# needs: document.getElementById('tab-main').querySelector('span').innerText = labels[key];

content = content.replace(
    "document.getElementById('tab-label').querySelector('span').innerText = labels[key];", 
    "document.getElementById('tab-main').querySelector('span').innerText = labels[key];"
)

# 2. Fix the double class attribute in HTML
# <div id="tab-main" onclick="loadSheet(currentTab)" class="cursor-pointer" class="bg-[var(--bg-editor)] ...
# We want to merge them into one class attribute.
bad_html_tag = 'id="tab-main" onclick="loadSheet(currentTab)" class="cursor-pointer" class="bg-[var(--bg-editor)]'
good_html_tag = 'id="tab-main" onclick="loadSheet(currentTab)" class="cursor-pointer bg-[var(--bg-editor)]'

content = content.replace(bad_html_tag, good_html_tag)

with open('index.html', 'w') as f:
    f.write(content)
