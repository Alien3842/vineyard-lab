"""Fixed held-out rows; v2 adds real training rows, never test rows."""

import argparse
from pathlib import Path

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split


def build(version: str, destination: Path = Path("data")):
    wine = load_wine(as_frame=True)
    frame = wine.frame.copy()
    frame.insert(0, "sample_id", frame.index)
    train, held = train_test_split(frame, test_size=0.4, random_state=42, stratify=frame.target)
    validation, test = train_test_split(held, test_size=0.5, random_state=42, stratify=held.target)
    if version == "v1":
        train, _ = train_test_split(train, train_size=0.7, random_state=42, stratify=train.target)
    elif version != "v2":
        raise ValueError("version must be v1 or v2")
    destination.mkdir(parents=True, exist_ok=True)
    for name, subset in [("train", train), ("validation", validation), ("test", test)]:
        subset.sort_values("sample_id").to_csv(destination / f"{name}.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", choices=["v1", "v2"], required=True)
    build(parser.parse_args().version)
