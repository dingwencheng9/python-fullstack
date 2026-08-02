# 项目 3: Data Intelligence Pipeline — 数据智能流水线

> **难度**: ⭐⭐⭐⭐ | **预计时间**: 10h | **前置项目**: 01-web-scraper

## 项目目标

构建从爬虫数据到分析报告的端到端数据流水线：

```
爬虫 JSON → 清洗 → 特征工程 → DuckDB 分析 → 可视化 → HTML/Markdown 报告
```

## 功能范围

### P0 — 必做

- 读取 `projects/01-web-scraper` 导出的 JSON
- 文本清洗与字段标准化
- 基础特征工程：词数、标题长度、来源域名
- DuckDB 聚合分析
- Markdown 报告生成
- pytest 测试

### P1 — 进阶

- Polars 快速处理大数据集
- 可视化图表输出
- HTML 报告
- 数据质量检查

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行管道

```bash
# 一键运行完整数据流水线（推荐）
bash run.sh

# 或单独生成报告（需先准备好 input JSON）
PYTHONPATH=projects/03-data-intelligence-pipeline uv run python -m pipeline.report \
  --input PATH/TO/scraped.json --output output/report.md
```

### 运行测试

```bash
pytest tests/ -v
```

## 项目结构

```
projects/03-data-intelligence-pipeline/
├── pipeline/
│   ├── ingest.py
│   ├── clean.py
│   ├── features.py
│   ├── analyze.py
│   ├── visualize.py
│   └── report.py
├── tests/
├── data/sample.json
└── reports/
```

## 快速开始

```bash
python -m pytest tests/ -v
python -m pipeline.report data/sample.json reports/report.md
```

## 评分标准

| 维度     | 权重 | 要求               |
| -------- | ---- | ------------------ |
| 数据读取 | 20%  | 支持 JSON/CSV      |
| 数据清洗 | 20%  | 处理空值/重复/异常 |
| 分析能力 | 25%  | DuckDB 聚合分析    |
| 报告输出 | 20%  | Markdown/HTML 报告 |
| 测试     | 15%  | 10+ 测试           |
