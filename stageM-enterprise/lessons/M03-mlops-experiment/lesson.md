# M03: MLOps 实验追踪

> **课程编号**: M03
> **所属阶段**: Stage M - 企业级 AI 应用
> **预计时长**: 4-5 小时
> **难度**: ⭐⭐⭐⭐ (中高级)
> **前置课程**: L51 (异步数据管道)、L52 (NumPy 基础)
> **状态**: 🟡 完善中
> **版本**: v4.1
> **最后更新**: 2026-07-18

---

## 📌 学习目标

完成本课程后，你将能够：

1. **理解 MLOps**：掌握 ML 系统工程化的核心理念
2. **实验管理**：使用 MLflow 追踪实验和模型版本
3. **特征管理**：构建企业级特征存储
4. **模型服务**：实现 A/B 测试和模型监控

---

## 📚 课程内容

### 第一部分：MLOps 概述

#### 1.1 为什么需要 MLOps

```
传统软件开发：
代码 → 部署 → 监控 (CI/CD)

ML 系统开发：
代码 + 数据 + 模型 → 训练 → 评估 → 部署 → 监控 (MLOps)
         ↓
    数据漂移、模型衰减、特征工程
```

#### 1.2 MLOps 成熟度模型

| 级别 | 特征 | 自动化程度 |
|------|------|------------|
| **Level 0** | 手动过程、无版本控制 | 0% |
| **Level 1** | 自动化训练、模型版本管理 | 30% |
| **Level 2** | 自动化 CI/CD、特征存储 | 60% |
| **Level 3** | 自动化部署、监控、告警 | 90% |

#### 1.3 MLOps 工具生态

```
┌─────────────────────────────────────────────────────────┐
│                     MLOps 工具生态                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  实验追踪 ──────────────────────────────────→ 模型注册  │
│  MLflow / W&B / TensorBoard           MLflow / Vertex AI│
│                                                          │
│  特征存储 ──────────────────────────────────→ 模型服务  │
│  Feast / Tecton / Hopsworks           Seldon / KServe   │
│                                                          │
│  数据验证 ──────────────────────────────────→ 监控告警  │
│  Great Expectations / TFDV           Evidently / Prometheus│
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

### 第二部分：MLflow 实验追踪

#### 2.1 MLflow 核心概念

```python
# MLflow 四大组件
# 1. Tracking - 实验追踪
# 2. Models - 模型管理
# 3. Model Registry - 模型注册表
# 4. Projects - 项目打包
```

#### 2.2 基础实验追踪

```python
import mlflow
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd

# 设置跟踪服务器
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("customer-churn-prediction")

def train_model_with_tracking(
    n_estimators: int,
    max_depth: int,
    min_samples_split: int,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> dict:
    """带追踪的模型训练"""

    with mlflow.start_run(run_name=f"rf_e{n_estimators}_d{max_depth}"):
        # 记录参数
        mlflow.log_params({
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "model_type": "RandomForestClassifier"
        })

        # 训练模型
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=42
        )
        model.fit(X_train, y_train)

        # 预测和评估
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")

        # 记录指标
        mlflow.log_metrics({
            "accuracy": accuracy,
            "f1_score": f1,
            "test_samples": len(y_test)
        })

        # 记录特征重要性
        feature_importance = pd.DataFrame({
            "feature": X_train.columns,
            "importance": model.feature_importances_
        }).sort_values("importance", ascending=False)

        # 保存特征重要性为 artifact
        feature_importance.to_csv("feature_importance.csv", index=False)
        mlflow.log_artifact("feature_importance.csv")

        # 记录模型
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name="customer-churn-rf"
        )

        return {
            "accuracy": accuracy,
            "f1_score": f1,
            "model": model
        }


