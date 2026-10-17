"""Repair local artifact paths after moving this offline MLflow bundle.

Stop the MLflow UI first. Metrics, parameters and run identities are unchanged.
"""

import shutil
import sqlite3
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent.parent
    database = root / "mlflow.db"
    if not database.exists():
        raise FileNotFoundError("No supplied mlflow.db found")
    shutil.copy2(database, root / "mlflow.db.before-relocation")
    with sqlite3.connect(database) as connection:
        experiment = connection.execute(
            "SELECT experiment_id FROM experiments WHERE name = ?", ("vineyard-lab",)
        ).fetchone()
        if experiment is None:
            raise ValueError("Expected vineyard-lab experiment")
        runs = connection.execute(
            "SELECT run_uuid FROM runs WHERE experiment_id = ?", experiment
        ).fetchall()
        for (run_id,) in runs:
            target = root / "mlartifacts" / run_id / "artifacts"
            if not (target / "model.joblib").exists():
                raise FileNotFoundError(f"Missing run artifacts: {run_id}")
            connection.execute(
                "UPDATE runs SET artifact_uri = ? WHERE run_uuid = ?",
                (target.as_uri(), run_id),
            )
        connection.execute(
            "UPDATE experiments SET artifact_location = ? WHERE experiment_id = ?",
            ((root / "mlartifacts").as_uri(), experiment[0]),
        )
    print(f"Updated paths for {len(runs)} runs. Backup: mlflow.db.before-relocation")


if __name__ == "__main__":
    main()
