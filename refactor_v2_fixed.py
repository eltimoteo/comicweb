
import re

# Read the file
with open('index.html', 'r') as f:
    content = f.read()

# 1. Update CSS Variables Definition (Add missing ones)
# We need to ensure we have vars for all the UI elements to allow global theming
css_vars = """        :root {
            --bg-editor: #1e1e1e;
            --bg-sidebar: #252526;
            --bg-activity: #333333;
            --bg-panel: #2d2d2d;     /* Panel headers, search container */
            --bg-input: #3c3c3c;     /* Dropdowns, Inputs */
            --bg-item-hover: #2a2d2e;
            --bg-item-active: #37373d;
            --border: #3e3e42;
            --accent: #007acc;
            --text-main: #d4d4d4;
            --text-muted: #858585;
            
            /* Syntax Highlighting */
            --keyword: #569cd6;      /* Blue */
            --string: #ce9178;       /* Orange/Brown */
            --function: #dcdcaa;     /* Yellow */
            --comment: #6a9955;      /* Green */
            --number: #b5cea8;       /* Light Green */
            --type: #4ec9b0;         /* Teal */
            --variable: #9cdcfe;     /* Light Blue */
        }"""

content = re.sub(r':root \{[^}]+\}', css_vars, content, flags=re.DOTALL)

# 2. Add Theme Data for the new variables
# We need to update the `themes` object in JS to include these new vars
js_themes = """const themes = {
            'dark-plus': {
                '--bg-editor': '#1e1e1e', '--bg-sidebar': '#252526', '--bg-activity': '#333333', 
                '--bg-panel': '#2d2d2d', '--bg-input': '#3c3c3c', '--bg-item-hover': '#2a2d2e', '--bg-item-active': '#37373d',
                '--border': '#3e3e42', '--accent': '#007acc', '--text-main': '#d4d4d4', '--text-muted': '#858585',
                '--keyword': '#569cd6', '--string': '#ce9178', '--function': '#dcdcaa', '--number': '#b5cea8', '--type': '#4ec9b0', '--variable': '#9cdcfe'
            },
            'light-plus': {
                '--bg-editor': '#ffffff', '--bg-sidebar': '#f3f3f3', '--bg-activity': '#2c2c2c', 
                '--bg-panel': '#f3f3f3', '--bg-input': '#ffffff', '--bg-item-hover': '#e8e8e8', '--bg-item-active': '#007acc33',
                '--border': '#e4e4e4', '--accent': '#007acc', '--text-main': '#333333', '--text-muted': '#666666',
                '--keyword': '#0000ff', '--string': '#a31515', '--function': '#795e26', '--number': '#098658', '--type': '#267f99', '--variable': '#001080'
            },
            'monokai': {
                '--bg-editor': '#272822', '--bg-sidebar': '#1e1f1c', '--bg-activity': '#171814', 
                '--bg-panel': '#1e1f1c', '--bg-input': '#414339', '--bg-item-hover': '#3e3d32', '--bg-item-active': '#75715e',
                '--border': '#1e1f1c', '--accent': '#f92672', '--text-main': '#f8f8f2', '--text-muted': '#75715e',
                '--keyword': '#f92672', '--string': '#e6db74', '--function': '#a6e22e', '--number': '#ae81ff', '--type': '#66d9ef', '--variable': '#fd971f'
            },
            'abyss': {
                '--bg-editor': '#000c18', '--bg-sidebar': '#051336', '--bg-activity': '#102a5f', 
                '--bg-panel': '#0b1c42', '--bg-input': '#223355', '--bg-item-hover': '#112244', '--bg-item-active': '#1e3a6e',
                '--border': '#2d3664', '--accent': '#77085a', '--text-main': '#6688c2', '--text-muted': '#3b5588',
                '--keyword': '#225588', '--string': '#22aa44', '--function': '#ddbb88', '--number': '#d2dfee', '--type': '#9966b8', '--variable': '#77085a'
            },
            'solarized': {
                '--bg-editor': '#fdf6e3', '--bg-sidebar': '#eee8d5', '--bg-activity': '#93a1a1', 
                '--bg-panel': '#e6dfc4', '--bg-input': '#fdf6e3', '--bg-item-hover': '#d5ccb4', '--bg-item-active': '#d3368222',
                '--border': '#d3cbb7', '--accent': '#2aa198', '--text-main': '#586e75', '--text-muted': '#93a1a1',
                '--keyword': '#859900', '--string': '#cb4b16', '--function': '#b58900', '--number': '#2aa198', '--type': '#268bd2', '--variable': '#6c71c4'
            }
        };"""

