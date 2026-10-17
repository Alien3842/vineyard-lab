# 座位演示顺序 / Desk-side demonstration

这不是正式幻灯片汇报。老师来之前把应用、MLflow、仓库、Actions、Azure 证据页提前打开；不要临场安装依赖或首次配置云服务。

## 演示前准备

终端 1（基础环境）：

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

终端 2（已安装 requirements-ml.txt）：

```powershell
python scripts/relocate_tracking.py
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000 --workers 1
```

仅在 MLflow 服务没运行时执行路径修复脚本。终端 3 留作测试：

```powershell
python -m pytest -q
git log --oneline --decorate --all
dvc status
```

## 约五分钟的顺序

**0:00 - 0:40 / A，讲用途并点预测**

> This is Vineyard Lab. It predicts one of three wine cultivars from chemical measurements. It is a small educational application, not a wine-quality rating tool. I will send the example measurements to the API.

点击 Classify sample。接着说：

> The API returns a class and the probabilities for all three classes. These probabilities come from the model; we have not calibrated them as real-world confidence estimates.

**0:40 - 1:30 / A，展示错误输入与测试**

在 `/docs` 对 `/predict` 使用 `{"values": [1, 2]}`，显示 422。运行测试。

> Here the request has too few measurements, so the API rejects it. Our tests cover valid predictions, invalid payloads, numerical edge cases, service endpoints and data-split integrity. We also check that repeated predictions are deterministic.

**1:30 - 2:40 / B，展示实验与数据**

打开 MLflow 的 vineyard-lab。显示 C、dataset_version、Git SHA、验证分数，再打开某个 run 的 Artifacts。

> We ran three experiments. The first comparison changes only the number of training samples. The second comparison keeps the version-two dataset fixed and changes C. This lets us separate the data change from the hyperparameter change. The validation score determines the selected model. The test set is evaluated after that choice.

打开 `ml/PROVENANCE.md` 和 `data.dvc`。

> This DVC pointer identifies the exact data contents. The Git commit and MLflow run tell us which code and dataset produced the model.

**2:40 - 4:00 / C，展示 DevOps**

打开真实 PR、CI 日志、分支规则和 Delivery。若还没连接 GitHub，必须改说 configured / pending，不能说 passed。

> A pull request must pass the quality check. That includes tests, static checks, a Docker build and a container smoke test. Successful pushes to staging and main trigger delivery with separate environment configuration. The container is actually started and checked on the runner, then the image is published to GHCR.

> There is no permanent public hosting in this project. The runner container is temporary; the verified container image is the delivery artifact.

**4:00 - 5:00 / 任一成员，展示 Azure 并讲限制**

展示真实 `dvc push` / fresh clone `dvc pull` 记录及 Blob 页面，不能只展示模板 URL。

> Git stores small pointers. Azure Blob Storage holds the dataset objects. A teammate can obtain the correct data version using Git and DVC together.

最后自然停在：

> The main limitation is the small historical dataset. We would need external validation, probability calibration and monitoring before using this outside a teaching demonstration.

## 常见故障

| 现象 | 处理 |
| --- | --- |
| 8000 端口已占用 | 关闭旧服务，或 uvicorn 加 `--port 8001`；smoke.py 固定 8000，要用默认端口验证 |
| 找不到模型 | 必须从项目目录运行，确认 models/model.joblib 已解压，不要只复制 app/ |
| sklearn 版本警告 | 用 Python 3.12 和锁定依赖重新建环境，不要用系统里旧版本加载模型 |
| MLflow 看得到指标但打不开模型 | 停服务，确认 mlartifacts/ 完整，运行路径修复脚本再启动 |
| DVC 无法连 Azure | 本地网页仍能运行；核对账户、容器、登录及 Blob 数据权限，不能把缓存命中当成远端成功 |
| PR 绿了但 Delivery 不运行 | Delivery 只响应 staging/main 的成功 push CI，不响应 PR CI；检查 Environment 与 secret |
| 老师问到不会的内容 | 说 “Let me show you the relevant code.” 然后定位；不要编造机制或实验 |
