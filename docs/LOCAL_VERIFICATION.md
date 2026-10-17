# Local verification

Verified on Windows with Python 3.12, using the pinned project dependencies.

| Check | Observed outcome |
| --- | --- |
| Training | Three real MLflow runs completed; fitted model artifacts saved |
| Full pytest suite | 25 passed; one upstream Starlette/httpx deprecation warning |
| Ruff lint | All checks passed |
| Ruff formatting | All project Python files formatted |
| DVC status | Data and pipelines are up to date |
| Historical restore | v1 and v2 restored in a separate clone using local DVC cache; hashes matched all runs |
| API smoke | /health returned 200; /predict returned valid probabilities and cultivar 1 |
| Browser | Form loaded, button click produced cultivar 1 with approximately 99.9% model probability |
| MLflow UI | HTTP 200 on port 5000, using one worker for Windows |
| Dependency consistency | pip check: no broken requirements |
| Docker build/runtime | Not executed locally: no Docker CLI/daemon available |
| GitHub Actions / protection / GHCR | Not executed: repository URL and access not supplied |
| Azure push/pull | Not executed: real storage account/container not configured |

The first local pytest attempt encountered the execution sandbox's default-temp
directory restriction. Rerunning with a workspace-local --basetemp completed all
25 tests. This is a local execution setting, not a change to test expectations.

The MLflow UI is started with --workers 1 to avoid Windows multiprocess socket
errors observed with its default multi-worker setting. Job execution is unsupported
on Windows in this MLflow version; the tracking UI and experiment records work.

`test-results.xml` contains the actual test report. `results.json` contains the
real dataset/commit/run mapping. `app-preview.png` is the browser result after
clicking Classify sample. These local files do not substitute for hosted evidence.