content = re.sub(r'const themes = \{.*?\};', js_themes, content, flags=re.DOTALL)


# 3. Replace Hardcoded Hexes with CSS Variables in HTML
replacements = {
    'bg-[#1e1e1e]': 'bg-[var(--bg-editor)]',
    'bg-[#252526]': 'bg-[var(--bg-sidebar)]',
    'bg-[#333333]': 'bg-[var(--bg-activity)]',
    'bg-[#3c3c3c]': 'bg-[var(--bg-input)]',  # Header + Inputs
    'bg-[#2d2d2d]': 'bg-[var(--bg-panel)]',
    'bg-[#37373d]': 'bg-[var(--bg-item-active)]',
    'hover:bg-[#2a2d2e]': 'hover:bg-[var(--bg-item-hover)]',
    'border-[#3e3e42]': 'border-[var(--border)]',
    'border-[#252526]': 'border-[var(--bg-sidebar)]',
    'border-[#1e1e1e]': 'border-[var(--bg-editor)]',
    'border-[#454545]': 'border-[var(--border)]',
    'border-black': 'border-[var(--border)]', # Fix tab header bottom border
    'border-[#4e4e4e]': 'border-[var(--border)]',
    'text-[#d4d4d4]': 'text-[var(--text-main)]',
    'text-[#858585]': 'text-[var(--text-muted)]',
    'text-gray-400': 'text-[var(--text-muted)]', # Approximate
    'text-gray-300': 'text-[var(--text-main)]',
    'bg-[#007acc]': 'bg-[var(--accent)]',
    'border-[#007acc]': 'border-[var(--accent)]',
    # Syntax Highlighting Colors
    'text-[#569cd6]': 'text-[var(--keyword)]',
    'text-[#4ec9b0]': 'text-[var(--type)]',
    'text-[#9cdcfe]': 'text-[var(--variable)]',
    'text-[#ce9178]': 'text-[var(--string)]',
    'text-[#b5cea8]': 'text-[var(--number)]'
}

for hex_code, var_code in replacements.items():
    content = content.replace(hex_code, var_code)

# 4. Update JS Logic (Shortcuts, Sidebar Actions, Sort Arrow)
js_logic = """
        document.addEventListener('keydown', (e) => {
            // CMD+F / CTRL+F -> Focus Search
            if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
                e.preventDefault();
                document.getElementById('searchInput').focus();
            }
            // CMD+B / CTRL+B -> Toggle Sidebar (VSCode standard)
            if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
                e.preventDefault();
                document.getElementById('icon-files').click();
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
             // Init Theme (to set initial vars if strict mode)
            const theme = themes['dark-plus'];
            Object.keys(theme).forEach(key => {
                document.documentElement.style.setProperty(key, theme[key]);
            });

            runSplash();
            loadSheet('marvel');

            // --- FUNCTIONAL SIDEBAR ---
            const sidebarExplorer = document.getElementById('sidebar-panel');
            
            // Files Icon -> Toggle Explorer
            document.getElementById('icon-files').addEventListener('click', (e) => {
                const isActive = !sidebarExplorer.classList.contains('hidden');
                document.querySelectorAll('.activity-icon').forEach(i => i.classList.remove('text-white', 'border-l-2', 'border-white'));

                if (isActive) {
                    sidebarExplorer.classList.add('hidden');
                } else {
                    sidebarExplorer.classList.remove('hidden');
                    document.getElementById('icon-files').classList.add('text-white', 'border-l-2', 'border-white');
                }
            });

            // Search Icon -> Focus Search
            document.getElementById('icon-search').addEventListener('click', () => {
                 document.getElementById('searchInput').focus();
                 document.querySelectorAll('.activity-icon').forEach(i => i.classList.remove('text-white', 'border-l-2', 'border-white'));
                 document.getElementById('icon-search').classList.add('text-white', 'border-l-2', 'border-white');
            });
            
            // Git Icon
            document.getElementById('icon-git').addEventListener('click', () => {
                alert("Source Control: No providers registered. (It's a static site!)");
            });

            // Debug Icon
            document.getElementById('icon-debug').addEventListener('click', () => {
                const debugInfo = {
                    currentTab,
                    totalItems: currentData.length,
                    activeTheme: document.getElementById('themeSelect').value
                };
                alert('DEBUG CONTEXT:\\n' + JSON.stringify(debugInfo, null, 2));
            });

            // Settings Icon -> Toggle Modal
            document.getElementById('icon-settings').addEventListener('click', (e) => {
                e.stopPropagation();
                document.getElementById('settings-modal').classList.toggle('hidden');
            });

            // Close modal on outside click
            document.addEventListener('click', (e) => {
                const modal = document.getElementById('settings-modal');
                const btn = document.getElementById('icon-settings');
                if (!modal.contains(e.target) && !btn.contains(e.target)) {
                    modal.classList.add('hidden');
                }
            });

            // Theme Switcher
            document.getElementById('themeSelect').addEventListener('change', (e) => {
                const theme = themes[e.target.value];
                Object.keys(theme).forEach(key => {
                    document.documentElement.style.setProperty(key, theme[key]);
                });
            });

            // Main Listeners
            document.getElementById('searchInput').addEventListener('input', renderComics);
            document.getElementById('readFilter').addEventListener('change', renderComics);
            document.getElementById('sortSelect').addEventListener('change', renderComics);
            document.getElementById('orderBtn').addEventListener('click', () => {
                isDescending = !isDescending;
                renderComics();
            });
        });
"""

