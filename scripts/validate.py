from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
root=Path('dist')
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key not in ('href','src') or not value or not value.startswith('/') or value.startswith('//'): continue
            path=root / unquote(urlsplit(value).path).lstrip('/')
            if path.is_dir(): path=path/'index.html'
            assert path.is_file(), f'Missing local link: {value}'
for page in root.rglob('*.html'): Links().feed(page.read_text())
assert 'november-aktion-2026.jpg' in (root/'index.html').read_text()
assert 'november-aktion' in (root/'kontakt/index.html').read_text()
print('14 HTML-Seiten, lokale Links und November-Aktion geprüft.')
