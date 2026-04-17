# GitHub Actions — deploy to ECS via CodePipeline / CodeDeploy

Workflow: **`.github/workflows/deploy.yml`** — name in UI: **`CD — ECR & CodePipeline`** (same layout as **`template.yml`**: `validate-version` → parallel **deploy-backend** / **deploy-frontend**).  
Trigger: **`workflow_dispatch`** — input **version** (semver `v1.2.3` or `1.2.3`); **same tag** for both backend and frontend images on their respective ECR repositories.

- Does **not** push a `latest` tag to ECR — only the single tag you entered.
- If that tag already exists on a repository, the corresponding job fails (avoids accidental overwrites).
- After push: build CodeDeploy bundle → upload to S3 → `StartPipelineExecution`.

## 1. AWS: Terraform outputs + IAM role (OIDC)

IAM **OIDC provider** và **deploy role** cho GitHub Actions **không** do Terraform trong `test-ecs-blue-green` tạo — tạo thủ công theo [`test-ecs-blue-green/docs/GITHUB_OIDC_MANUAL_SETUP.md`](../../test-ecs-blue-green/docs/GITHUB_OIDC_MANUAL_SETUP.md). Sau đó đặt GitHub variable `AWS_ROLE_TO_ASSUME` = ARN role bạn đã tạo (ví dụ `arn:aws:iam::123456789012:role/<project_name>-gha-deploy`).

After `terraform apply` in `test-ecs-blue-green`, note:

| Output | Used as |
|--------|---------|
| _(manual)_ IAM role ARN | GitHub variable `AWS_ROLE_TO_ASSUME` |
| `gha_s3_bucket` | `GHA_S3_BUCKET` |
| `gha_s3_object_key_backend` | `GHA_S3_OBJECT_KEY_BACKEND` |
| `gha_s3_object_key_frontend` | `GHA_S3_OBJECT_KEY_FRONTEND` |
| `codepipeline_name_backend` | `CODEPIPELINE_NAME_BACKEND` |
| `codepipeline_name_frontend` | `CODEPIPELINE_NAME_FRONTEND` |
| `ecr_repository_url_backend` | repo name only for `ECR_REPOSITORY_BACKEND` (last segment of URL) |
| `ecr_repository_url_frontend` | idem → `ECR_REPOSITORY_FRONTEND` |
| `ecs_task_definition_family_backend` | `TASK_DEFINITION_FAMILY_BACKEND` |
| `ecs_task_definition_family_frontend` | `TASK_DEFINITION_FAMILY_FRONTEND` |

Task definition families match `${project_name}-be` / `${project_name}-fe` (e.g. `blue-green-demo-be`); use the Terraform outputs above instead of guessing.

Container names must match Terraform: `container_name_backend` / `container_name_frontend` (defaults `backend` / `frontend`).

## 2. GitHub repository variables

**Settings → Secrets and variables → Actions → Variables** (same for all workflows unless you use Environments):

| Variable | Example |
|----------|---------|
| `AWS_ACCOUNT_ID` | (recommended) `123456789012` — same as `template.yml`; if unset, the workflow uses `sts get-caller-identity` |
| `AWS_ROLE_TO_ASSUME` | `arn:aws:iam::123456789012:role/blue-green-demo-gha-deploy` |
| `AWS_REGION` | `us-east-1` |
| `ECR_REPOSITORY_BACKEND` | `blue-green-app-be` |
| `ECR_REPOSITORY_FRONTEND` | `blue-green-app-fe` |
| `TASK_DEFINITION_FAMILY_BACKEND` | `blue-green-demo-be` |
| `TASK_DEFINITION_FAMILY_FRONTEND` | `blue-green-demo-fe` |
| `CONTAINER_NAME_BACKEND` | `backend` |
| `CONTAINER_NAME_FRONTEND` | `frontend` |
| `CONTAINER_PORT` | `80` |
| `GHA_S3_BUCKET` | from `gha_s3_bucket` |
| `GHA_S3_OBJECT_KEY_BACKEND` | from `gha_s3_object_key_backend` |
| `GHA_S3_OBJECT_KEY_FRONTEND` | from `gha_s3_object_key_frontend` |
| `CODEPIPELINE_NAME_BACKEND` | from `codepipeline_name_backend` |
| `CODEPIPELINE_NAME_FRONTEND` | from `codepipeline_name_frontend` |

No secrets are required if you use OIDC only.

## 3. GitHub Environments (optional)

You can attach **Environment** `production` / `test` with protection rules (required reviewers) **in addition** to AWS Manual Approval — not required for PoC.

## 4. IAM OIDC trust

When you create the deploy role (see manual doc), set the trust `sub` claim to `repo:<owner>/<repo>:*` for the **app** repository (e.g. `myorg/test-ecs-blue-green-app`), not the infra/Terraform repo — unless you intentionally run workflows from another repo.

## 5. First run

1. Set **Variables** (`AWS_ACCOUNT_ID` optional if the role can call STS).
2. **Actions** → **CD — ECR & CodePipeline** → **Run workflow** → enter **version** (e.g. `0.2.0`).
3. In AWS: CodePipeline → latest execution → **Approve** → CodeDeploy blue/green.

## 6. OIDC provider trên account

Mỗi AWS account chỉ cần **một** IAM OIDC provider cho `https://token.actions.githubusercontent.com`. Nếu đã tạo trước đó (Console hoặc CLI), tái sử dụng ARN đó trong trust policy của role deploy; không tạo trùng.
