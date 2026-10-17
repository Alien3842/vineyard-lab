# Current serving model

- Run: `a30d20d714a24da7a580f36804b237f3`
- Code: `5a24bb2c147bfbb88e4083b1e1048f610efca934`
- Dataset: v2, SHA-256 `bb2f6d6a7462be4e15e9ce09cae8cdb5e3bd1b2f59a4f85bd9a4099013c0d5f5`
- Pipeline: StandardScaler + LogisticRegression(C=1.0, max_iter=2000, random_state=42)
- Selected by validation macro F1: 1.000000
- Held-out test: macro F1 0.975172; accuracy 0.972222
- Runtime files: models/model.joblib and models/metadata.json

This registry document is explanatory; the service loads the actual model file, not this text. Promote by validation only using ml.train --promote. Roll back model and metadata together.
