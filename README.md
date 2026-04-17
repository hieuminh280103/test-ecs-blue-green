# test-ecs-blue-green-app

PoC app repo: **`.github/workflows/deploy.yml`** (`CD — ECR & CodePipeline`) — `validate-version` → **deploy-backend** and **deploy-frontend** in parallel (same pattern as **`template.yml`**), one semver tag for both, no `:latest`.

- Run: **Actions** → **CD — ECR & CodePipeline** → enter **version**.
- Config: [docs/GITHUB_ACTIONS_SETUP.md](docs/GITHUB_ACTIONS_SETUP.md).
