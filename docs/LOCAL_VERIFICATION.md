# Local verification

Verified on Windows with Python 3.12, using the pinned project dependencies.

| Check | Observed outcome |
| --- | --- |
| Training | Three real MLflow runs completed; fitted model artifacts saved |
| Full pytest suite | 31 passed, including 6 readiness regression cases; one upstream Starlette/httpx deprecation warning |
| Ruff lint | All checks passed |
| Ruff formatting | All project Python files formatted |
| DVC status | Data and pipelines are up to date |
| Historical restore | v1 and v2 restored in a separate clone using local DVC cache; hashes matched all runs |
| API smoke | /health returned 200; /predict returned valid probabilities and cultivar 1 |
| Browser | Form loaded, button click produced cultivar 1 with approximately 99.9% model probability |
| MLflow UI | HTTP 200 on port 5000, using one worker for Windows |
| Dependency consistency | pip check: no broken requirements |
| Docker build/runtime | GitHub CI built the image successfully; initial container smoke test failed; no local Docker daemon |
| GitHub Actions / protection / GHCR | Initial hosted lint, tests and Docker build passed; readiness fix awaits PR verification; branch protection and GHCR delivery pending |
| Azure push/pull | Not executed: real storage account/container not configured |

The first local pytest attempt encountered the execution sandbox's default-temp
directory restriction. Rerunning with a workspace-local --basetemp completed all
25 tests. This is a local execution setting, not a change to test expectations.

The MLflow UI is started with --workers 1 to avoid Windows multiprocess socket
errors observed with its default multi-worker setting. Job execution is unsupported
on Windows in this MLflow version; the tracking UI and experiment records work.

## First hosted CI and readiness fix

The public GitHub Actions job metadata confirms that dependency installation,
lint/formatting, all original 25 tests and Docker build succeeded. The following
container smoke test failed immediately. The unauthenticated log-download API
requires repository-admin access. The repository owner supplied the job traceback,
which confirms ConnectionResetError (Errno 104) during the first health request.
Reference: https://github.com/Starry202122/vineyard-lab/actions/runs/39052787857

Readiness regression tests reproduce a gap: an early connection reset or remote
disconnect escapes the original retry handler. The fix retries those transport
errors within the existing 30-attempt limit and prints diagnostics. Permanent
startup failure still fails CI. These tests failed against the original handler
and pass with the fix; they do not substitute for rerunning the actual Docker job.

`test-results.xml` contains the actual test report. `results.json` contains the
real dataset/commit/run mapping. `app-preview.png` is the browser result after
clicking Classify sample. These local files do not substitute for hosted evidence.
