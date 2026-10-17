# 三人准备安排 / Three-person preparation

提交前请先看 `ACCEPTANCE.md`。项目已经有本地实现，但 GitHub、Azure、Docker 的远端证据必须真实补齐。以下是建议分工，不是已经发生的小组协作记录。请把 A/B/C 换成真实姓名，并在各自账号留下真实的 PR。

## A：应用、接口、测试 / Application and testing

读 `app/main.py`、`app/index.html`、`tests/test_app.py`。亲自运行网页，点击预测；用 `/docs` 发一个缺少特征的请求，观察 422；运行测试并解释每一组测试的目的。

建议真实贡献：增加一个有意义的输入场景测试，或改进页面错误提示，通过 feature 分支发 PR，请队友审核。

30-second introduction:

> I focus on the application and its tests. The browser sends thirteen measurements to a FastAPI endpoint. The server validates the input and uses a saved preprocessing-and-classification pipeline. It returns a cultivar ID and three probabilities. We also test incorrect lengths, invalid types and non-finite values. Input validation prevents malformed requests, but it does not prove that a sample comes from the training distribution.

## B：数据、模型、实验 / Data and MLOps

读 `ml/data_pipeline.py`、`ml/train.py`、`ml/README_data.md`、`ml/README_experiments.md`。打开 MLflow，找出三次 run 的 C、dataset hash、Git SHA、指标和模型文件。能把某个 run 对回 DVC 指针。

建议真实贡献：补充每个类别的验证集错误分析，或增加一个与现有实验区分明确的验证实验。不要为了刷分反复看测试集调参。

30-second introduction:

> I focus on the data and experiment lifecycle. We keep validation and test samples fixed across dataset versions. Version two adds real training samples. We compare the same model setting first, then tune regularization on the validation set. MLflow records the configuration, metrics, model and code-and-data identifiers. DVC records the dataset contents, while Azure is the shared storage for those contents.

Azure 未配置前，最后一句可以改成：

> The Azure remote template is ready, but the upload has not been verified yet.

## C：Git、Docker、CI/CD / DevOps

读 `Dockerfile`、`.dockerignore`、两份 workflow 和 `DEPLOYMENT.md`。亲自完成一次 PR 检查，查看 Docker build 日志，配置并测试分支保护，确认 staging/production 的环境变量不同。

建议真实贡献：完善 smoke test 的失败信息，或者补充一次真实的 staging 验证记录。截图和文档只描述真的执行过的内容。

30-second introduction:

> I focus on the delivery process. Our planned path is feature to dev, then staging, then main. Pull requests run formatting, linting, tests, a Docker build and an inference smoke test. GitHub branch rules must require the quality check. After successful push CI, delivery uses the corresponding environment secret, starts and checks a container on the runner, and publishes an image tagged with the exact commit. The runner deployment is temporary.

## 所有人都要会的五件事

1. 这是品种分类，不是酒的好坏评分；3 类标签不是已知商品名。
2. 代码由 Git 管，数据内容由 DVC 管，训练记录由 MLflow 管；三者不是互相替代。
3. 标准化只在训练集 fit，验证和测试只能 transform；否则会泄漏信息。
4. 验证集用于选择，测试集用于选定后的评估。分数高不等于现实部署可靠。
5. 能指出仓库中“实际完成”和“仍待账号验证”的区别。

## 周日前的练习顺序

- 第一轮，各自跑通自己负责的一块，记下真正不懂的函数。
- 第二轮，互换角色：A 解释 DVC，B 解释 CI，C 解释预测流程。
- 第三轮，合上讲稿，每人随机答五题。用自己的英文说，停顿和简短表达没有关系。
- 最后一轮，断开网络再测试本地应用和已有 MLflow 记录；线上 GitHub/Azure 证据提前准备好。

不要背诵“我们花了几周”“我们遇到了某某问题”这类没有发生过的故事。如果课程要求披露 AI 辅助，按课程规定披露；能够定位代码、解释结果、亲自修改并验证，才是答辩准备的重点。
