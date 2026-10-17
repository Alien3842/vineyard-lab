# Experiment comparison

All results below are from actual local MLflow runs. Every run uses a StandardScaler + LogisticRegression pipeline, max_iter=2000 and random_state=42.

| Dataset | C | Validation accuracy | Validation macro F1 | Run ID |
| --- | ---: | ---: | ---: | --- |
| v1 | 0.01 | 0.944444 | 0.948413 | `109f9e9599e24b0fa1b8afd0bc89c657` |
| v2 | 0.01 | 0.972222 | 0.974321 | `4d08725b11a04c64bdc6562cf6de8191` |
| v2 | 1.0 | 1.000000 | 1.000000 | `a30d20d714a24da7a580f36804b237f3` |

The v1/v2 comparison with C fixed isolates the effect of adding training data. The two v2 runs isolate the effect of regularization. C is inverse regularization strength: 0.01 applies stronger regularization than 1.0. The third run is not evidence that larger C is always preferable.

We optimize **validation macro F1**, which weights each class equally rather than allowing the largest class to dominate. We also log accuracy. The selected run is the one with highest validation macro F1; ties prefer smaller C. The selected run must match the current dataset hash before promotion. This is a small hand-defined comparison, not cross-validation or a large automated search.

For this teaching application, run `a30d20d714a24da7a580f36804b237f3` (v2, C=1.0) is the serving candidate. Its validation macro F1 is 1.000000. After selection, it achieves test accuracy 0.972222 (35/36 correct) and test macro F1 0.975172. The unselected runs have no test metrics because their test scores were not used for selection.

These numbers do not establish real-world readiness. Validation contains only 36 samples and was used to select the model; the test set also contains 36 samples. One mistake materially changes the score. There is no external validation, uncertainty interval, calibrated confidence or drift monitor. "Serving candidate" means suitable for this course demonstration only.

Each run logs C, maximum iterations, random state, training row count, Git SHA, dataset label and SHA-256 digest. Artifacts include the exact data.dvc pointer, fitted model, validation confusion matrix and metadata. The selected run also has promotion metadata and test scores. In the confusion matrix, rows are true labels and columns predicted labels, ordered 0,1,2.

The SQLite database and mlartifacts directory are supplied in the ZIP for offline inspection. They are deliberately ignored by Git. Run scripts/relocate_tracking.py with the UI stopped after moving the bundle, then start the UI from the project root. Run IDs and metric values remain unchanged during path repair. Fresh clones from GitHub need the offline tracking bundle or genuine new training runs to obtain this run history.
