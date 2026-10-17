# 英文问答与中文理解

把英文当作表达参考，用自己的话回答。老师可能追问“在哪一行”“能不能改一下”，因此每题都附上可打开的文件。

## 1. What does the application predict?

It predicts one of three cultivars from thirteen chemical measurements. The target is a class label, not a quality score or a price estimate. We display the original class IDs as one, two and three.

中文：分类目标是品种；原始标签 0/1/2，在页面显示为 1/2/3。不要把类别说成好中差。定位：`app/main.py`。

## 2. Why did you choose this dataset?

It is small, public and available through scikit-learn. That makes the training quick and reproducible, so we can focus on the complete DevOps and MLOps lifecycle. Its small size is also a limitation; it is not representative of every wine in the world.

中文：题目允许 toy scale，选它是为了真正跑完整条流程，不是因为它能解决商业酒类鉴定。定位：`ml/data_pipeline.py`。

## 3. Did you train the model yourselves, or just call a pretrained API?

The training script fits a new StandardScaler and LogisticRegression pipeline on our training split. We save the fitted pipeline and serve it locally. There is no pretrained language-model API in the prediction path.

中文：数据是现成公开数据，但模型参数由本项目 fit 得到。定位：`ml/train.py` 的 model.fit。

## 4. Why logistic regression?

It is fast, interpretable and suitable for a small tabular multiclass problem. It gives class probabilities and has a simple regularization parameter. We do not need a large neural network to demonstrate the required lifecycle.

中文：名字叫回归，但 LogisticRegression 用于分类；多类情况下根据各类分数计算概率，再取最大值。

## 5. Why scale the features?

The features have very different numerical scales. StandardScaler subtracts the training mean and divides by the training standard deviation. It makes regularization behave more consistently across features. The scaler is fitted on the training split only.

中文：例如 alcohol 大约十几，proline 可以上千；标准化避免数值单位影响正则化。不能先对全数据 fit 再分割。定位：make_pipeline。

## 6. What does C mean?

C is the inverse strength of regularization. A smaller C means stronger regularization. We compare C equal to 0.01 and 1.0 with the version-two data held fixed. A higher C is not automatically better; we choose using validation macro F1.

中文：C 不是学习率。不要回答 C 越大越好。定位：`ml/configs/`。

## 7. What changed from v1 to v2?

Version one uses a stratified subset of the training pool. Version two uses the full training pool. The validation and test rows stay exactly the same. We add real samples from the same public dataset; we do not duplicate or synthesize samples.

中文：只是增加训练集覆盖，不能说清洗了脏数据。定位：`ml/README_data.md`，`tests/test_data.py`。

## 8. How do you avoid data leakage?

We split by stable sample IDs, stratify by class, and test that the splits do not overlap. Preprocessing is fitted only on training data. Hyperparameter selection uses validation scores, while the held-out test set is reserved for the selected model.

中文：数据不重叠只是第一步，预处理和模型选择也可能泄漏。定位：数据测试和训练代码。

## 9. Why macro F1 rather than accuracy alone?

Macro F1 computes an F1 score for each class and averages the three scores equally. This helps prevent the largest class from dominating the evaluation. We also report accuracy for readability. On this small test split, both estimates are uncertain.

中文：precision = TP/(TP+FP)，recall = TP/(TP+FN)，F1 = 2PR/(P+R)。macro 每类同权；不是把所有 TP 一起加总再算。

## 10. Your validation F1 is 1.0. Is the model perfect?

No. The validation split contains only thirty-six samples and we used it to choose the model. The selected model makes one mistake on the separate thirty-six-sample test set. We need more independent data before making a stronger claim.

中文：验证满分不能说没有过拟合；实际测试不是满分。定位：实验总结和 models/metadata.json。

## 11. Why three experiments if the requirement says two?

The extra run is a control. V1 versus v2 with C fixed shows the effect of adding training data. V2 with C changed shows the effect of tuning. Without that control we would change two factors at the same time.

中文：baseline v1 → baseline v2 → tuned v2，比较更好解释。

## 12. What is the difference between Git and DVC?

Git versions code and small metadata. DVC hashes dataset contents and stores those contents in a cache or remote storage. Git versions the small DVC pointer. Checking out a Git version and pulling its DVC data restores the corresponding dataset.

中文：Git 不保存这里的 CSV；data.dvc 不含数据本体。定位：data.dvc、.gitignore、.dvc/config。

## 13. What does Azure Blob Storage do here?

It is the shared remote for the DVC dataset objects. It is a cloud service, not our training algorithm and not something that runs the web API. Credentials stay outside Git. The account name and container location identify where DVC should connect.

中文：Azure 是存储数据；本地 .dvc/cache 不是 Azure。没上传验证时必须明确说 pending。

