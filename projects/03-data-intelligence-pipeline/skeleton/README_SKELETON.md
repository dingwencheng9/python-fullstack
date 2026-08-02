# 项目 3 Data Intelligence Pipeline 骨架代码使用指南

## 🎯 使用方法

骨架代码是为了帮助你分步实现数据智能流水线，关键位置已经留好`TODO`注释，你只需要按照提示补全代码即可。

### 📋 文件说明

```
skeleton/
├── README_SKELETON.md    # 本文件
├── ingest_skeleton.py    # 数据读取骨架
├── clean_skeleton.py     # 数据清洗骨架
├── features_skeleton.py  # 特征工程骨架
├── analyze_skeleton.py   # 数据分析骨架
├── visualize_skeleton.py # 可视化骨架
└── report_skeleton.py    # 报告生成骨架
```

### 🚀 练习步骤

建议按顺序完成：

#### 第一步：数据读取

1. `ingest_skeleton.py` - 实现从 JSON/CSV 读取爬虫输出数据
2. 转换为标准化 DataFrame 格式

#### 第二步：数据清洗

1. `clean_skeleton.py` - 实现文本清洗
2. 处理缺失值
3. 去重
4. 过滤异常数据

#### 第三步：特征工程

1. `features_skeleton.py` - 提取词数特征
2. 提取标题长度特征
3. 提取域名特征
4. 提取日期特征

#### 第四步：数据分析

1. `analyze_skeleton.py` - 用 DuckDB 做聚合分析
2. 统计总页数、平均词数等指标

#### 第五步：可视化（可选）

1. `visualize_skeleton.py` - 生成直方图、条形图

#### 第六步：报告生成

1. `report_skeleton.py` - 生成 Markdown 报告
2. （可选）生成 HTML 报告

### ✅ 验证方法

写完后和`pipeline/`目录下的参考实现对比，或者直接运行测试：

```bash
# 运行测试
pytest tests/ -v

# 运行完整管道
python pipeline/main.py data/sample.json
```

### 💡 知识点提示

**涉及知识点：**

- Pandas / Polars 数据处理
- DuckDB 分析查询
- 正则表达式文本清洗
- Matplotlib / Seaborn 可视化
- 特征工程基础

### 🎯 挑战练习

完成基础功能后，可以尝试扩展：

1. 使用 Polars 替换 Pandas，对比性能
2. 增加数据质量检查规则
3. 支持增量更新（只处理新数据）
4. 自动检测 outliers 并标记
