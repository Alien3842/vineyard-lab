# Dataset versions

Source: Aeberhard, S. & Forina, M. (1992). Wine [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5PC7J
Original description: https://archive.ics.uci.edu/dataset/109/wine
License: Creative Commons Attribution 4.0 (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/
Local access: sklearn.datasets.load_wine(as_frame=True), using the pinned scikit-learn package.

The source contains 178 samples, 13 numerical features and 3 cultivar classes from the same Italian region. The sklearn target is 0/1/2; the interface displays 1/2/3. We do not invent cultivar names or infer wine quality. The source has no missing values, so no imputation or claimed outlier cleaning is performed.

## Splitting and version change

We first stratify 60% of the full dataset into a training pool and 40% into a held-out pool, using random_state=42. The held-out pool is stratified equally into validation and test. Version one uses 70% of the training pool; version two uses the full training pool. Stable sample_id values allow overlap checks. Those IDs and target are removed from the feature matrix.

| Version | Training | Validation | Test | Change |
| --- | ---: | ---: | ---: | --- |
| data-v1 | 74 | 36 | 36 | First usable training subset |
| data-v2 | 106 | 36 | 36 | 32 additional real training samples |

The evaluation sets remain byte-identical between versions. This avoids selecting a more favorable test split for v2. StandardScaler is fitted only on the corresponding training split. We do not fit on validation or test data. CSV export uses an explicit CRLF line terminator to preserve the original byte representation on Windows and Linux.

## Exact version links

- `data-v1`: commit `8306b5aff77f928b0498fd1cc8ab7baae49ea4e5`, DVC directory hash `2566cdf9877abb6cbd30262b18b20b14.dir`.
- `data-v2`: commit `5a24bb2c147bfbb88e4083b1e1048f610efca934`, DVC directory hash `456b9d52120b803e62579d9056e5c70b.dir`.

Git stores data.dvc and ignores data/. DVC cache objects hold the dataset bytes. The default remote URL is an unconnected Azure template until configured with your real storage account and container. See DEPLOYMENT.md for authentication and uploading both historical versions. Never describe the local cache as proof that the Azure remote works.

## Reproduce a historical dataset safely

Use a disposable clone, install requirements-ml.txt, check out data-v1 or data-v2, then run dvc pull for a configured Azure remote. The supplied offline package can instead restore from its own .dvc/cache with dvc checkout. The source pipeline can regenerate either version using python -m ml.data_pipeline --version v1 (or v2); dvc add data records a new change if you intentionally alter its contents.
