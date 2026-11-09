"""Apply the maintained design layer to every source page, idempotently."""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
PAGES = ['membercloud-site.html', 'dental.html', 'veterinary.html',
         'gym-wellness.html', 'any-membership.html', 'mental-health.html',
         'privacy.html', 'resources.html', 'pricing.html', 'book-demo.html', 'contact.html']

def apply():
    css = (BASE / 'design/apple-design.css').read_text()
    js = (BASE / 'design/apple-design.js').read_text() + '\n' + (BASE / 'design/accessibility.js').read_text()
    layer = f'<!-- mc-apple-design:start -->\n<style>{css}</style>\n<script>{js}</script>\n<!-- mc-apple-design:end -->'
    for name in PAGES:
        path = BASE / name
        source = path.read_text()
        if name == 'membercloud-site.html':
            source = re.sub(r'<!-- mc-home-hero:start -->[\s\S]*?<!-- mc-home-hero:end -->\s*', '', source)
            source += '\n<!-- mc-home-hero:start -->\n<style>' + (BASE / 'design/home-hero.css').read_text() + '\n' + (BASE / 'design/home-hero-a.css').read_text() + '</style>\n<script>' + (BASE / 'design/home-hero.js').read_text() + '</script>\n<!-- mc-home-hero:end -->\n'
        source = re.sub(r'<!-- mc-apple-design:start -->[\s\S]*?<!-- mc-apple-design:end -->\s*', '', source)
        source = re.sub(r'\s*</body>', lambda m: '\n' + layer + '\n</body>', source) if '</body>' in source else source.rstrip() + '\n' + layer + '\n'
        path.write_text(source)

if __name__ == '__main__':
    apply()