## 14. Can you identify the exact data that produced this model?

Yes, for the local experiments. The model metadata and MLflow record contain the Git SHA, dataset version and a SHA-256 digest. The run also stores the exact data.dvc pointer. The provenance document maps the data tags to commits and DVC hashes.

中文：同时展示 run、Git SHA、data.dvc 内容哈希，不要只展示“v2”文字标签。定位：ml/PROVENANCE.md。

## 15. What does MLflow record?

It records the experiment runs, hyperparameters, validation metrics, code and data identifiers, and artifacts such as the fitted model and confusion matrix. Test metrics are logged only for the promoted run. MLflow tracks the experiment; it does not replace DVC or Git.

中文：本地 SQLite 保存元数据，mlartifacts 保存模型等文件；两个一起保留。定位：ml/train.py。

## 16. Why save the scaler together with the classifier?

Serving must use exactly the same transformation learned during training. Saving a single pipeline prevents us from forgetting the scaler or fitting a new scaler on a prediction request.

中文：不能推理时重新 fit scaler。定位：models/model.joblib 和 app/main.py。

## 17. What makes the tests meaningful?

They check behavior and invariants. Valid predictions must have three probabilities that sum to one. Invalid payloads must return 422. Numerical guards reject non-finite values. Data tests ensure disjoint splits and unchanged evaluation sets across versions. Each group has several cases.

中文：25 个参数化用例，不等于 25 种独立功能；要会解释分类后的测试目的。定位：tests/。

## 18. What is CI in your project?

CI runs on pull requests to dev, staging and main, and on pushes to those branches. It runs Ruff checks, formatting, the full test suite, a Docker build and a container inference smoke test. A failing required quality check should block merging through GitHub branch rules.

中文：workflow 不会自动启用“不能合并”；必须有仓库保护规则并验证。定位：ci.yml。

## 19. What is CD in your project?

After successful push CI on staging or main, delivery checks out that exact commit, creates environment configuration from GitHub Environment secrets, builds and starts the image, verifies it and pushes it to GHCR. The runner container is temporary. We do not claim a permanent production website.

中文：从 Actions 页面展示真实执行；没执行过只能说配置已准备。定位：delivery.yml。

## 20. Why a slim Docker image and .dockerignore?

The runtime only needs the API, its dependencies and the fitted model. We exclude training data, Git history, caches, experiment logs and environment files. This reduces the image contents and avoids copying unnecessary or sensitive files into it. We also run as a non-root user.

中文：不要把整个训练环境装进线上镜像。Dockerfile 的 pip 层先复制 requirements 可以复用缓存。

## 21. What is the difference between an image and a container?

An image is the packaged filesystem and startup configuration. A container is a running instance of that image. Building successfully does not prove the application starts, so our CI also runs the container and sends a prediction request.

中文：镜像 build 通过只是打包成功，smoke test 才检查启动与推理。

## 22. Why does .env not appear in the image?

The pipeline creates it for runtime configuration and passes it with docker run --env-file. It is excluded from the build context. Staging and production use separate GitHub Environments. We avoid baking secrets into an image layer.

中文：Docker 不会自动读取 .env；这里显式传入。演示用 APP_ENV 本身不敏感。

## 23. How would you roll back?

We would create a reviewed revert PR restoring the intended code and model artifact. CI tests that state and delivery builds an image for the new commit. For data investigation, we can check out the matching data tag and restore it with DVC.

中文：模型回退必须模型文件和 metadata 一起回退，不是只改文档里的版本号。

## 24. What are the limitations and next steps?

We have a small historical dataset, a single fixed split and no external validation. Probabilities are not calibrated, and we have no drift monitoring. Next we would collect independent samples, evaluate more robustly, calibrate probabilities and monitor the serving distribution.

中文：回答已有的限制即可；不要说做了交叉验证、漂移告警、真实酒厂数据或云端长期部署，这些都没实现。

## 25. How did the team work together? / Did you use AI?

This must be answered from your real process. Show each member's actual PR and explain what they reviewed, changed and tested. If asked about AI, describe the assistance honestly and follow the course policy. Do not present this package's automated build author as a student contributor.

可以按事实填：

> We used assistance to prepare an initial implementation. Each of us then reviewed a different part, made a change through a pull request, and tested the complete demonstration. My contribution was [your actual change], and I can show that PR and explain the relevant code.

只有真的完成这些步骤后才能这样说；否则说明当前真实状态。

## 不知道时的自然英文

- “Let me show you the relevant code.”（打开代码核对）
- “That is a limitation of our current version.”（确实未实现）
- “We have configured that stage, but we have not verified it on GitHub yet.”（配置与执行区分）
- “We selected using validation data, not the test score.”（解释模型选择）
- “I would need to test that before claiming it works.”（不要猜测）
