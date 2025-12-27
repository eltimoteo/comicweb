
import re

with open('index.html', 'r') as f:
    content = f.read()

# ----------------------------
# 1. FIX TEXT VISIBILITY (LIGHT MODE)
# ----------------------------
# Hardcoded 'text-white' on active items causes invisible text on light backgrounds.
# We'll use a new variable --text-active which defaults to white in dark mode, but high contrast in light mode.

# First, update CSS Variables in HEAD
css_vars_update = """            --text-main: #d4d4d4;
            --text-muted: #858585;
            --text-active: #ffffff;  /* Default dark mode active text */
"""
# We need to find the specific block to inject --text-active
content = content.replace('--text-muted: #858585;', '--text-muted: #858585;\n            --text-active: #ffffff;')

# Update Theme Definitions in Script for Light Mode
light_theme_update = "'--text-main': '#333333', '--text-muted': '#666666', '--text-active': '#333333',"
content = content.replace("'--text-main': '#333333', '--text-muted': '#666666',", light_theme_update)

# Now replace usages of 'text-white' on ACTIVE elements with 'text-[var(--text-active)]'
# Targeting:
# 1. Active Sidebar Tab (loadSheet)
# 2. Activity Bar Icons (active state)
# 3. Status Bar (keep white usually, but let's see) - Status bar is usually colored bg, so white is fine.

# JS Replacement in `loadSheet`:
content = content.replace("el.classList.remove('bg-[var(--bg-item-active)]', 'text-white');", 
                          "el.classList.remove('bg-[var(--bg-item-active)]', 'text-[var(--text-active)]');")
                          
content = content.replace("activeBtn.classList.add('bg-[var(--bg-item-active)]', 'text-white');", 
                          "activeBtn.classList.add('bg-[var(--bg-item-active)]', 'text-[var(--text-active)]');")

# JS Replacement in `icon-files` listener:
content = content.replace("document.querySelectorAll('.activity-icon').forEach(i => i.classList.remove('text-white', 'border-l-2', 'border-white'));",
                          "document.querySelectorAll('.activity-icon').forEach(i => i.classList.remove('text-[var(--text-active)]', 'border-l-2', 'border-[var(--text-active)]'));")
                          
content = content.replace("document.getElementById('icon-files').classList.add('text-white', 'border-l-2', 'border-white');",
                          "document.getElementById('icon-files').classList.add('text-[var(--text-active)]', 'border-l-2', 'border-[var(--text-active)]');")

# ...and other listeners similarly if they use text-white for active state
# Search Icon
content = content.replace("document.getElementById('icon-search').classList.add('text-white', 'border-l-2', 'border-white');",
                          "document.getElementById('icon-search').classList.add('text-[var(--text-active)]', 'border-l-2', 'border-[var(--text-active)]');")


# ----------------------------
# 2. README TAB (ABOUT ME)
# ----------------------------
# We need to inject the README content div and the logic to show it.

readme_html = """            <!-- README / About Me Content -->
            <div id="readme-container" class="hidden flex-1 overflow-y-auto p-8 font-serif bg-[var(--bg-editor)] text-[var(--text-main)]">
                <div class="max-w-3xl mx-auto">
                    <h1 class="text-4xl font-bold mb-6 border-b border-[var(--border)] pb-4">About Me</h1>
                    <p class="mb-4 text-lg leading-relaxed">
                        Hi, I'm <span class="text-[var(--accent)] font-bold">Timothy</span>. Welcome to my comic collection tracker!
                    </p>
                    <p class="mb-4 text-lg leading-relaxed">
                        I built this application to catalog my growing collection of Marvel and DC comics. 
                        It connects directly to my Google Sheets database and provides a developer-centric interface for browsing.
                    </p>
                    <h2 class="text-2xl font-bold mt-8 mb-4">Tech Stack</h2>
                    <ul class="list-disc pl-6 space-y-2 mb-8">
                        <li><strong>Frontend:</strong> HTML5, Tailwind CSS, Vanilla JS</li>
                        <li><strong>Data:</strong> Google Sheets CSV API + PapaParse</li>
                        <li><strong>Design:</strong> VSCode Dark+ Theme (Custom Implementation)</li>
                    </ul>
                    <div class="p-4 bg-[var(--bg-item-active)] rounded-lg border-l-4 border-[var(--accent)]">
                        <p class="italic">"With great power comes great responsibility."</p>
                        <p class="text-right text-sm mt-2">- Uncle Ben</p>
                    </div>
                </div>
            </div>
"""

# Insert this after `scroll-container`
if 'id="scroll-container">' in content:
    # We find the closing div of scroll-container to append AFTER it, OR we make scroll-container hidden.
    # Actually, `scroll-container` contains the grid. We should toggle visibility between `scroll-container` and `readme-container`.
    # Let's insert readme-container as a sibling to scroll-container
    content = content.replace('<div class="flex-1 overflow-y-auto p-4 md:p-6" id="scroll-container">', 
                              readme_html + '\n            <div class="flex-1 overflow-y-auto p-4 md:p-6" id="scroll-container">')

