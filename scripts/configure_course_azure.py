"""Configure the course resource without committing the private SAS credential."""

import getpass
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs

ROOT = Path(__file__).resolve().parent.parent
REMOTE = "azure"
URL = "azure://dvc/vineyard-lab-starry202122"
ACCOUNT = "wut2026"


def main():
    ignored = subprocess.run(
        ["git", "check-ignore", ".dvc/config.local"], cwd=ROOT, capture_output=True
    )
    if ignored.returncode:
        raise RuntimeError("Local DVC credential file must be ignored by Git")
    token = getpass.getpass("Paste the course SAS token (input hidden): ").strip().lstrip("?")
    if not {"sp", "se", "sig"}.issubset(parse_qs(token)) or any(c.isspace() for c in token):
        raise ValueError("Provide the complete single-line SAS token from the private course guide")
    for name, value in [("url", URL), ("account_name", ACCOUNT), ("sas_token", token)]:
        result = subprocess.run(
            [sys.executable, "-m", "dvc", "remote", "modify", "--local", REMOTE, name, value],
            cwd=ROOT,
            capture_output=True,
        )
        if result.returncode:
            raise RuntimeError(f"DVC could not save local {name}; credential output suppressed")
    print("Course remote configured in Git-ignored .dvc/config.local.")
    print("Use dvc pull -r azure, or dvc push --all-commits -r azure.")


if __name__ == "__main__":
    main()
