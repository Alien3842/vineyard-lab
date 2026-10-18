# Course Azure remote: verified

The private course DVC-with-Azure-Blob-Storage guide supplies a storage account,
container and SAS credential for this project. You do not need a personal Azure
subscription or payment card to use that supplied resource.

- Account: `wut2026`
- Container: `dvc`
- Project prefix: `vineyard-lab-starry202122`
- Remote: `azure`
- Credential: `.dvc/config.local`, ignored by Git and excluded from ZIP packaging
- SAS expiry stated in the course guide: 2026-12-12 10:59:11 UTC

`dvc push --all-commits -r azure` completed: **6 objects pushed**. These are
directory manifests and data file objects, not six distinct datasets. A dedicated
prefix separates this project from other groups in the shared container.

## Actual remote recovery

Two separate Git clones were created and checked out at `data-v1` and `data-v2`.
Each clone had its own empty DVC cache before recovery. No data directory or cache
was copied from the original project. Only local private remote configuration was
supplied. Each clone ran `dvc pull -r azure`.

| Tag | DVC result | Train / validation / test | Dataset digest |
| --- | --- | --- | --- |
| data-v1 | 4 objects fetched, 3 CSVs materialized | 74 / 36 / 36 | Matched original training record |
| data-v2 | 4 objects fetched, 3 CSVs materialized | 106 / 36 / 36 | Matched original training record |

Exact Git SHAs and SHA-256 digests are in `azure-download-verification.json`.
They agree with `ml/PROVENANCE.md` and the recorded MLflow runs. Access was proven
at verification time; the resource owner can revoke the token before its expiry.

## Teammate setup

Install `requirements-ml.txt`, then run:

```powershell
python scripts/configure_course_azure.py
dvc pull -r azure
```

Enter the complete single-line SAS token from the private course guide at the
hidden prompt. The helper contains no token. It saves the account and URL locally
too, so historical tags with placeholder configuration use the same endpoint.
The current machine is already configured. Do not upload the private course PDF
or local credential file to GitHub. Show `.dvc/config`, the pointer, download
output and hashes for a demo; do not display `.dvc/config.local`.

English explanation:

> Our course provides an Azure Blob container and a time-limited SAS token. We
> store the credential only in local ignored configuration. We pushed both
> dataset versions, then recovered each in a separate clone with an empty cache.
> The downloaded hashes match the data used by our recorded experiments.
