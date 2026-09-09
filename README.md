# Concord House / Ынтымак Ордосу

Production repository for the Concord House interactive website.

## Production
Vercel project: `concord-house`

Current production alias:
https://concord-house-adils-projects-7b8d0e6c.vercel.app

## Update workflow
1. Make changes in this repository or prepare them with ChatGPT.
2. Commit changes to `main`.
3. Vercel can be connected to this repository so pushes to `main` become Production deployments.
4. For larger changes, use a feature branch and Vercel Preview before merging to `main`.

## Structure
- `index.html` — self-contained production site, including the current Concord House branding assets.
- `vercel.json` — static hosting configuration.
- `DEPLOYMENT.md` — deployment and maintenance notes.
- `.github/workflows/pages.yml` — optional GitHub Pages fallback deployment.

The repository intentionally keeps the production page self-contained to reduce missing-asset failures and make rollback straightforward.
