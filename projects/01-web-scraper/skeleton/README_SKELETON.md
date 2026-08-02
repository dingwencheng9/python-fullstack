# 项目1 Web Scraper 骨架代码使用指南

## 🎯 使用方法

骨架代码是为了帮助你分步实现爬虫功能，关键位置已经留好`TODO`注释，你只需要按照提示补全代码即可。

### 📋 文件说明

```
skeleton/
├── collector_skeleton.py   # 采集器骨架
└── pipeline_skeleton.py    # 数据管道骨架
```

### 🚀 练习步骤

#### 第一步：实现`collector_skeleton.py`

建议按以下顺序完成：

1. 先写`__init__`方法，初始化所有属性
2. 实现`_rate_limit`限速功能
3. 实现`_extract_title`和`_extract_text`解析功能
4. 实现`_should_follow`链接判断
5. 实现`fetch`单页采集
6. 最后实现`crawl`广度优先爬取

#### 第二步：实现`pipeline_skeleton.py`

建议按以下顺序完成：

1. 先写`__init__`方法，连接数据库并建表
2. 实现`clean_text`文本清洗
3. 实现`extract_date`日期提取
4. 实现`save`单条数据存储
5. 实现`save_batch`批量存储
6. 实现`analyze`统计分析
7. 最后实现`export_json`和`export_csv`导出功能

### ✅ 验证方法

写完后和`scraper/`目录下的参考实现对比，或者直接运行测试：

```bash
# 运行测试
pytest tests/ -v

# 运行你写的爬虫
python main.py --url https://example.com --output test.json
```

### 💡 知识点提示

#### Collector 涉及知识点：

- HTTP请求：`requests.get()`的使用
- HTML解析：`BeautifulSoup`的使用
- 队列和广度优先搜索
- 正则表达式
- 时间控制：`time.sleep()`

#### Pipeline 涉及知识点：

- 数据库操作：`DuckDB` SQL语法
- 数据清洗：正则表达式
- 数据导出：`pandas` JSON/CSV导出
- 类型注解：Python 3.13 类型系统

### 🎯 挑战练习

完成基础功能后，可以尝试扩展：

1. 支持异步请求（用`aiohttp`替换`requests`）
2. 增加代理IP支持
3. 增加布隆过滤器去重
4. 支持分布式爬取（用Redis做队列）
