"""Train on train only, select by validation macro F1, test once at promotion."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def git_sha():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def dataset_hash():
    digest = hashlib.sha256()
    for path in sorted(Path("data").glob("*.csv")):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def load_split(name):
    frame = pd.read_csv(f"data/{name}.csv")
    return frame.drop(columns=["sample_id", "target"]), frame.target


def train(version, config_path):
    config = json.loads(Path(config_path).read_text())
    x, y = load_split("train")
    xv, yv = load_split("validation")
    model = make_pipeline(StandardScaler(), LogisticRegression(**config))
    model.fit(x, y)
    predictions = model.predict(xv)
    metrics = {
        "validation_macro_f1": f1_score(yv, predictions, average="macro"),
        "validation_accuracy": accuracy_score(yv, predictions),
    }
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    if mlflow.get_experiment_by_name("vineyard-lab") is None:
        mlflow.create_experiment("vineyard-lab", artifact_location="./mlartifacts")
    mlflow.set_experiment("vineyard-lab")
    with mlflow.start_run(run_name=f"{version}-C{config['C']}") as run:
        mlflow.log_params(
            config
            | {
                "dataset_version": version,
                "git_sha": git_sha(),
                "dataset_sha256": dataset_hash(),
                "train_rows": len(x),
            }
        )
        mlflow.log_metrics(metrics)
        pointer = Path("data.dvc").read_text()
        mlflow.log_text(pointer, "data.dvc")
        run_dir = Path("experiments") / run.info.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, run_dir / "model.joblib")
        np.savetxt(
            run_dir / "confusion_validation.csv",
            confusion_matrix(yv, predictions),
            fmt="%d",
            delimiter=",",
        )
        metadata = {
            "run_id": run.info.run_id,
            "git_sha": git_sha(),
            "dataset_version": version,
            "dataset_sha256": dataset_hash(),
            "feature_names": list(x.columns),
            "config": config,
            **metrics,
        }
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
        mlflow.log_artifacts(str(run_dir))
        print(json.dumps(metadata, indent=2))
    return metadata


def promote():
    candidates = [json.loads(p.read_text()) for p in Path("experiments").glob("*/metadata.json")]
    # Stable tie-break: prefer the smaller C (stronger regularization).
    best = max(candidates, key=lambda m: (m["validation_macro_f1"], -m["config"]["C"]))
    if best["dataset_sha256"] != dataset_hash():
        raise ValueError("Selected model dataset differs from current DVC data")
    source = Path("experiments") / best["run_id"] / "model.joblib"
    model = joblib.load(source)
    xt, yt = load_split("test")
    predictions = model.predict(xt)
    best.update(
        {
            "test_macro_f1": f1_score(yt, predictions, average="macro"),
            "test_accuracy": accuracy_score(yt, predictions),
            "test_rows": len(xt),
        }
    )
    Path("models").mkdir(exist_ok=True)
    joblib.dump(model, "models/model.joblib")
    Path("models/metadata.json").write_text(json.dumps(best, indent=2))
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    with mlflow.start_run(run_id=best["run_id"]):
        mlflow.log_metrics({k: best[k] for k in ["test_accuracy", "test_macro_f1"]})
        mlflow.log_dict(best, "promotion.json")
    print(json.dumps(best, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", choices=["v1", "v2"])
    parser.add_argument("--config", default="ml/configs/baseline.json")
    parser.add_argument("--promote", action="store_true")
    args = parser.parse_args()
    if args.promote:
        promote()
    elif args.version:
        train(args.version, args.config)
    else:
        parser.error("provide --version or --promote")
