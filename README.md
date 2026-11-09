# MemberCloud — Marketing Site

Marketing website for **MemberCloud**, a membership and billing platform for
clinics and recurring-membership businesses (dental, veterinary, gym &
wellness, mental health, and general "any membership" businesses). The site
showcases the platform, lets visitors book a demo, and includes an AI-powered
chat widget that can answer product questions in real time.

## Stack

- **Static site generator (Python):** the HTML pages are generated/assembled
  by a set of Python scripts (`build_landings.py`, `blocks.py`, `replica.py`,
  `dd.py`, `apply_design.py`, `make_pricing.py`, `make_demo_contact.py`).
  `build.sh` orchestrates the full build.
- **Hosting:** [Cloudflare Pages](https://pages.cloudflare.com/) (see
  `wrangler.toml`, project `membercloud-review`).
- **Serverless backend:** [Cloudflare Functions](https://developers.cloudflare.com/pages/functions/)
  under `functions/api/` handle:
  - `chat.js` — AI chat widget (Anthropic or OpenAI, selectable via the
    `PROVIDER` env var)
  - `lead.js` — lead capture, email delivery via [Resend](https://resend.com/)
  - `status.js` — health/config check endpoint
- **Frontend:** plain HTML/CSS/JS, no framework or bundler.

All secrets (model provider API keys, Resend API key) are injected as
Cloudflare Pages environment variables/secrets — **never committed to this
repository**.

## Project layout

```
build.sh                  # Orchestrates the full site build
build_landings.py          # Generates the landing pages
blocks.py / replica.py     # Shared page-building blocks/helpers
apply_design.py             # Applies the current visual design system
make_pricing.py             # Generates the pricing page
make_demo_contact.py        # Generates the demo/contact pages
functions/api/               # Cloudflare Functions (chat, lead, status)
functions/lib/shared.js      # Shared helpers for the Functions
chat/                         # Chat widget client code + knowledge base
images/, real/, icons/        # Site media assets
design/                       # Design system assets (CSS/JS)
dist/                          # Build output (generated, gitignored)
```

## Running the build locally

Requirements: Python 3 (no third-party packages needed — the build uses only
the standard library).

```sh
./build.sh
```

This regenerates the landing pages and produces a ready-to-deploy `dist/`
folder (copies of all HTML pages, images, chat assets, `_headers`, and
`robots.txt`). `dist/` is not committed; run the script to produce it.

## Deployment

The site deploys to Cloudflare Pages from the `dist/` output
(`pages_build_output_dir` in `wrangler.toml`). Required secrets, set via
`wrangler pages secret put <NAME> --project-name membercloud-review`:

- `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY` if `PROVIDER = "openai"`)
- `RESEND_API_KEY`

## Notes

- `dist/` is a build artifact — regenerate it with `./build.sh` rather than
  editing it directly.
- `.wrangler/`, `__pycache__/`, and any `.env*` files are intentionally
  excluded from version control (see `.gitignore`).
