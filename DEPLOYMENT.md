# Delivery and external setup

## 1. Publish the existing repository

Use the supplied repository with its existing history; do not run `git init` again.
Create an empty GitHub repository without an initial README. From this project:

```powershell
git remote add origin https://github.com/YOUR-TEAM/YOUR-REPOSITORY.git
git push -u origin main
git push origin dev staging --tags
```

Replace the URL with the real repository. No credentials belong in the URL or Git.
Enable Actions. The first staging/main push can fail delivery until step 2 is done;
CI remains independently visible. Push a new reviewed commit after configuration.

## 2. Configure GitHub Environments and merge rules

Settings → Environments: create `staging` and `production`. Under each environment,
create an **environment secret** named `APP_ENV`: respectively `staging` and
`production`. This value is intentionally non-sensitive for a safe teaching demo;
it demonstrates environment isolation without placing real passwords in the image.
Restrict environment deployment branches to their corresponding branch. Enable
package creation for Actions if organization policy requires it. GHCR publishing
uses the workflow's short-lived `GITHUB_TOKEN` with `packages: write`.

Settings → Rules / Branch protection: protect `dev`, `staging`, `main`; require a
pull request, one approval by a teammate, and the CI status check **quality**.
Run CI once if the check is not yet selectable. Require current checks and disable
force push/deletion/bypass where supported. Some GitHub plans restrict enforcement
for private repositories: verify the effective rules; use a suitable public repo
if course/privacy constraints allow it. Do not call the rule enforced until tested.

Have each student make a real change on their own feature branch. Merge feature
into dev, dev into staging, staging into main using PRs. Keep links to one PR per
person. Never fabricate author identities, dates, approvals or screenshots.

## 3. Azure Blob Storage for DVC

Create or use an Azure Storage account and a **private Blob container**. Install
Azure CLI, sign in locally with `az login`, and grant the signed-in identity
Storage Blob Data Contributor at the relevant scope. Roles can take time to apply.
Then use the activated ML environment:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/configure_azure.ps1 -AccountName YOURACCOUNT -ContainerName YOURCONTAINER
dvc push --all-commits
dvc status -c
git add .dvc/config
git commit -m "Configure team Azure data remote"
```

`--all-commits` uploads v1 as well as v2 from the local cache and history. Verify
both snapshots in a separate clone with `git checkout data-v1` / `dvc pull` and
`git checkout data-v2` / `dvc pull`. These checkout commands belong in a disposable
clone to avoid disturbing the demonstration worktree. Never delete the main cache
as part of proving a download.

If account policy requires a connection string, enter it locally with
`dvc remote modify --local azure connection_string <your-value>`; `.dvc/config.local`
is ignored. Do not paste it into chat, documentation, screenshots, or Actions logs.
The template remote uses container `vineyard-data` and lacks an account name until
you run the configuration script. It is a template, not a connected Azure remote.

## 4. What the delivery pipeline actually does

`CI` runs on PRs and branch pushes. `Delivery` is a `workflow_run` triggered only
after successful **push** CI on staging/main, avoiding PR secrets and races between
independent test and publishing workflows. It checks out the successful run's SHA,
builds `ghcr.io/<owner>/<repository>:<sha>`, starts the image with `--env-file .env`,
waits for readiness and checks a prediction. Only a passing image is pushed.

The `.env` is runtime configuration and is excluded by `.dockerignore`. Docker
does not automatically read `.env`; the explicit `--env-file` is essential.
The image is branch-specific by commit and environment is supplied at runtime.
There is no separate release workflow and no persistent cloud host. For the
rubric's automated deployment stage, an actual container starts on the temporary
runner and is checked, then removed. Explain this scope honestly to the teacher.

## 5. Evidence and failure demonstration

Before Monday's demonstration, retain links/screenshots for: green CI including
Docker, a refused merge with failing `quality`, staging delivery success,
production delivery success, GHCR commit image tag, Azure blobs, successful fresh
`dvc pull`, and MLflow runs. Hide any secrets.

For the failed-check demonstration use a disposable feature PR with a deliberately
failing assertion, confirm merging is blocked, then close that PR. Do not put a
failing commit onto the protected branches. Rollback is a reviewed revert PR to
the desired model/code version; delivery then produces a new commit-tagged image.