# 使用示例
# X, y = load_customer_data()
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# result = train_model_with_tracking(100, 10, 5, X_train, y_train, X_test, y_test)
```

#### 2.3 自动化超参数搜索

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import numpy as np

def hyperparameter_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    search_type: str = "random",
    n_iter: int = 20
) -> dict:
    """
    超参数搜索并记录到 MLflow
    """
    mlflow.set_experiment("hyperparameter-tuning")

    param_grid = {
        "n_estimators": [50, 100, 200, 300],
        "max_depth": [5, 10, 15, 20, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]
    }

    base_model = RandomForestClassifier(random_state=42)

    if search_type == "grid":
        search = GridSearchCV(
            base_model,
            param_grid,
            cv=5,
            scoring="f1_weighted",
            n_jobs=-1
        )
    else:
        search = RandomizedSearchCV(
            base_model,
            param_grid,
            n_iter=n_iter,
            cv=5,
            scoring="f1_weighted",
            n_jobs=-1,
            random_state=42
        )

    with mlflow.start_run(run_name=f"hpo_{search_type}"):
        search.fit(X_train, y_train)

        # 记录最佳参数
        mlflow.log_params(search.best_params_)
        mlflow.log_metrics({
            "best_cv_score": search.best_score_,
            "n_iter": n_iter if search_type == "random" else len(param_grid["n_estimators"]) *
                      len(param_grid["max_depth"]) * len(param_grid["min_samples_split"]) *
                      len(param_grid["min_samples_leaf"])
        })

        # 记录所有试验结果
        cv_results = pd.DataFrame(search.cv_results_)
        cv_results.to_csv("cv_results.csv", index=False)
        mlflow.log_artifact("cv_results.csv")

        mlflow.sklearn.log_model(
            search.best_estimator_,
            "best_model",
            registered_model_name="customer-churn-optimized"
        )

        return {
            "best_params": search.best_params_,
            "best_score": search.best_score_,
            "best_model": search.best_estimator_
        }
```

---

### 第三部分：特征存储

#### 3.1 特征存储架构

```
┌─────────────────────────────────────────────────────────┐
│                     特征存储架构                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐ │
│  │ 数据源   │   →     │ 特征管道  │   →     │ 特征存储  │ │
│  │ (ODS)    │         │ (Flink等) │         │ (Redis等) │ │
│  └──────────┘         └──────────┘         └──────────┘ │
│                                                  ↓        │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐ │
│  │ 离线训练  │ ←       │ 特征注册  │         │ 在线服务  │ │
│  │ (Batch)  │         │ (Registry)│         │ (Real-time)│ │
│  └──────────┘         └──────────┘         └──────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 3.2 Feast 特征定义

```python
# features.py - Feast 特征定义

from feast import Entity, Feature, FeatureView, FileSource
from feast.types import Float64, Int64
from pandas import Timestamp

# 定义实体（主键）
customer = Entity(
    name="customer_id",
    description="Customer identifier"
)

# 定义数据源
customer_stats_source = FileSource(
    path="data/customer_stats.parquet",
    timestamp_field="event_timestamp"
)

# 定义特征视图
customer_stats_fv = FeatureView(
    name="customer_statistics",
    entities=["customer_id"],
    ttl=Timedelta(days=365),
    schema=[
        Feature(name="total_purchases", dtype=Int64),
        Feature(name="avg_order_value", dtype=Float64),
        Feature(name="last_purchase_days", dtype=Int64),
        Feature(name="churn_risk_score", dtype=Float64),
    ],
    source=customer_stats_source
)

# 注册特征
def register_features():
    from feast import RepoConfig, FeatureStore

    config = RepoConfig(
        project="customer_ml",
        provider="local",
        feature_store="data/feature_store"
    )

    fs = FeatureStore(config=config)
    fs.apply([customer, customer_stats_fv])
    print("Features registered successfully!")


# 使用特征
async def get_online_features(customer_ids: list[int]) -> pd.DataFrame:
    """获取在线特征"""
    from feast import FeatureStore

    fs = FeatureStore(repo_path=".")

    feature_service = fs.get_feature_service("customer_churn_features")

    features = await fs.get_online_features(
        feature_refs=[
            "customer_statistics:total_purchases",
            "customer_statistics:avg_order_value",
            "customer_statistics:last_purchase_days",
            "customer_statistics:churn_risk_score"
        ],
        entity_rows=[{"customer_id": cid} for cid in customer_ids]
    )

    return features.to_df()


# 离线特征获取（用于训练）
def get_historical_features(
    customer_ids: list[int],
    event_timestamps: list[Timestamp]
) -> pd.DataFrame:
    """获取历史特征用于训练"""
    from feast import FeatureStore

    fs = FeatureStore(repo_path=".")

    training_df = fs.get_historical_features(
        feature_refs=[
            "customer_statistics:total_purchases",
            "customer_statistics:avg_order_value",
            "customer_statistics:last_purchase_days",
            "customer_statistics:churn_risk_score"
        ],
        entity_df=pd.DataFrame({
            "customer_id": customer_ids,
            "event_timestamp": event_timestamps
        })
    ).to_df()

    return training_df
