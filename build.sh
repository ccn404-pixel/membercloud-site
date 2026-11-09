#!/bin/sh
# Regenerates the landing pages and the deploy folder. Run from site-v6/.
set -e
python3 -I build_landings.py
rm -rf dist && mkdir -p dist/images dist/chat
cp membercloud-site.html dist/index.html
cp dental.html veterinary.html gym-wellness.html any-membership.html mental-health.html privacy.html dist/
cp -R real dist/real
cp images/logo-horizontal.png images/mark-white.png dist/images/
cp chat/chat.js dist/chat/
printf '/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n' > dist/_headers
printf 'User-agent: *\nDisallow: /\n' > dist/robots.txt
echo "dist ready: $(du -sh dist | cut -f1)"
