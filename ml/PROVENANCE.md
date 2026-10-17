# Code, dataset and model provenance

| Tag | Git commit | DVC directory MD5 | Content SHA-256 |
| --- | --- | --- | --- |
| data-v1 | `8306b5aff77f928b0498fd1cc8ab7baae49ea4e5` | `2566cdf9877abb6cbd30262b18b20b14.dir` | `cddba0255ac4611b3911a34246f9fedc358ba4e17939225fac7b881cef5533b5` |
| data-v2 | `5a24bb2c147bfbb88e4083b1e1048f610efca934` | `456b9d52120b803e62579d9056e5c70b.dir` | `bb2f6d6a7462be4e15e9ce09cae8cdb5e3bd1b2f59a4f85bd9a4099013c0d5f5` |

DVC uses a directory hash and individual file objects. The SHA-256 above is an additional ordered digest over each CSV filename and its bytes, as implemented in ml/train.py. These are different hash schemes, not conflicting versions.

Promoted MLflow run: `a30d20d714a24da7a580f36804b237f3`. Training code commit: `5a24bb2c147bfbb88e4083b1e1048f610efca934`. The fitted preprocessing and classifier are packaged together in models/model.joblib. Later documentation and portability commits do not change these recorded training identities.

Both historical tags were checked out in a separate local clone and restored using DVC from the supplied local cache. All three run digests matched those restored datasets. This is local restore evidence, not an Azure upload/download claim.