```

#### 3.3 特征血缘追踪

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class FeatureType(Enum):
    RAW = "raw"           # 原始特征
    DERIVED = "derived"   # 派生特征
    AGGREGATED = "aggregated"  # 聚合特征

@dataclass
class FeatureLineage:
    """特征血缘"""
    feature_name: str
    feature_type: FeatureType
    source_tables: List[str]
    source_columns: List[str]
    transformation_sql: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    description: str = ""

class FeatureCatalog:
    """特征目录"""

    def __init__(self):
        self.features: dict[str, FeatureLineage] = {}

    def register_feature(self, lineage: FeatureLineage) -> None:
        """注册特征"""
        self.features[lineage.feature_name] = lineage

    def get_lineage(self, feature_name: str) -> Optional[FeatureLineage]:
        """获取特征血缘"""
        return self.features.get(feature_name)

    def get_upstream_features(self, feature_name: str) -> List[str]:
        """获取上游特征"""
        lineage = self.get_lineage(feature_name)
        if not lineage:
            return []
        return lineage.source_columns

    def get_downstream_features(self, feature_name: str) -> List[str]:
        """获取下游特征"""
        downstream = []
        for name, lineage in self.features.items():
            if feature_name in lineage.source_columns:
                downstream.append(name)
        return downstream

    def visualize_lineage(self, feature_name: str) -> str:
        """可视化血缘"""
        upstream = self.get_upstream_features(feature_name)
        downstream = self.get_downstream_features(feature_name)

        return f"""
Feature: {feature_name}
{'=' * len(feature_name)}

Upstream Dependencies:
{chr(10).join(f'  - {f}' for f in upstream) if upstream else '  (none)'}

Downstream Consumers:
{chr(10).join(f'  - {f}' for f in downstream) if downstream else '  (none)'}
"""
```

---

### 第四部分：模型服务与监控

#### 4.1 A/B 测试框架

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Callable
from enum import Enum
import random
import hashlib

class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"

@dataclass
class Experiment:
    """A/B 测试实验"""
    experiment_id: str
    name: str
    model_a: str  # 控制组
    model_b: str  # 实验组
    traffic_split: float = 0.5  # 模型 B 的流量比例
    status: ExperimentStatus = ExperimentStatus.DRAFT
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metrics: Dict[str, float] = field(default_factory=dict)

