# Deployment and maintenance

## Primary hosting: Vercel
The Concord House production site is deployed as a static site.

Production alias:
https://concord-house-adils-projects-7b8d0e6c.vercel.app

Recommended Git integration:
- Repository: `AdilKaibaliev/concord-house`
- Production branch: `main`
- Framework preset: Other / static
- Root directory: repository root
- Build command: none
- Output directory: repository root

Once the repository is connected to the existing Vercel project, every push to `main` can deploy automatically.

## Recommended change process
For small approved edits:
1. Update `index.html`.
2. Commit to `main`.
3. Confirm the new Vercel Production deployment.

For larger visual or functional changes:
1. Create a branch such as `update/hero`.
2. Push the changes.
3. Review the Vercel Preview deployment.
4. Merge into `main` only after approval.

## Rollback
Vercel retains prior deployments, so a previous working deployment can be promoted if a new release has a problem. Git history also preserves each committed site version.

## GitHub Pages fallback
The workflow in `.github/workflows/pages.yml` can publish this static repository to GitHub Pages if Pages is enabled in repository settings.