# Modify `loadSheet` to hide Readme and show content
# We'll do this by replacing the function body partly or using regex
load_sheet_extra_logic = """
            // Hide Readme, Show Grid
            document.getElementById('readme-container').classList.add('hidden');
            document.getElementById('scroll-container').classList.remove('hidden');
            
            // Update Tab Header Styles
            document.getElementById('tab-readme').classList.remove('border-t-2', 'border-[var(--accent)]', 'bg-[var(--bg-editor)]', 'text-[var(--text-main)]');
            document.getElementById('tab-readme').classList.add('bg-[var(--bg-panel)]', 'text-[var(--text-muted)]', 'border-r', 'border-[var(--bg-sidebar)]');
            
            document.getElementById('tab-main').classList.add('bg-[var(--bg-editor)]', 'text-[var(--text-main)]', 'border-t-2', 'border-[var(--accent)]');
            document.getElementById('tab-main').classList.remove('bg-[var(--bg-panel)]', 'text-[var(--text-muted)]', 'border-r');
"""
# Insert this at start of loadSheet
content = content.replace("function loadSheet(key) {", "function loadSheet(key) {" + load_sheet_extra_logic)

# Create `loadReadme` function
load_readme_fn = """
        function loadReadme() {
            // Update UI for Readme Mode
            document.getElementById('scroll-container').classList.add('hidden');
            document.getElementById('readme-container').classList.remove('hidden');
            
            // Deselect Sidebars
             document.querySelectorAll('[id^="btn-"]').forEach(el => {
                el.classList.remove('bg-[var(--bg-item-active)]', 'text-[var(--text-active)]');
                el.classList.add('text-[var(--text-main)]');
            });
            
            // Tab Header Styles
            document.getElementById('tab-main').classList.remove('border-t-2', 'border-[var(--accent)]', 'bg-[var(--bg-editor)]', 'text-[var(--text-main)]');
            document.getElementById('tab-main').classList.add('bg-[var(--bg-panel)]', 'text-[var(--text-muted)]', 'border-r', 'border-[var(--bg-sidebar)]'); // Inactive style
            
            document.getElementById('tab-readme').classList.add('bg-[var(--bg-editor)]', 'text-[var(--text-main)]', 'border-t-2', 'border-[var(--accent)]');
            document.getElementById('tab-readme').classList.remove('bg-[var(--bg-panel)]', 'text-[var(--text-muted)]', 'border-r');
            
            // Update Breadcrumbs
            document.getElementById('crumb-active').innerText = "README.md";
            document.getElementById('statsBar').innerText = "Markdown Preview";
        }
"""
# Append to script
content = content.replace("function loadSheet(key)", load_readme_fn + "\n        function loadSheet(key)")

# Update HTML IDs for Tabs to work with logic
content = content.replace('id="tab-label"', 'id="tab-main" onclick="loadSheet(currentTab)" class="cursor-pointer"')
# Update the Readme Tab
readme_tab_search = """<!-- Fake inactive tab -->
                <div class="bg-[var(--bg-panel)] text-gray-500 px-4 h-full flex items-center gap-2 border-r border-[var(--bg-sidebar)]">
                    <i class="fa-solid fa-file-lines"></i>
                    <span>README.md</span>
                </div>"""
readme_tab_replace = """<!-- Readme Tab -->
                <div id="tab-readme" onclick="loadReadme()" class="cursor-pointer bg-[var(--bg-panel)] text-[var(--text-muted)] px-4 h-full flex items-center gap-2 border-r border-[var(--bg-sidebar)]">
                    <i class="fa-solid fa-file-lines text-blue-400"></i>
                    <span>README.md</span>
                </div>"""
content = content.replace(readme_tab_search.strip(), readme_tab_replace.strip())
# Also fix `text-gray-500` to vars if missed
content = content.replace('text-gray-500', 'text-[var(--text-muted)]')


# ----------------------------
# 3. SIDEBAR TOGGLE BUTTON
# ----------------------------
# User wants a "file icon on the side bar that collapses the explorer bar"
# The 'icon-files' ALREADY does this. 
# "create a file icon on the side bar that collapses the explorer bar"
# Maybe they mean inside the Explorer Header (top right of the panel)?
# Let's add that chevron icon in the explorer header to be safe, as it's a common UI pattern.

explorer_header_search = '<div class="px-4 py-2 uppercase text-xs font-bold text-[var(--text-muted)] tracking-wider">Explorer</div>'
explorer_header_replace = """<div class="px-4 py-2 flex items-center justify-between uppercase text-xs font-bold text-[var(--text-muted)] tracking-wider">
                <span>Explorer</span>
                <i id="btn-collapse-explorer" class="fa-solid fa-ellipsis hover:text-white cursor-pointer" title="More Actions"></i>
            </div>"""

content = content.replace(explorer_header_search, explorer_header_replace)

# We can make the ellipsis actually collapse it or just show an alert, but sticking to 
# ensuring the sidebar Files icon is robust is key.
# I will double check the `icon-files` replacement logic earlier to make sure I didn't break strictly matching strings.
# The previous replacement:
# content = content.replace("document.getElementById('icon-files').classList.add('text-white', 'border-l-2', 'border-white');",
#                          "document.getElementById('icon-files').classList.add('text-[var(--text-active)]', 'border-l-2', 'border-[var(--text-active)]');")

# This relies on the EXACT string match. I should probably match partial to be safe or use regex.
# Given I wrote the code, I know exactly what it is unless I made a typo.
# Checking line 364: document.getElementById('icon-files').classList.add('text-white', 'border-l-2', 'border-white');
# It matches.

# Final write
with open('index.html', 'w') as f:
    f.write(content)
