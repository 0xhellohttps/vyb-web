#!/usr/bin/env python3
"""Local preview that resolves URLs the way GitHub Pages does.

`python3 -m http.server` 404s on every internal link in this site, because the
nav links are extensionless (`/pulse`, `/api`) and Pages serves `/pulse` from
`pulse.html`. Previewing with the stock server makes correct links look broken.

    python3 serve.py [port]        # default 8080
"""
import http.server, os, sys

class PagesHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = super().translate_path(path)
        # /pulse -> pulse.html, matching Pages' "pretty URL" resolution.
        if not os.path.exists(local) and not path.endswith('/'):
            html = local + '.html'
            if os.path.isfile(html):
                return html
        return local

    def log_message(self, fmt, *args):  # quiet
        pass

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"vyb-web preview → http://localhost:{port}  (extensionless URLs resolve, as on Pages)")
    http.server.HTTPServer(('', port), PagesHandler).serve_forever()
