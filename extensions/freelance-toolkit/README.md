# Freelance Toolkit — 自由职业接单工具包

> 职业扩展方向：把本课程学到的技术变成**订单**。
> 与其他 `extensions/*` 不同，本目录不是路线图，而是**可直接复制使用的模板**。

## 内容总览

```
freelance-toolkit/
├── README.md                          # 本文件：使用指南
├── templates/
│   ├── 01-quote-tiered.md            # 三档报价单模板（青铜/白银/黄金）
│   ├── 02-simple-contract-cn.md      # 简易服务合同模板（个人独立开发者版）
│   ├── 03-presale-faq.md             # 售前 FAQ 模板（客户最常问的 12 个问题）
│   ├── 04-acceptance-checklist.md    # 验收标准模板
│   ├── 05-payment-comparison.md      # 收款方式对比（国内/国际）
│   ├── 06-portfolio-readme.md        # GitHub 个人主页 README 模板
│   └── 07-cold-outreach.md           # 主动询价话术模板
└── playbooks/
    ├── crawler-playbook.md           # 爬虫接单 Playbook（最易上手）
    ├── api-backend-playbook.md       # API 后端接单 Playbook
    └── rag-knowledge-base-playbook.md # 企业知识库 RAG Playbook
```

## 三档接单方向 ↔ Playbook 对应

| 方向                    | 起步周期 | 报价区间（自行验证） | Playbook                         |
| ----------------------- | -------- | -------------------- | -------------------------------- |
| 网页爬虫 / 数据采集     | 1-2 周   | ¥300–5000/单         | `crawler-playbook.md`            |
| FastAPI 后端 / API 外包 | 3-4 周   | ¥3000–25000/单       | `api-backend-playbook.md`        |
| 企业知识库 RAG          | 1-2 月   | ¥10000–50000/单      | `rag-knowledge-base-playbook.md` |

## 使用方式

### 第一次接单前

按顺序读完三个文件即可：

1. `templates/06-portfolio-readme.md` → 把 GitHub 主页打理一遍
2. `templates/03-presale-faq.md` → 准备好客户问题的标准答案
3. `templates/01-quote-tiered.md` → 准备 3 档套餐定价

### 收到询价后

1. 用 `templates/07-cold-outreach.md` 框架回复（无论是你主动询价还是被动接询）
2. 谈到具体需求时拿 `templates/01-quote-tiered.md` 报价
3. 客户接受后用 `templates/02-simple-contract-cn.md` 走简易合同
4. 交付时按 `templates/04-acceptance-checklist.md` 提供验收清单
5. 收款用 `templates/05-payment-comparison.md` 选最优方式

### 进阶：建立长期客户

每完成一单，复盘三件事：

1. 客户最满意的点是什么？（沉淀到 `case-study.md`）
2. 哪一步最耗时？（下次报价加价 / 优化流程）
3. 客户后续可能要什么？（主动 follow-up，复购率 > 拉新成本）

---

## ⚠️ 重要边界

- 本工具包**不是法律建议**。重要合同请咨询律师。
- 报价区间为**经验范围**，不构成市场承诺。请抽样验证你所在地区的真实成交价。
- 模板使用 CC0 协议，可自由修改商用，不需注明来源。

---

## 配套阅读

- 项目作品集：[projects/01-04](../../projects/)（接单时演示的真实代码）
- 个人品牌：[templates/06-portfolio-readme.md](templates/06-portfolio-readme.md)（GitHub 个人主页 README 模板）
