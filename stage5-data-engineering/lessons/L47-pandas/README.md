# L47: Pandas 完整实战

> **课程编号**: L47  
> **所属阶段**: Stage 5 - 数据工程  
> **预计时长**: 4-5 小时  
> **难度**: ⭐⭐⭐⭐☆ (中高级)

**课程目标**: 掌握 Pandas 2.0+ 高效数据处理与性能优化技术

---

## 📊 数据准备

由于数据文件较大（82MB），需要运行生成脚本：

```bash
cd stage5-data-engineering/lessons/L48-pandas-complete
python data/generate_data.py
```

生成的 `sample_orders.csv` 将用于性能测试和练习。

---

## 🎯 学习目标

完成本课程后，你将能够：

1. ✅ 使用 Pandas 2.0 的 PyArrow 后端加速计算
2. ✅ 掌握向量化操作替代循环
3. ✅ 优化内存使用和数据类型

---

## 📚 课程内容

### 第一部分：Pandas 2.0 新特性

#### 1.1 PyArrow 后端

_(详细代码见 lesson.md)_

#### 1.2 Copy-on-Write (CoW)

_(详细代码见 lesson.md)_

---

### 第二部分：向量化操作

#### 2.1 避免循环

_(详细代码见 lesson.md)_

#### 2.2 高效的条件操作

_(详细代码见 lesson.md)_

#### 2.3 字符串操作向量化

_(详细代码见 lesson.md)_

---

### 第三部分：内存优化

#### 3.1 数据类型优化

_(详细代码见 lesson.md)_

#### 3.2 分类数据

_(详细代码见 lesson.md)_

#### 3.3 稀疏数据

_(详细代码见 lesson.md)_

---

### 第四部分：高效索引和查询

#### 4.1 设置索引

_(详细代码见 lesson.md)_

#### 4.2 MultiIndex

_(详细代码见 lesson.md)_

#### 4.3 query 方法

_(详细代码见 lesson.md)_

---

### 第五部分：分块处理

#### 5.1 读取大文件

_(详细代码见 lesson.md)_

#### 5.2 逐块聚合

_(详细代码见 lesson.md)_

---

### 第六部分：并行计算

#### 6.1 使用 Dask

_(详细代码见 lesson.md)_

#### 6.2 使用 Modin

_(详细代码见 lesson.md)_

---

### 第七部分：性能最佳实践

#### 7.1 链式操作优化

_(详细代码见 lesson.md)_

#### 7.2 使用 eval

_(详细代码见 lesson.md)_

#### 7.3 批量操作

_(详细代码见 lesson.md)_

---

## 📂 课程资源

### 示例代码

- `examples/01_vectorization_pipeline.py` - 向量化数据处理管道
- `examples/02_memory_optimizer.py` - 内存优化工具类

### 练习项目

- `exercises/project_ecommerce_analytics.py` - 电商数据分析项目
  - 难度: ⭐⭐⭐⭐
  - 时长: 2-3 小时
  - 要求: RFM 分析、用户分层、内存优化

### 标准答案

- `solutions/project_ecommerce_analytics.py` - 完整解决方案

### 数据集

- `data/generate_data.py` - 生成订单与产品样例数据
- `data/sample_products.csv` - 小型产品数据（可入库）
- `data/sample_orders.csv` - 100 万行订单数据（约 82MB，**不入 git**，按需生成）
- `data/README.md` - 数据集说明

生成大数据文件：

```bash
cd stage5-data-engineering/lessons/L48-pandas-complete
python data/generate_data.py
```

### 测试

_(详细代码见 lesson.md)_

---

## 🛠️ 前置要求

### 必备知识

- Python 基础
- NumPy 基础
- Pandas 基础操作
- 数据分析基础

### 环境要求

_(详细代码见 lesson.md)_

### 安装依赖

```bash
# 安装 Pandas 和数据处理依赖
uv sync --extra data
```

#### 可选依赖

部分练习示例使用了以下可选依赖：

**pyarrow**（Pandas 2.0 PyArrow 后端）

如果运行测试时看到相关测试被跳过（SKIPPED），可以安装：

```bash
uv pip install pyarrow
# 或使用 uv add
uv add pyarrow
```

**说明**：

- 该依赖**不是必需的**，核心学习路径不受影响
- 安装后可以使用 Pandas 2.0 的 PyArrow 后端（5-50x 性能提升）
- 跳过相关测试不影响课程完成度

---

## 🚀 快速开始

### 1. PyArrow 后端

_(详细代码见 lesson.md)_

### 2. 向量化操作

_(详细代码见 lesson.md)_

### 3. 内存优化

```python
# 优化数据类型
df["category_col"] = df["category_col"].astype("category")
df["int_col"] = df["int_col"].astype("int8")
```

---

## 📝 练习

### 练习 1: 向量化

将循环操作改写为向量化：

- 条件赋值
- 字符串处理
- 数值计算

### 练习 2: 内存优化

优化 DataFrame 内存：

- 类型转换
- 类别数据
- 稀疏数组

### 练习 3: 大文件处理

处理 1GB+ CSV 文件：

- 分块读取
- 逐块聚合
- 结果合并

### 练习 4: 性能对比

对比不同方法性能：

- apply vs 向量化
- 有索引 vs 无索引
- eval vs 标准操作

---

## 🧪 测试

### 性能基准测试

_(详细代码见 lesson.md)_

---

## 📖 参考资料

### 官方文档

- [Pandas 2.0 文档](https://pandas.pydata.org/docs/)
- [PyArrow 集成](https://pandas.pydata.org/docs/user_guide/pyarrow.html)
- [性能优化指南](https://pandas.pydata.org/docs/user_guide/enhancingperf.html)

### 扩展阅读

- [Pandas 性能优化](https://realpython.com/fast-flexible-pandas/)
- [高效 Pandas](https://tomaugspurger.github.io/posts/modern-1-intro/)

---

## 📁 文件导航

| 目录       | 说明     |
| ---------- | -------- |
| examples/  | 示例代码 |
| exercises/ | 练习题   |
| solutions/ | 参考答案 |
| tests/     | 单元测试 |

---

## ✅ 完成标准

- [ ] 完成所有练习题
- [ ] 通过全部测试：`pytest tests/ -v`

---

## 🔗 下一步

[L49: 数据可视化](../L48-visualization/README.md)
