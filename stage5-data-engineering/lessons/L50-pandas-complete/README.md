# L50: Pandas Complete - 进阶数据处理技术

> **课程编号**: L50
> **所属阶段**: Stage 5 - 数据工程
> **预计时长**: 4 小时
> **难度**: ⭐⭐⭐⭐☆
> **前置课程**: L47 Pandas 基础
> **状态**: ✅ 完整版
> **轨道**: CORE
> **版本**: v4.1
> **最后更新**: 2026-07-17

---

## 📌 学习目标

完成本课程后，你将能够：

1. **掌握高级分组聚合**：GroupBy 高级用法、transform、agg 多函数
2. **精通复杂连接操作**：merge、join、concat 高级场景
3. **处理时间序列数据**：重采样、滚动窗口、时区处理
4. **实现窗口函数**：移动统计、累计计算、排名窗口
5. **优化大数据处理**：分块策略、内存映射、加速技巧

---

## 📚 课程内容

### 第一部分：高级分组聚合
- GroupBy 核心概念回顾
- 多层级分组与聚合
- transform 方法
- 过滤分组

### 第二部分：复杂连接操作
- merge 基础回顾
- 多种连接类型
- 复合键连接
- concat 高级用法

### 第三部分：时间序列处理
- DatetimeIndex
- 重采样
- 滚动窗口
- 时区处理

### 第四部分：窗口函数
- Expanding 窗口
- 排名与百分位
- lag/lead 操作

### 第五部分：性能优化
- 分块处理大文件
- category 类型优化
- eval 与 query

---

## 📂 课程资源

### 示例代码

- `examples/01_advanced_groupby.py` - 高级分组聚合示例
- `examples/02_complex_joins.py` - 复杂连接操作示例
- `examples/03_time_series.py` - 时间序列处理示例
- `examples/04_window_functions.py` - 窗口函数示例

### 练习项目

- `exercises/exercise_01_sales_analysis.py` - 销售数据分析
- `exercises/exercise_02_time_series.py` - 时间序列预测
- `exercises/exercise_03_portfolio.py` - 投资组合分析

---

## 🧪 测试

```bash
pytest tests/ -v
```

---

## 📖 参考资料

- [Pandas User Guide: Group By](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Pandas User Guide: Merge](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Pandas User Guide: Time Series](https://pandas.pydata.org/docs/user_guide/timeseries.html)

---

## ✅ 完成标准

- [ ] 完成所有示例代码运行
- [ ] 完成练习项目
- [ ] 通过全部测试

---

## 🔗 下一步

完成本课后继续学习：

- [L51: 异步数据管道](../L51-async-data-pipeline/README.md)

> 📖 **学习路径提示**：L51 将学习异步数据管道的构建。

---

**最后更新**: 2026-07-17
