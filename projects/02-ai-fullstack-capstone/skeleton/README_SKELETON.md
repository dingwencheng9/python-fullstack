# 项目 2 AI Fullstack Capstone 骨架代码使用指南

## 🎯 使用方法

骨架代码是为了帮助你分步实现 AI 全栈应用，关键位置已经留好`TODO`注释，你只需要按照提示补全代码即可。

### 📋 文件结构

```
skeleton/
├── README_SKELETON.md       # 本文件
├── main_skeleton.py         # FastAPI 应用入口骨架
├── config_skeleton.py       # 配置骨架
├── models_skeleton.py       # 数据模型骨架
├── routes/
│   ├── health_skeleton.py   # 健康检查路由骨架
│   ├── documents_skeleton.py # 文档导入路由骨架
│   └── chat_skeleton.py     # 聊天问答路由骨架
└── services/
    ├── storage_skeleton.py  # 存储服务骨架
    ├── vector_store_skeleton.py # 向量存储骨架
    ├── rag_skeleton.py      # RAG 检索骨架
    └── agent_skeleton.py    # Agent 回答生成骨架
```

### 🚀 练习步骤

建议按照以下顺序完成：

#### 第一步：基础结构

1. `config_skeleton.py` - 实现配置加载，从环境变量读取
2. `models_skeleton.py` - 定义 Pydantic 数据模型
3. `main_skeleton.py` - 创建 FastAPI 应用，注册路由，挂载静态文件

#### 第二步：路由实现

1. `routes/health_skeleton.py` - 实现 `/health` 健康检查
2. `routes/documents_skeleton.py` - 实现文档导入 API
3. `routes/chat_skeleton.py` - 实现聊天问答接口，支持 SSE 流式输出

#### 第三步：服务层

1. `services/storage_skeleton.py` - 实现文档持久化存储
2. `services/vector_store_skeleton.py` - 实现内存向量检索
3. `services/rag_skeleton.py` - 实现 RAG 检索逻辑
4. `services/agent_skeleton.py` - 实现 Agent 回答生成，支持 Mock 模式

### ✅ 验证方法

写完后和`app/`目录下的参考实现对比，或者直接运行测试：

```bash
# 运行测试
pytest tests/ -v

# 启动应用
uvicorn app.main:app --reload

# 访问 http://localhost:8000
```

### 💡 知识点提示

**涉及知识点：**

- FastAPI 路由和依赖注入
- Pydantic V2 数据模型
- SSE 流式输出
- HTMX 前端交互
- 向量嵌入和余弦相似度计算
- LangGraph Agent 状态机
- 环境变量配置

### 🎯 挑战练习

完成基础功能后，可以尝试扩展：

1. 集成 Qdrant 向量数据库替换内存存储
2. 增加 WebSocket 全双工聊天
3. 支持文档分块策略配置
4. 增加用户会话和历史对话存储
