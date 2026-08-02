# L48:  数据可视化 - 详细教程

> **课程时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐☆（数据工程）
> **所属阶段**: Stage 5 - 数据工程  
> **课程编号**: L48
> **所属阶段**: Stage 5 - 数据工程
> **预计时长**: 3-4 小时
> **难度**: ⭐⭐⭐⭐☆（数据工程）
> **前置课程**: L48
> **版本**: v1.0
> **最后更新**: 2026-07-23
> **核心版本**: Python 3.13


## 📚 前置知识

**学习本课程前，你应该掌握：**

- **L48**: Pandas 完整实战

**如果你还没有学习以上课程，建议先完成前置课程。**

---

> **课程定位**: Stage 5 数据工程核心 - 数据洞察的视觉呈现  
> **前置要求**: L48 Pandas 完整实战  
> **后续课程**: L48 DuckDB 分析引擎  
> **学习时长**: 4-5 小时

---

---

## 📚 目录

- [第一章：Matplotlib 基础](#第一章matplotlib-基础)
- [第二章：Seaborn 统计可视化](#第二章seaborn-统计可视化)
- [第三章：图表定制化](#第三章图表定制化)
- [第四章：可视化最佳实践](#第四章可视化最佳实践)

---

## 第一章：Matplotlib 基础

### 1.1 折线图 (Line Chart)

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y1, label='sin(x)', linewidth=2)
plt.plot(x, y2, label='cos(x)', linewidth=2, linestyle='--')
plt.xlabel('X 轴')
plt.ylabel('Y 轴')
plt.title('三角函数图')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**适用场景**: 时间序列、趋势变化

---

### 1.2 柱状图 (Bar Chart)

```python
categories = ['A', 'B', 'C', 'D', 'E']
values = [25, 40, 30, 55, 45]

plt.figure(figsize=(8, 6))
plt.bar(categories, values, color='skyblue', edgecolor='black')
plt.xlabel('类别')
plt.ylabel('数值')
plt.title('柱状图示例')
plt.ylim(0, 60)  # 设置 Y 轴范围
plt.show()

# 水平柱状图
plt.barh(categories, values, color='coral')
plt.xlabel('数值')
plt.ylabel('类别')
plt.title('水平柱状图')
plt.show()
```

**适用场景**: 分类数据对比

---

### 1.3 散点图 (Scatter Plot)

```python
x = np.random.randn(100)
y = 2 * x + np.random.randn(100)

plt.figure(figsize=(8, 6))
plt.scatter(x, y, c=y, cmap='viridis', s=50, alpha=0.6, edgecolors='black')
plt.colorbar(label='Y 值')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('散点图 (颜色映射)')
plt.show()
```

**适用场景**: 变量关系、离群点检测

---

### 1.4 直方图 (Histogram)

```python
data = np.random.randn(1000)

plt.figure(figsize=(8, 6))
plt.hist(data, bins=30, color='green', alpha=0.7, edgecolor='black')
plt.xlabel('数值')
plt.ylabel('频数')
plt.title('直方图 - 正态分布')
plt.axvline(data.mean(), color='red', linestyle='--', label=f'均值: {data.mean():.2f}')
plt.legend()
plt.show()
```

**适用场景**: 数据分布

---

### 1.5 饼图 (Pie Chart)

```python
labels = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
sizes = [30, 25, 20, 15, 10]
explode = (0.1, 0, 0, 0, 0)  # 突出第一块

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.title('编程语言使用占比')
plt.axis('equal')  # 保持圆形
plt.show()
```

**适用场景**: 比例展示 (≤7 类)

---

### 1.6 箱线图 (Box Plot)

```python
data = [np.random.normal(0, std, 100) for std in range(1, 4)]

plt.figure(figsize=(8, 6))
plt.boxplot(data, labels=['Group 1', 'Group 2', 'Group 3'])
plt.ylabel('数值')
plt.title('箱线图 - 多组对比')
plt.grid(axis='y', alpha=0.3)
plt.show()
```

**适用场景**: 分布对比、异常值检测

---

## 第二章：Seaborn 统计可视化

### 2.1 快速配置

```python
import seaborn as sns

# 设置主题
sns.set_theme(style='whitegrid')  # 或 'darkgrid', 'white', 'dark', 'ticks'

# 设置调色板
sns.set_palette('pastel')  # 或 'deep', 'muted', 'bright', 'dark'
```

---

### 2.2 热力图 (Heatmap)

```python
import pandas as pd

# 相关系数矩阵
data = pd.DataFrame(np.random.randn(100, 5), columns=list('ABCDE'))
corr = data.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
            vmin=-1, vmax=1, square=True, linewidths=1)
plt.title('相关系数热力图')
plt.show()
```

**适用场景**: 相关性矩阵、混淆矩阵

---

### 2.3 小提琴图 (Violin Plot)

```python
tips = sns.load_dataset('tips')

plt.figure(figsize=(10, 6))
sns.violinplot(x='day', y='total_bill', data=tips, palette='Set2')
plt.title('小提琴图 - 分布对比')
plt.show()
```

**适用场景**: 分布形状对比

---

### 2.4 成对关系图 (Pair Plot)

```python
iris = sns.load_dataset('iris')

sns.pairplot(iris, hue='species', diag_kind='kde', markers=['o', 's', 'D'])
plt.suptitle('鸢尾花数据集 - 成对关系图', y=1.02)
plt.show()
```

**适用场景**: 多变量关系探索

---

### 2.5 分类散点图 (Swarm Plot)

```python
plt.figure(figsize=(10, 6))
sns.swarmplot(x='day', y='total_bill', hue='sex', data=tips, palette='Set1')
plt.title('分类散点图')
plt.show()
```

**适用场景**: 分类数据分布

---

### 2.6 联合分布图 (Joint Plot)

```python
sns.jointplot(x='total_bill', y='tip', data=tips, kind='hex', color='purple')
plt.suptitle('联合分布图', y=1.02)
plt.show()
```

**kind 选项**: `'scatter'`, `'hex'`, `'kde'`, `'reg'`

---

## 第三章：图表定制化

### 3.1 子图布局

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 子图 1: 折线图
axes[0, 0].plot([1, 2, 3, 4], [1, 4, 2, 3])
axes[0, 0].set_title('折线图')

# 子图 2: 柱状图
axes[0, 1].bar(['A', 'B', 'C'], [3, 7, 5], color='orange')
axes[0, 1].set_title('柱状图')

# 子图 3: 散点图
axes[1, 0].scatter(np.random.rand(50), np.random.rand(50), c='green', alpha=0.5)
axes[1, 0].set_title('散点图')

# 子图 4: 直方图
axes[1, 1].hist(np.random.randn(100), bins=20, color='red', alpha=0.7)
axes[1, 1].set_title('直方图')

plt.tight_layout()
plt.show()
```

---

### 3.2 样式定制

```python
# 使用内置样式
plt.style.use('seaborn-v0_8')  # 或 'ggplot', 'fivethirtyeight'

# 自定义样式
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.figsize'] = (10, 6)

# 中文字体支持 (macOS)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 负号显示
```

---

### 3.3 颜色配置

```python
# 颜色映射
cmap = plt.cm.get_cmap('viridis')  # 或 'plasma', 'inferno', 'magma'

# 自定义颜色列表
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

# 使用颜色
plt.scatter(x, y, c=colors[0], s=100)
```

**推荐配色方案**:

- **定性**: `'Set1'`, `'Set2'`, `'Paired'`
- **定量**: `'viridis'`, `'plasma'`, `'coolwarm'`
- **发散**: `'RdBu'`, `'RdYlGn'`

---

### 3.4 标注与文本

```python
x = [1, 2, 3, 4, 5]
y = [2, 4, 3, 5, 6]

plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o')

# 添加文本
plt.text(3, 3.5, '重要点', fontsize=12, color='red')

# 添加箭头标注
plt.annotate('最高点', xy=(5, 6), xytext=(4, 5.5),
             arrowprops=dict(facecolor='black', shrink=0.05))

# 添加水平线
plt.axhline(y=4, color='gray', linestyle='--', label='阈值')

plt.legend()
plt.show()
```

---

## 第四章：可视化最佳实践

### 4.1 选图原则

| 数据类型     | 推荐图表                 | 示例场景                 |
| ------------ | ------------------------ | ------------------------ |
| **时间序列** | 折线图                   | 股票价格、气温变化       |
| **分类对比** | 柱状图                   | 销售额对比、排名         |
| **分布**     | 直方图、箱线图、小提琴图 | 年龄分布、成绩分布       |
| **关系**     | 散点图、热力图           | 身高体重关系、特征相关性 |
| **比例**     | 饼图 (≤7类)、堆叠柱状图  | 市场份额、组成占比       |
| **多变量**   | 成对关系图、平行坐标     | 特征探索、分类问题       |

---

### 4.2 配色最佳实践

```python
# ✅ 色盲友好配色
colorblind_palette = sns.color_palette('colorblind')

# ✅ 定性数据: 对比鲜明
qualitative = sns.color_palette('Set2', 8)

# ✅ 定量数据: 连续渐变
quantitative = sns.color_palette('YlGnBu', as_cmap=True)

# ❌ 避免: 红绿配色 (色盲不友好)
# ❌ 避免: 彩虹色 (Rainbow) - 不适合定量数据
```

---

### 4.3 常见错误

**错误 1: 3D 饼图**

```python
# ❌ 避免 (视觉欺骗)
# plt.pie(..., shadow=True, explode=..., startangle=...)

# ✅ 使用简单 2D 饼图或柱状图
```

**错误 2: 双 Y 轴滥用**

```python
# ❌ 不同量纲强行放一起
# ✅ 使用子图分开展示
```

**错误 3: 过度装饰**

```python
# ❌ 避免: 过多颜色、3D 效果、渐变背景
# ✅ 保持简洁: 最小化非数据墨水
```

---

### 4.4 完整可视化流程

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 数据准备
df = pd.DataFrame({
    'month': range(1, 13),
    'sales': [100, 120, 150, 180, 200, 220, 240, 260, 250, 230, 210, 190],
    'costs': [80, 90, 110, 130, 150, 160, 180, 190, 180, 170, 160, 150],
})

# 2. 设置样式
sns.set_theme(style='whitegrid')
plt.figure(figsize=(12, 6))

# 3. 绘图
plt.plot(df['month'], df['sales'], marker='o', label='销售额', linewidth=2)
plt.plot(df['month'], df['costs'], marker='s', label='成本', linewidth=2)

# 4. 定制
plt.xlabel('月份', fontsize=12)
plt.ylabel('金额 (万元)', fontsize=12)
plt.title('2024年销售与成本趋势', fontsize=14, fontweight='bold')
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(range(1, 13))

# 5. 保存
plt.tight_layout()
plt.savefig('sales_trend.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 🎯 最佳实践总结

## 第七章：大规模数据可视化性能

### 7.1 Datashader 极致性能

```python
import datashader as ds
import datashader.transfer_functions as tf
import pandas as pd

# ❌ 错误：Matplotlib 绘制 1000 万点
import matplotlib.pyplot as plt
df = pd.DataFrame({'x': range(10000000), 'y': range(10000000)})
plt.scatter(df['x'], df['y'])  # 卡死

# ✅ 正确：Datashader 秒级渲染
cvs = ds.Canvas(plot_width=800, plot_height=600)
agg = cvs.points(df, 'x', 'y')
img = tf.shade(agg, cmap=['lightblue', 'darkblue'])
img
```

### 7.2 交互式可视化（Plotly）

```python
import plotly.express as px

# ❌ 错误：静态图表无法交互
plt.plot(df['x'], df['y'])
plt.show()

# ✅ 正确：交互式图表
fig = px.scatter(df, x='x', y='y', hover_data=['category'])
fig.show()
```

### 7.3 GPU 加速可视化（cuDF + cuGraph）

```python
import cudf
import cugraph

# ✅ GPU 加速网络图
G = cugraph.Graph()
G.from_cudf_edgelist(df_edges, source='src', destination='dst')
pagerank = cugraph.pagerank(G)
```

## 🐛 常见错误与调试

### 错误 1: 内存溢出

**症状**: 绘图时内存不足

**原因**:

```python
# ❌ 绘制所有点
plt.scatter(df['x'], df['y'])
```

**解决方案**:

```python
# ✅ 降采样
sample = df.sample(n=10000)
plt.scatter(sample['x'], sample['y'])
```

### 错误 2: 图表不清晰

**症状**: 点太密集看不清

**原因**:

```python
# ❌ alpha=1.0
plt.scatter(df['x'], df['y'], alpha=1.0)
```

**解决方案**:

```python
# ✅ 调整透明度
plt.scatter(df['x'], df['y'], alpha=0.1)
```

### 错误 3: 中文乱码

**症状**: 中文显示为方块

**原因**:

```python
# ❌ 未设置字体
plt.title('中文标题')
```

**解决方案**:

````python
# ✅ 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
---

## ⚠️ 常见错误与大数据可视化优化

### 错误 1: 前端浏览器 OOM - 直接渲染千万级数据

**症状**: 浏览器标签页崩溃，控制台显示 "Out of Memory"

#### ❌ 错误：直接向前端投喂 1000 万散点

```python
import matplotlib.pyplot as plt
import numpy as np

# 生成 1000 万个散点
np.random.seed(42)
x = np.random.randn(10_000_000)
y = np.random.randn(10_000_000)

# ❌ 错误：直接绘制全部数据
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.5)
plt.title('1000 万散点')
plt.savefig('scatter.png', dpi=300)
# 结果: 内存溢出，浏览器崩溃
````

**问题**:

- 1000 万个点 × (x, y, rgba) = 160MB 原始数据
- Matplotlib 渲染为 SVG/PNG：文件 >500MB
- 浏览器加载崩溃

#### ✅ 正确：Datashader 后端像素聚合

```python
import datashader as ds
import datashader.transfer_functions as tf
import pandas as pd

# ✅ 正确：Datashader 服务器端栅格化
df = pd.DataFrame({'x': x, 'y': y})

# 创建画布（指定像素分辨率）
cvs = ds.Canvas(plot_width=800, plot_height=600)

# 聚合为像素网格（服务器端计算）
agg = cvs.points(df, 'x', 'y')

# 渲染为图像（仅传递 800x600 像素）
img = tf.shade(agg, cmap=['lightblue', 'darkblue'])
img
# 结果: 输出 PNG 仅 50KB，浏览器秒开
```

**性能对比**:

| 方法               | 内存占用 | 文件大小 | 浏览器加载 | 渲染时间 |
| ------------------ | -------- | -------- | ---------- | -------- |
| Matplotlib scatter | 2.5GB    | 520MB    | ❌ 崩溃    | N/A      |
| Datashader         | 180MB    | **50KB** | ✅ <1s     | **2.3s** |

**关键点**:

- ✅ 服务器端栅格化（Rasterization）
- ✅ 像素级聚合（每个像素 = 多个数据点）
- ✅ 仅传递图像像素（800×600 = 480K 像素）

---

### 错误 2: Plotly 大数据集 - 前端 JSON 爆炸

**症状**: Plotly 图表加载 5 分钟，最终白屏

#### ❌ 错误：Plotly 传递百万级数据到前端

```python
import plotly.graph_objects as go

# ❌ 错误：Plotly 将全部数据序列化为 JSON
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x[:1_000_000],  # 100 万点
    y=y[:1_000_000],
    mode='markers',
    marker=dict(size=2, opacity=0.5)
))

fig.write_html('plotly_large.html')
# 结果: HTML48 文件 85MB，浏览器加载 5 分钟后白屏
```

**问题**:

- Plotly 将数据序列化为 JSON 嵌入 HTML
- 100 万点 × 2 坐标 × 8 字节 = 16MB 数据
- JSON 编码后 ~85MB
- 浏览器解析 JSON + 渲染 → 性能崩溃

#### ✅ 正确：后端预聚合 + Scattergl

```python
# ✅ 方案 1：降采样到合理数量
from sklearn.cluster import MiniBatchKMeans

# 聚类降采样到 10000 点
kmeans = MiniBatchKMeans(n_clusters=10000, random_state=42)
kmeans.fit(np.column_stack([x[:1_000_000], y[:1_000_000]]))
centers = kmeans.cluster_centers_

fig = go.Figure()
fig.add_trace(go.Scattergl(  # 使用 WebGL48 加速
    x=centers[:, 0],
    y=centers[:, 1],
    mode='markers',
    marker=dict(size=3)
))
fig.write_html('plotly_optimized.html')
# 结果: HTML48 文件 450KB，浏览器秒开

# ✅ 方案 2：六边形分箱（Hexbin）
import plotly.figure_factory as ff

fig = ff.create_hexbin_mapbox(
    data_frame=df.sample(100000),  # 采样
    lat='y', lon='x',
    nx_hexagon=50,  # 六边形网格密度
)
```

**性能对比**:

| 方法               | 数据量 | HTML48 大小 | 加载时间 | 交互性能 |
| ------------------ | ------ | --------- | -------- | -------- |
| Scatter (100万)    | 100万  | 85MB      | 300s     | ❌ 卡顿  |
| Scattergl (降采样) | 1万    | 450KB     | **1s**   | ✅ 流畅  |
| Hexbin             | 10万   | 320KB     | **0.8s** | ✅ 流畅  |

---

### 错误 3: 动态图表未释放 - 内存泄漏

**症状**: Jupyter Notebook 运行 1 小时后占用 8GB 内存

#### ❌ 错误：循环绘制未关闭 Figure

```python
import matplotlib.pyplot as plt
import numpy as np

# ❌ 错误：循环绘制 100 个图表，未释放
for i in range(100):
    plt.figure(figsize=(10, 6))
    data = np.random.randn(10000)
    plt.hist(data, bins=50)
    plt.title(f'Histogram {i}')
    plt.savefig(f'hist_{i}.png')
    # 忘记 plt.close() → Figure 对象未释放

# 结果: 100 个 Figure 对象常驻内存，占用 ~2GB
```

**问题**:

- 每个 Figure 对象占用 ~20MB
- 100 个 Figure × 20MB = 2GB
- Jupyter Notebook 不会自动回收

#### ✅ 正确：使用上下文管理器

```python
# ✅ 方案 1：显式关闭
for i in range(100):
    fig, ax = plt.subplots(figsize=(10, 6))
    data = np.random.randn(10000)
    ax.hist(data, bins=50)
    ax.set_title(f'Histogram {i}')
    fig.savefig(f'hist_{i}.png')
    plt.close(fig)  # 显式释放

# ✅ 方案 2：上下文管理器（推荐）
from contextlib import contextmanager

@contextmanager
def managed_figure(*args, **kwargs):
    """自动管理 Figure 生命周期"""
    fig = plt.figure(*args, **kwargs)
    try:
        yield fig
    finally:
        plt.close(fig)

for i in range(100):
    with managed_figure(figsize=(10, 6)) as fig:
        ax = fig.add_subplot(111)
        data = np.random.randn(10000)
        ax.hist(data, bins=50)
        ax.set_title(f'Histogram {i}')
        fig.savefig(f'hist_{i}.png')
    # 自动释放
```

**内存对比**:

| 方法         | 100 次循环后内存 | 1000 次循环后内存 |
| ------------ | ---------------- | ----------------- |
| 未关闭       | 2.1GB            | 20.8GB → ❌ OOM   |
| plt.close()  | **85MB**         | **92MB**          |
| 上下文管理器 | **80MB**         | **88MB**          |

---

### 错误 4: 子图批量创建 - 循环低效

**症状**: 创建 100 个子图耗时 2 分钟

#### ❌ 错误：循环创建子图

```python
import time

# ❌ 错误：逐个创建子图
start = time.time()
fig = plt.figure(figsize=(20, 20))

for i in range(100):
    ax = fig.add_subplot(10, 10, i+1)  # 每次重新计算布局
    ax.plot(np.random.randn(100))
    ax.set_title(f'Plot {i}')

print(f"循环创建: {time.time() - start:.2f}s")
# 输出: 循环创建: 125.34s
```

**问题**:

- `add_subplot` 每次触发布局重计算
- 100 次调用 = 100 次布局计算
- O(n²) 时间复杂度

#### ✅ 正确：批量创建子图

```python
# ✅ 正确：一次性创建全部子图
start = time.time()
fig, axes = plt.subplots(10, 10, figsize=(20, 20))  # 批量创建

for i, ax in enumerate(axes.flat):
    ax.plot(np.random.randn(100))
    ax.set_title(f'Plot {i}')

print(f"批量创建: {time.time() - start:.2f}s")
# 输出: 批量创建: 3.42s

# 加速比: 125.34 / 3.42 = 36.6x
```

**关键点**:

- ✅ `plt.subplots(nrows, ncols)` 批量创建
- ✅ 一次性计算布局
- ✅ `axes.flat` 扁平化迭代

---

## 🐛 调试技巧

### 1. 内存分析

```python
import matplotlib.pyplot as plt
import gc

# 查看当前 Figure 数量
print(f"活跃 Figure 数: {len(plt.get_fignums())}")

# 强制垃圾回收
gc.collect()
```

### 2. Datashader 调试

```python
# 检查聚合结果
print(agg)
# xarray.DataArray: (600, 800) 像素

# 可视化聚合热力图
import matplotlib.pyplot as plt
plt.imshow(agg.values, cmap='viridis')
plt.colorbar(label='点密度')
```

### 3. Plotly 性能分析

```python
import plotly.io as pio

# 检查 HTML48 大小
fig.write_html('temp.html')
import os
size_mb = os.path.getsize('temp.html') / 1024 / 1024
print(f"HTML48 大小: {size_mb:.2f} MB")

# 超过 10MB → 需要降采样
if size_mb > 10:
    print("⚠️  文件过大，建议降采样")
```

---

plt.rcParams['axes.unicode_minus'] = False
plt.title('中文标题')

````

### ✅ 可视化清单

- [ ] 明确可视化目的 (对比/分布/关系/趋势)
- [ ] 选择合适图表类型
- [ ] 使用色盲友好配色
- [ ] 添加清晰标题和标签
- [ ] 保持简洁 (最小化非数据墨水)
- [ ] 数据与墨水比 >0.7
- [ ] 提供图例和数据源

### ❌ 避坑指南

1. **避免 3D 图表** (除非真有 3 维数据)
2. **饼图 ≤7 类** (否则用柱状图)
3. **避免彩虹色** (定量数据用渐变)
4. **Y 轴从 0 开始** (柱状图必须)
5. **避免过度装饰** (阴影/渐变/3D 效果)

---

## 🔗 延伸阅读

### 相关课程

- **L48 Pandas 完整实战** - 可视化前的数据清洗与聚合
- **L48 DuckDB 分析引擎** - 大数据量分析后再可视化

### 推荐资源

- [Matplotlib 官方文档](https://matplotlib.org/)
- [Seaborn 官方教程](https://seaborn.pydata.org/)
- [《数据可视化基础》- Edward Tufte](https://www.edwardtufte.com/)

---

## 📝 练习题

### 练习 1: 完整仪表板

创建多图表仪表板 (2x2 子图):

- 销售趋势折线图
- 分类销售柱状图
- 相关性热力图
- 利润分布直方图

### 练习 2: Seaborn 探索

使用 `sns.load_dataset('titanic')`:

- 生存率 vs 船舱等级
- 年龄分布 (按性别)
- 成对关系图

### 练习 3: 定制化

重现以下样式:

- 经济学人风格图表
- FiveThirtyEight 风格图表

---

**练习答案**: 参见 `solutions/` 目录

**下一课**: [L48 DuckDB 分析引擎](../L49-duckdb/lesson.md)

## 第十章：性能调优实战

### 10.1 CPU 密集优化

```python
import numpy as np

# ❌ 错误：Python 循环
result = []
for i in range(1000000):
    result.append(i * 2 + 1)

# ✅ 正确：NumPy 向量化
result = np.arange(1000000) * 2 + 1
````

### 10.2 内存优化策略

```python
# ❌ 错误：加载全部数据
df = pd.read_csv('large.csv')

# ✅ 正确：分块处理
for chunk in pd.read_csv('large.csv', chunksize=10000):
    process(chunk)
```

### 10.3 I/O 优化

```python
# ❌ 错误：CSV 格式
df.to_csv('output.csv')

# ✅ 正确：Parquet 压缩
df.to_parquet('output.parquet', compression='snappy')
```

## 第十一章：生产环境部署

### 11.1 配置管理

```python
from pydantic import BaseSettings

# ✅ 使用 Pydantic 管理配置
class Settings(BaseSettings):
    database_url: str
    batch_size: int = 1000
    max_workers: int = 4

    class Config:
        env_file = '.env'

settings = Settings()
```

### 11.2 日志记录

```python
import logging

# ✅ 结构化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("处理开始", extra={'records': len(df)})
logger.error("处理失败", extra={'error': str(e)})
```

### 11.3 监控指标

```python
from prometheus_client import Counter, Histogram

# ✅ 导出 Prometheus 指标
records_processed = Counter('records_processed_total', 'Total records processed')
processing_time = Histogram('processing_seconds', 'Time spent processing')

with processing_time.time():
    result = process_data(df)
    records_processed.inc(len(result))
```

## 第十二章：调试与故障排查

### 12.1 常见陷阱

```python
# ❌ 陷阱 1：隐式类型转换
df['id'] = df['id'].astype(str)  # 可能很慢

# ✅ 正确：在读取时指定类型
df = pd.read_csv('data.csv', dtype={'id': str})
```

### 12.2 调试工具

```python
# ✅ 使用 %prun 分析性能
%prun process_data(df)

# ✅ 使用 %memit 分析内存
%memit df = pd.read_csv('large.csv')
```

### 12.3 故障恢复

```python
import pickle

# ✅ 检查点机制
try:
    with open('checkpoint.pkl', 'rb') as f:
        state = pickle.load(f)
except FileNotFoundError:
    state = {'last_index': 0}

for i in range(state['last_index'], len(data)):
    process(data[i])
    state['last_index'] = i
    if i % 1000 == 0:
        with open('checkpoint.pkl', 'wb') as f:
            pickle.dump(state, f)
```

## 第十三章：高级技巧

### 13.1 并行处理

```python
from concurrent.futures import ProcessPoolExecutor

# ✅ 多进程并行
def process_chunk(chunk):
    return chunk.apply(expensive_function)

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_chunk, chunks))
```

### 13.2 缓存优化

```python
from functools import lru_cache

# ✅ 缓存计算结果
@lru_cache(maxsize=1000)
def expensive_calc(value):
    return complex_operation(value)
```

### 13.3 懒加载

```python
# ✅ 延迟加载数据
class LazyData:
    def __init__(self, path):
        self.path = path
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = pd.read_csv(self.path)
        return self._data
```

## 第十四章：案例研究

### 14.1 案例 1：电商数据处理

```python
# 场景：处理 1 亿条订单数据
# ❌ 错误：全量加载
df = pd.read_csv('orders_100M.csv')

# ✅ 正确：分布式处理
import dask.dataframe as dd
ddf = dd.read_csv('orders_*.csv')
result = ddf.groupby('user_id').agg({'amount': 'sum'}).compute()
```

### 14.2 案例 2：实时数据清洗

```python
# 场景：Kafka 流式数据
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('data_topic')

for message in consumer:
    data = json.loads(message.value)
    cleaned = clean_record(data)
    save_to_db(cleaned)
```

### 14.3 案例 3：大规模特征工程

```python
# 场景：1000 万用户特征
# ✅ 使用 Polars 加速
import polars as pl

df = pl.read_csv('users.csv')
features = df.select([
    pl.col('age') * 2,
    pl.col('income').log(),
    pl.col('category').value_counts()
])
```

## 第十五章：高级可视化

### 15.1 动态图表

```python
import plotly.graph_objects as go

# ✅ 动态更新图表
fig = go.Figure()
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 4, 9]))
fig.update_layout(title='动态图表')
fig.show()
```

### 15.2 3D 可视化

```python
from mpl_toolkits.mplot3d import Axes3D

# ✅ 3D 散点图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['x'], df['y'], df['z'])
```

### 15.3 地理可视化

```python
import folium

# ✅ 交互式地图
m = folium.Map(location=[39.9, 116.4], zoom_start=10)
folium.Marker([39.9, 116.4], popup='北京').add_to(m)
m.save('map.html')
```


## 🔗 下一步


[L49: DuckDB 嵌入式分析](../L49-duckdb/)