# Inject IDs
content = content.replace('class="fa-solid fa-code-branch', 'id="icon-git" class="fa-solid fa-code-branch')
content = content.replace('class="fa-solid fa-bug', 'id="icon-debug" class="fa-solid fa-bug')
content = content.replace('placeholder="Search files (Ctrl+P)"', 'placeholder="Search (Cmd+F)"')

# Full script to write using simple write rather than regex replace to avoid escaping hell
# We will use re.split to protect the surrounding script tags but simpler manual approach 
# is to define the full script and just search/replace the unique block identifier

final_script = r"""<script>
        // --- DATA CONFIG ---
        const sheetConfig = {
            marvel: "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFTPLKwr0aJgqiW3fPIbp5SvHLSDu6mPGnILzw9uMBKWfw7VdNykUY4NLiGNcb4dU3VI7XLkO8iSqX/pub?gid=61223904&single=true&output=csv",
            dc: "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFTPLKwr0aJgqiW3fPIbp5SvHLSDu6mPGnILzw9uMBKWfw7VdNykUY4NLiGNcb4dU3VI7XLkO8iSqX/pub?gid=0&single=true&output=csv",
            others: "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFTPLKwr0aJgqiW3fPIbp5SvHLSDu6mPGnILzw9uMBKWfw7VdNykUY4NLiGNcb4dU3VI7XLkO8iSqX/pub?gid=1684289763&single=true&output=csv"
        };
        
        // --- THEMES ---
        const themes = {
            'dark-plus': {
                '--bg-editor': '#1e1e1e', '--bg-sidebar': '#252526', '--bg-activity': '#333333', 
                '--bg-panel': '#2d2d2d', '--bg-input': '#3c3c3c', '--bg-item-hover': '#2a2d2e', '--bg-item-active': '#37373d',
                '--border': '#3e3e42', '--accent': '#007acc', '--text-main': '#d4d4d4', '--text-muted': '#858585',
                '--keyword': '#569cd6', '--string': '#ce9178', '--function': '#dcdcaa', '--number': '#b5cea8', '--type': '#4ec9b0', '--variable': '#9cdcfe'
            },
            'light-plus': {
                '--bg-editor': '#ffffff', '--bg-sidebar': '#f3f3f3', '--bg-activity': '#2c2c2c', 
                '--bg-panel': '#f3f3f3', '--bg-input': '#ffffff', '--bg-item-hover': '#e8e8e8', '--bg-item-active': '#007acc33',
                '--border': '#e4e4e4', '--accent': '#007acc', '--text-main': '#333333', '--text-muted': '#666666',
                '--keyword': '#0000ff', '--string': '#a31515', '--function': '#795e26', '--number': '#098658', '--type': '#267f99', '--variable': '#001080'
            },
            'monokai': {
                '--bg-editor': '#272822', '--bg-sidebar': '#1e1f1c', '--bg-activity': '#171814', 
                '--bg-panel': '#1e1f1c', '--bg-input': '#414339', '--bg-item-hover': '#3e3d32', '--bg-item-active': '#75715e',
                '--border': '#1e1f1c', '--accent': '#f92672', '--text-main': '#f8f8f2', '--text-muted': '#75715e',
                '--keyword': '#f92672', '--string': '#e6db74', '--function': '#a6e22e', '--number': '#ae81ff', '--type': '#66d9ef', '--variable': '#fd971f'
            },
            'abyss': {
                '--bg-editor': '#000c18', '--bg-sidebar': '#051336', '--bg-activity': '#102a5f', 
                '--bg-panel': '#0b1c42', '--bg-input': '#223355', '--bg-item-hover': '#112244', '--bg-item-active': '#1e3a6e',
                '--border': '#2d3664', '--accent': '#77085a', '--text-main': '#6688c2', '--text-muted': '#3b5588',
                '--keyword': '#225588', '--string': '#22aa44', '--function': '#ddbb88', '--number': '#d2dfee', '--type': '#9966b8', '--variable': '#77085a'
            },
            'solarized': {
                '--bg-editor': '#fdf6e3', '--bg-sidebar': '#eee8d5', '--bg-activity': '#93a1a1', 
                '--bg-panel': '#e6dfc4', '--bg-input': '#fdf6e3', '--bg-item-hover': '#d5ccb4', '--bg-item-active': '#d3368222',
                '--border': '#d3cbb7', '--accent': '#2aa198', '--text-main': '#586e75', '--text-muted': '#93a1a1',
                '--keyword': '#859900', '--string': '#cb4b16', '--function': '#b58900', '--number': '#2aa198', '--type': '#268bd2', '--variable': '#6c71c4'
            }
        };

        let currentData = [];
        let currentTab = 'marvel';
        let isDescending = false;

        // --- SPLASH SCREEN LOGIC ---
        async function runSplash() {
            const terminal = document.getElementById('terminal-text');
            const footer = document.getElementById('splash-footer');
            const commands = [
                "> npm install comic-db",
                "[SUCCESS] Installed 142 packages in 0.4s",
                "> npm run dev",
                "> Server ready at localhost:3000..."
            ];

            for (const cmd of commands) {
                const p = document.createElement('div');
                p.className = cmd.startsWith(">") ? "text-white" : "text-gray-400 pl-4";
                terminal.appendChild(p);
                
                // Typing effect for commands
                if (cmd.startsWith(">")) {
                    p.innerHTML = "> <span class='cursor'></span>";
                    const text = cmd.substring(2);
                    for (let i = 0; i < text.length; i++) {
                        p.querySelector('span').textContent = text.substring(0, i + 1); // Remove cursor for now or keep it?
                        p.innerHTML = `> ${text.substring(0, i+1)}<span class='cursor'></span>`;
                        await new Promise(r => setTimeout(r, 20));
                    }
                    p.querySelector('.cursor').remove();
                } else {
                    p.innerText = cmd;
                    await new Promise(r => setTimeout(r, 150));
                }
                await new Promise(r => setTimeout(r, 100)); // Faster startup
            }
            
            footer.classList.remove('hidden');
            setTimeout(() => {
                const splash = document.getElementById('splash');
                splash.style.opacity = '0';
                splash.style.transition = 'opacity 0.4s';
                setTimeout(() => splash.remove(), 400);
            }, 600);
        }

        document.addEventListener('keydown', (e) => {
            // CMD+F / CTRL+F -> Focus Search
            if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
                e.preventDefault();
                document.getElementById('searchInput').focus();
            }
             // CMD+P / CTRL+P -> Focus Search (User habit)
            if ((e.metaKey || e.ctrlKey) && e.key === 'p') {
                e.preventDefault();
                document.getElementById('searchInput').focus();
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
             // Init Theme (to set initial vars if strict mode)
            const theme = themes['dark-plus'];
            Object.keys(theme).forEach(key => {
                document.documentElement.style.setProperty(key, theme[key]);
            });
            
            runSplash();
            loadSheet('marvel');

            // --- FUNCTIONAL SIDEBAR ---
            const sidebarExplorer = document.getElementById('sidebar-panel');
            
            // Files Icon -> Toggle Explorer
            document.getElementById('icon-files').addEventListener('click', (e) => {
                const isActive = !sidebarExplorer.classList.contains('hidden');
                document.querySelectorAll('.activity-icon').forEach(i => i.classList.remove('text-white', 'border-l-2', 'border-white'));

                if (isActive) {
                    sidebarExplorer.classList.add('hidden');
                } else {
                    sidebarExplorer.classList.remove('hidden');
                    document.getElementById('icon-files').classList.add('text-white', 'border-l-2', 'border-white');
                }
            });

            // Search Icon -> Focus Search
            document.getElementById('icon-search').addEventListener('click', () => {
                 document.getElementById('searchInput').focus();
                 document.querySelectorAll('.activity-icon').forEach(i => i.classList.remove('text-white', 'border-l-2', 'border-white'));
                 document.getElementById('icon-search').classList.add('text-white', 'border-l-2', 'border-white');
            });
            
            // Git Icon
            document.getElementById('icon-git').addEventListener('click', () => {
                alert("Source Control: No providers registered. (It's a static site!)");
            });

            // Debug Icon
            document.getElementById('icon-debug').addEventListener('click', () => {
                const debugInfo = {
                    currentTab,
                    totalItems: currentData.length,
                    activeTheme: document.getElementById('themeSelect').value
                };
                alert('DEBUG CONTEXT:\\n' + JSON.stringify(debugInfo, null, 2));
            });

            // Settings Icon -> Toggle Modal
            document.getElementById('icon-settings').addEventListener('click', (e) => {
                e.stopPropagation();
                document.getElementById('settings-modal').classList.toggle('hidden');
            });

            // Close modal on outside click
            document.addEventListener('click', (e) => {
                const modal = document.getElementById('settings-modal');
                const btn = document.getElementById('icon-settings');
                if (!modal.contains(e.target) && !btn.contains(e.target)) {
                    modal.classList.add('hidden');
                }
            });

            // Theme Switcher
            document.getElementById('themeSelect').addEventListener('change', (e) => {
                const theme = themes[e.target.value];
                Object.keys(theme).forEach(key => {
                    document.documentElement.style.setProperty(key, theme[key]);
                });
            });

            // Main Listeners
            document.getElementById('searchInput').addEventListener('input', renderComics);
            document.getElementById('readFilter').addEventListener('change', renderComics);
            document.getElementById('sortSelect').addEventListener('change', renderComics);
            document.getElementById('orderBtn').addEventListener('click', () => {
                isDescending = !isDescending;
                renderComics();
            });
        });

        function loadSheet(key) {
            currentTab = key;
            const grid = document.getElementById('comicGrid');

            // Update Active State in Sidebar
            document.querySelectorAll('[id^="btn-"]').forEach(el => {
                el.classList.remove('bg-[var(--bg-item-active)]', 'text-white');
                el.classList.add('text-[var(--text-main)]');
            });
            const activeBtn = document.getElementById(`btn-${key}`);
            activeBtn.classList.add('bg-[var(--bg-item-active)]', 'text-white');
            activeBtn.classList.remove('text-[var(--text-main)]');
            
            // Update Breadcrumb & Tab (Also update icon color based on JS/JSON)
            const labels = { marvel: 'marvel_comics.js', dc: 'dc_universe.js', others: 'indie_reads.json' };
            document.getElementById('crumb-active').innerText = labels[key];
            document.getElementById('tab-label').querySelector('span').innerText = labels[key];

            grid.innerHTML = '';
            document.getElementById('loading').classList.remove('hidden');

            Papa.parse(sheetConfig[key], {
                download: true,
                header: true,
                complete: function (results) {
                    currentData = results.data;
                    document.getElementById('loading').classList.add('hidden');
                    renderComics();
                }
            });
        }

        function renderComics() {
            const grid = document.getElementById('comicGrid');
            const search = document.getElementById('searchInput').value.toLowerCase();
            const filter = document.getElementById('readFilter').value;
            const sortMode = document.getElementById('sortSelect').value;

            // Update Sort UI Indication
             const orderBtn = document.getElementById('orderBtn');
            orderBtn.innerHTML = isDescending 
                ? `<i class="fa-solid fa-arrow-down-z-a"></i> toggle: desc` 
                : `<i class="fa-solid fa-arrow-down-a-z"></i> toggle: asc`;

            grid.innerHTML = '';

            const filtered = currentData.filter(row => {
                if (!row.TITLE) return false;
                const textMatch = (row.TITLE+row.WRITER+row.CHARACTER).toLowerCase().includes(search);
                const isRead = (row.READ || '').toUpperCase() === 'TRUE';
                if (filter === 'read' && !isRead) return false;
                if (filter === 'unread' && isRead) return false;
                return textMatch;
            });

            // Sort logic
            filtered.sort((a, b) => {
                let res = 0;
                if (sortMode === 'title') res = (a.TITLE || '').localeCompare(b.TITLE || '');
                else if (sortMode === 'year') {
                    const getYear = s => (s || '').match(/\\d{4}/) ? parseInt((s || '').match(/\\d{4}/)[0]) : 0;
                    res = getYear(a.PUBLISH) - getYear(b.PUBLISH);
                }
                else if (sortMode === 'rating') res = (parseFloat(a.RATING) || -1) - (parseFloat(b.RATING) || -1);
                
                return isDescending ? -res : res;
            });

            document.getElementById('statsBar').innerText = `Objects: ${filtered.length}`;

            filtered.forEach(comic => {
                const isRead = (comic.READ || '').toUpperCase() === 'TRUE';
                
                // Code Block Card Style
                const div = document.createElement('div');
                div.className = "vscode-card p-0 border-l-[3px] border-[var(--accent)] hover:border-white transition group relative overflow-hidden";
                div.style.backgroundColor = "var(--bg-sidebar)"; 
                
                if(currentTab === 'marvel') div.style.borderColor = "var(--function)";
                if(currentTab === 'dc') div.style.borderColor = "var(--keyword)"; 

                div.innerHTML = `
                    ${comic.IMAGE ? 
                        `<div class="h-32 overflow-hidden border-b" style="border-color: var(--border)">
                            <img src="${comic.IMAGE}" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition">
                        </div>` : ''
                    }
                    
                    <div class="p-3 font-mono text-xs">
                        <div style="color: var(--keyword)" class="mb-1">class <span style="color: var(--type)">${(comic.TITLE || '').replace(/\\s+/g, '')}</span> {</div>
                        
                        <div class="pl-4 ml-1" style="border-left: 1px solid var(--border)">
                            <div><span style="color: var(--variable)">author</span>: <span style="color: var(--string)">"${comic.WRITER}"</span>;</div>
                            <div><span style="color: var(--variable)">year</span>: <span style="color: var(--number)">${(comic.PUBLISH || '').match(/\\d{4}/)?.[0] || 'null'}</span>;</div>
                            <div><span style="color: var(--variable)">read</span>: <span style="color: var(--keyword)">${isRead}</span>;</div>
                            ${comic.RATING ? `<div><span style="color: var(--variable)">rating</span>: <span style="color: var(--number)">${comic.RATING}</span>;</div>` : ''}
                        </div>
                        
                        <div style="color: var(--keyword)" class="mt-1">}</div>
                    </div>
                    
                    <!-- Hover Action -->
                    ${comic.LINK ? 
                    `<a href="${comic.LINK}" target="_blank" class="absolute top-2 right-2 px-2 py-1 bg-[#007acc] text-white text-xs opacity-0 group-hover:opacity-100 transition" style="background-color: var(--accent)">
                        <i class="fa-solid fa-external-link-alt"></i>
                    </a>` : ''}
                `;
                grid.appendChild(div);
            });
        }
    </script>"""

# Using regex replace with DOTALL to ensure we span multiple lines
# We need to escape backslashes in the replacement string for regex to work, 
# but since we are using 'raw' string r"" in python it handles most, 
# except groups. `re.sub` usually treats groups.
# A safer way avoiding regex replace for the script block:
parts = re.split(r'<script>\s*// --- DATA CONFIG ---', content)
if len(parts) > 1:
    new_content = parts[0] + final_script + '</body>\n</html>'
    with open('index.html', 'w') as f:
        f.write(new_content)
else:
    # Fallback to direct write if split fails (shouldn't happen given file content)
    print("Split failed, checking file integrity.")
