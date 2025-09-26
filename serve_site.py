import http.server
import socketserver
import os
import webbrowser

PORT = 8000
DEFAULT_SITE_DIR = "site"

# Try to find a site folder automatically
def find_site_dir():
    # 1. Check default "site"
    if os.path.isdir(DEFAULT_SITE_DIR):
        return DEFAULT_SITE_DIR
    
    # 2. Look for any folder with index.html inside
    for entry in os.listdir("."):
        full_path = os.path.join(entry, "index.html")
        if os.path.isdir(entry) and os.path.isfile(full_path):
            return entry
    
    return None

SITE_DIR = find_site_dir()

if SITE_DIR is None:
    raise FileNotFoundError(
        "No built site found. Please run 'mkdocs build --clean' first."
    )

print(f"Using site directory: {SITE_DIR}")
os.chdir(SITE_DIR)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Serving docs at {url}")
    webbrowser.open(url)  # auto-open browser
    httpd.serve_forever()
