# Rubric acceptance record

This record separates working local evidence from account-dependent actions.
Update pending items with real links after completing them. Do not submit the
template configuration as proof of an Azure upload or GitHub deployment.

| PDF requirement | Implementation/evidence | Status |
| --- | --- | --- |
| Trained ML application | app/main.py, app/index.html, models/ | Local implementation |
| At least 3 meaningful tests with edge cases | tests/test_app.py, tests/test_data.py | Run results in docs/LOCAL_VERIFICATION.md |
| Git history and dataset commits | Git history, data-v1/data-v2 tags | Local only; team PR evidence still required |
| GitHub online repository | DEPLOYMENT.md setup | Pending team repository URL |
| Feature → dev → staging → main | README branch plan; local branches | Actual team PRs pending |
| Slim Dockerfile and ignore | Dockerfile, .dockerignore | Configured; local Docker unavailable |
| PR CI full tests + lint + Docker build | .github/workflows/ci.yml | GitHub run pending |
| Failed CI cannot merge | Required quality check documented | Account-level rule and refusal test pending |
| Environment-specific staging / production configuration | Delivery environments and .env | Secrets and hosted run pending |
| Automated deployment stage | Delivery starts and checks runner container | Configured; hosted execution pending |
| DVC initialized | .dvc/, data.dvc | Locally verified |
| Azure DVC remote | configure_azure.ps1 and template .dvc/config | Real account/container + upload/pull pending |
| Two dataset versions | data-v1/data-v2, ml/README_data.md | Actual local snapshots |
| Commit ↔ dataset mapping | ml/PROVENANCE.md | Generated from real commits |
| MLflow tracking code | ml/train.py | Actual local runs |
| Baseline + tuned experiments | mlflow.db, mlartifacts/, run summary | Actual local records |
| Parameters, metrics, code/data versions, artifacts | Per-run MLflow records | Inspect with MLflow UI |
| Production model rationale | ml/README_experiments.md, ml/registry/current_model.md | Actual validation selection |

No claim is made that three people used GitHub during this assisted build. Before
submission the three members should review, understand, improve and exercise the
repository through their own accounts. The build environment has no Docker daemon;
only a real Docker build on your machine or GitHub Actions can close that check.