class ABTestFramework:
    """A/B 测试框架"""

    def __init__(self):
        self.experiments: Dict[str, Experiment] = {}

    def create_experiment(
        self,
        name: str,
        model_a: str,
        model_b: str,
        traffic_split: float = 0.5
    ) -> Experiment:
        """创建实验"""
        experiment_id = hashlib.md5(
            f"{name}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:8]

        experiment = Experiment(
            experiment_id=experiment_id,
            name=name,
            model_a=model_a,
            model_b=model_b,
            traffic_split=traffic_split
        )

        self.experiments[experiment_id] = experiment
        return experiment

    def start_experiment(self, experiment_id: str) -> None:
        """启动实验"""
        exp = self.experiments.get(experiment_id)
        if exp:
            exp.status = ExperimentStatus.RUNNING
            exp.start_time = datetime.now()

    def get_model_for_request(
        self,
        experiment_id: str,
        user_id: str
    ) -> str:
        """
        根据用户 ID 决定使用哪个模型
        使用一致性哈希确保同一用户始终分到同一模型
        """
        exp = self.experiments.get(experiment_id)
        if not exp or exp.status != ExperimentStatus.RUNNING:
            return exp.model_a if exp else ""

        # 一致性哈希
        hash_value = int(hashlib.md5(f"{experiment_id}_{user_id}".encode()).hexdigest(), 16)
        bucket = (hash_value % 100) / 100

        if bucket < exp.traffic_split:
            return exp.model_b
        return exp.model_a

    def record_metric(
        self,
        experiment_id: str,
        user_id: str,
        model_used: str,
        metric_name: str,
        metric_value: float
    ) -> None:
        """记录指标"""
        key = f"{experiment_id}_{model_used}_{metric_name}"
        if key not in self.experiments[experiment_id].metrics:
            self.experiments[experiment_id].metrics[key] = 0.0
        self.experiments[experiment_id].metrics[key] += metric_value

    def get_experiment_results(self, experiment_id: str) -> dict:
        """获取实验结果"""
        exp = self.experiments.get(experiment_id)
        if not exp:
            return {}

        model_a_metrics = {
            k.replace(f"{exp.model_a}_", ""): v
            for k, v in exp.metrics.items()
            if k.startswith(exp.model_a)
        }

        model_b_metrics = {
            k.replace(f"{exp.model_b}_", ""): v
            for k, v in exp.metrics.items()
            if k.startswith(exp.model_b)
        }

        return {
            "experiment_id": exp.experiment_id,
            "name": exp.name,
            "status": exp.status.value,
            "model_a": exp.model_a,
            "model_b": exp.model_b,
            "traffic_split": exp.traffic_split,
            "model_a_metrics": model_a_metrics,
            "model_b_metrics": model_b_metrics,
            "improvement": self._calculate_improvement(model_a_metrics, model_b_metrics)
        }

    def _calculate_improvement(
        self,
        metrics_a: dict,
        metrics_b: dict
    ) -> dict:
        """计算改进幅度"""
        improvement = {}
        for key in metrics_a:
            if key in metrics_b and metrics_a[key] != 0:
                improvement[key] = (metrics_b[key] - metrics_a[key]) / metrics_a[key]
        return improvement
```

#### 4.2 模型监控

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from enum import Enum
import numpy as np

class DriftType(Enum):
    DATA_DRIFT = "data_drift"     # 数据漂移
    PREDICTION_DRIFT = "prediction_drift"  # 预测漂移
    CONCEPT_DRIFT = "concept_drift"  # 概念漂移

@dataclass
class MonitoringMetrics:
    """监控指标"""
    timestamp: datetime
    metric_name: str
    value: float
    threshold: float
    is_anomaly: bool = False

@dataclass
class DriftReport:
    """漂移报告"""
    drift_type: DriftType
    feature_name: str
    drift_score: float
    p_value: float
    severity: str  # low, medium, high
    recommendation: str

class ModelMonitor:
    """模型监控系统"""

    def __init__(
        self,
        baseline_data: np.ndarray,
        alert_threshold: float = 0.05
    ):
        self.baseline_data = baseline_data
        self.baseline_stats = self._compute_statistics(baseline_data)
        self.alert_threshold = alert_threshold
        self.alerts: List[DriftReport] = []

    def _compute_statistics(self, data: np.ndarray) -> dict:
        """计算统计信息"""
        return {
            "mean": np.mean(data, axis=0),
            "std": np.std(data, axis=0),
            "median": np.median(data, axis=0),
            "p25": np.percentile(data, 25, axis=0),
            "p75": np.percentile(data, 75, axis=0)
        }

    def detect_data_drift(
        self,
        current_data: np.ndarray,
        feature_name: str = "features"
    ) -> DriftReport:
        """
        检测数据漂移（使用 Population Stability Index）
        """
        # 计算 PSI
        psi = self._calculate_psi(
            self.baseline_data,
            current_data,
            buckets=10
        )

        # 判断严重程度
        if psi < 0.1:
            severity = "low"
        elif psi < 0.2:
            severity = "medium"
        else:
            severity = "high"

        drift_report = DriftReport(
            drift_type=DriftType.DATA_DRIFT,
            feature_name=feature_name,
            drift_score=psi,
            p_value=0.0,  # PSI 不使用 p-value
            severity=severity,
            recommendation=self._get_drift_recommendation(severity)
        )

        if severity == "high":
            self.alerts.append(drift_report)

        return drift_report

    def _calculate_psi(
        self,
        expected: np.ndarray,
        actual: np.ndarray,
        buckets: int = 10
    ) -> float:
        """计算 Population Stability Index"""
        # 分桶
        breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))

        expected_counts = np.histogram(expected, breakpoints)[0]
        actual_counts = np.histogram(actual, breakpoints)[0]

        # 避免除零
        expected_counts = np.where(expected_counts == 0, 1, expected_counts)
        actual_counts = np.where(actual_counts == 0, 1, actual_counts)

        # 计算比例
        expected_pct = expected_counts / len(expected)
        actual_pct = actual_counts / len(actual)

        # 计算 PSI
        psi = np.sum(
            (actual_pct - expected_pct) *
            np.log(actual_pct / expected_pct)
        )

        return psi

    def detect_prediction_drift(
        self,
        baseline_predictions: np.ndarray,
        current_predictions: np.ndarray
    ) -> DriftReport:
        """检测预测漂移"""
        baseline_mean = np.mean(baseline_predictions)
        current_mean = np.mean(current_predictions)

        # 使用相对变化
        drift_score = abs(current_mean - baseline_mean) / (baseline_mean + 1e-6)

        if drift_score < 0.05:
            severity = "low"
        elif drift_score < 0.15:
            severity = "medium"
        else:
            severity = "high"

        return DriftReport(
            drift_type=DriftType.PREDICTION_DRIFT,
            feature_name="predictions",
            drift_score=drift_score,
            p_value=0.0,
            severity=severity,
            recommendation=self._get_drift_recommendation(severity)
        )

    def _get_drift_recommendation(self, severity: str) -> str:
        """获取漂移处理建议"""
        recommendations = {
            "low": "继续监控，无需干预",
            "medium": "考虑收集更多数据，准备模型重训练",
            "high": "立即触发告警，需要紧急模型重训练或回滚"
        }
        return recommendations.get(severity, "")

    def get_monitoring_dashboard(self) -> dict:
        """获取监控仪表板数据"""
        return {
            "total_alerts": len(self.alerts),
            "high_severity_alerts": sum(
                1 for a in self.alerts if a.severity == "high"
            ),
            "recent_alerts": [
                {
                    "type": a.drift_type.value,
                    "feature": a.feature_name,
                    "severity": a.severity,
                    "recommendation": a.recommendation
                }
                for a in self.alerts[-10:]
            ],
            "baseline_stats": self.baseline_stats
        }
```

---

## 🚀 实战案例

### 案例：端到端 MLOps 流程

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import mlflow
import pandas as pd

@dataclass
class MLOpsPipeline:
    """MLOps 完整流程"""
    experiment_name: str
    model_name: str

    def __post_init__(self):
        mlflow.set_experiment(self.experiment_name)

    def run_training_pipeline(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        target_column: str,
        hyperparameters: dict
    ) -> dict:
        """运行完整训练流程"""

        with mlflow.start_run(run_name=f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # 1. 数据准备
            X_train = train_data.drop(columns=[target_column])
            y_train = train_data[target_column]
            X_test = test_data.drop(columns=[target_column])
            y_test = test_data[target_column]

            mlflow.log_param("train_size", len(X_train))
            mlflow.log_param("test_size", len(X_test))
            mlflow.log_param("n_features", X_train.shape[1])

            # 2. 训练模型
            from sklearn.ensemble import GradientBoostingClassifier
            model = GradientBoostingClassifier(**hyperparameters)
            model.fit(X_train, y_train)

            # 3. 评估模型
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

            y_pred = model.predict(X_test)
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average="weighted"),
                "recall": recall_score(y_test, y_pred, average="weighted"),
                "f1": f1_score(y_test, y_pred, average="weighted")
            }

            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)

            # 4. 注册模型
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=self.model_name
            )

            # 5. 记录数据信息
            mlflow.log_dict(
                {"features": list(X_train.columns)},
                "feature_info.json"
            )

            return {"model": model, "metrics": metrics}

    def run_inference(self, model_version: str, input_data: pd.DataFrame) -> list:
        """运行推理"""
        import mlflow.pyfunc

        # 加载最新版本的模型
        model_uri = f"models:/{self.model_name}/{model_version}"
        model = mlflow.pyfunc.load_model(model_uri)

        predictions = model.predict(input_data)
        return predictions.tolist()
```

---

## ✅ 自检清单

完成本课程后，你应该能够：

- [ ] 理解 MLOps 的核心理念和成熟度模型
- [ ] 使用 MLflow 追踪实验和注册模型
- [ ] 构建基于 Feast 的特征存储
- [ ] 实现 A/B 测试框架
- [ ] 设置模型监控和漂移检测
- [ ] 搭建完整的端到端 MLOps 流程

---

## 🔗 相关资源

- [MLflow 官方文档](https://mlflow.org/docs/latest/index.html)
- [Feast 文档](https://docs.feast.dev/)
- [MLOps 最佳实践](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

---

## 🔗 下一步

完成本课程后，你可以：

- 进入 M04: Litestar 框架
- 学习 M05: RAG 深度优化
- 探索 M06: AI Agent 最终项目

---

**最后更新**: 2026-07-18
