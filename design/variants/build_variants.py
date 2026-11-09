"""Write local hero previews (preview-hero-a.html / preview-hero-b.html in site-v6/). Preview only: does not touch the Wix pipeline."""
from pathlib import Path
BASE = Path(__file__).resolve().parents[2]
src = (BASE / 'membercloud-site.html').read_text()
head = '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
for key in ('a', 'b'):
    css = (Path(__file__).parent / f'hero-{key}.css').read_text()
    (BASE / f'preview-hero-{key}.html').write_text(head + src + f'\n<style id="hero-variant-{key}">{css}</style>\n')
    print('wrote', f'preview-hero-{key}.html')
