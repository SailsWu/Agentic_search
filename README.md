# 智能线索匹配与搜索Agent系统（Workus_01）

本项目是一个基于大模型（LLM）的智能线索匹配与多源线索搜索系统，支持企业客户画像（ICP）与leads的智能匹配、异步多源搜索、数据标准化与持久化，适用于B2B线索挖掘、销售自动化等场景。

---

## 目录结构总览

```
workus_01/
├── agents/
│   ├── base_agent.py                # Agent基类，定义统一异步入口
│   ├── LeadMatchAgent/              # 智能线索匹配主调度模块
│   │   ├── lead_match_agent.py      # 主调度器LeadMatchAgent
│   │   ├── __init__.py              # 包初始化
│   │   ├── prompt_templates/        # Prompt模板
│   │   │   └── match_prompt.txt     # 匹配任务Prompt模板
│   │   └── tools/                   # LeadMatchAgent专用工具
│   │       ├── context_loader.py    # 上下文加载器
│   │       ├── icp_loader.py        # ICP加载器
│   │       ├── llm_client.py        # LLM客户端
│   │       └── result_persister.py  # 匹配结果持久化
│   └── LeadSearchAgent/             # 多数据源线索搜索Agent
│       ├── LeadSearchAgent.py       # 主调度器LeadSearchAgent
│       ├── __init__.py              # 包初始化
│       ├── tools/                   # 搜索工具集合
│       │   ├── clay_tool.py         # Clay数据源工具
│       │   ├── DataSourceBaseTool.py# 数据源工具基类
│       │   └── internal_db_tool.py  # 内部数据库工具
│       └── README.md                # 说明文档
├── configs/
│   └── data_sources.yaml            # 数据源配置
├── main.py                          # 主程序入口
├── match_agent/                     # 早期/兼容版线索匹配模块
│   └── README.md                    # 说明文档
├── raw_data/                        # 原始数据存储
│   └── internaldb.json              # 内部数据库样例
├── results/                         # 匹配/搜索结果存储
├── storage/                         # 预留存储目录
├── tests/                           # 测试用例
│   └── test_match_agent.py          # 匹配Agent测试
├── tools/                           # 通用工具
│   └── test.py                      # 工具测试
├── utils/                           # 数据标准化等工具
│   └── standardizer.py              # 数据标准化
├── requirements.txt                 # 依赖包
└── 说明.txt                         # 项目说明
```

---

## 主要模块与职责

### 1. LeadMatchAgent（智能线索匹配Agent）
- 目录：`agents/LeadMatchAgent/`
- 作用：负责根据客户ICP与leads进行智能匹配，调用大模型判断匹配性，输出结构化结果并持久化。
- 主要组件：
  - `lead_match_agent.py`：主调度类，控制整体流程。
  - `tools/`：包含ICP加载、上下文构建、LLM调用、结果保存等工具。
  - `prompt_templates/`：存放大模型Prompt模板。
- 典型用法：
  ```python
  from agents.LeadMatchAgent.lead_match_agent import LeadMatchAgent
  agent = LeadMatchAgent()
  result = agent.run_sync(customer_id, leads_list)
  ```
- 详细说明见 [`agents/LeadMatchAgent/README.md`](agents/LeadMatchAgent/README.md)

### 2. LeadSearchAgent（多数据源线索搜索Agent）
- 目录：`agents/LeadSearchAgent/`
- 作用：支持异步并发搜索多个外部/内部数据源，自动合并、去重和标准化leads。
- 主要组件：
  - `LeadSearchAgent.py`：主调度类，负责多源调度与结果处理。
  - `tools/`：包含各数据源工具（如Clay、内部DB等）及工具基类。
- 典型用法：
  ```python
  from agents.LeadSearchAgent.LeadSearchAgent import LeadSearchAgent
  agent = LeadSearchAgent("configs/data_sources.yaml")
  result = await agent.run({"icp": icp, "limit": 100})
  ```
- 详细说明见 [`agents/LeadSearchAgent/README.md`](agents/LeadSearchAgent/README.md)

### 3. match_agent（兼容/早期版线索匹配模块）
- 目录：`match_agent/`
- 作用：早期或兼容版的线索匹配实现，结构与LeadMatchAgent类似。
- 详细说明见 [`match_agent/README.md`](match_agent/README.md)

### 4. 通用工具与配置
- `configs/`：数据源与全局配置（如API密钥、数据源开关等）。
- `utils/`：数据标准化、合并、过滤等通用工具。
- `tools/`：通用或测试工具。
- `raw_data/`、`results/`、`storage/`：数据输入输出与中间结果存储。
- `tests/`：测试用例。

---

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据源
编辑 `configs/data_sources.yaml` 文件，配置API密钥和数据源开关：
```yaml
data_sources:
  clay:
    config:
      api_key: "your_clay_api_key"
  linkedin:
    config:
      api_key: "your_linkedin_api_key"
```

### 3. 运行主程序
```bash
python main.py
```

---

## 典型用法示例

### LeadMatchAgent 匹配示例
```python
from agents.LeadMatchAgent.lead_match_agent import LeadMatchAgent
agent = LeadMatchAgent()
input_data = {
    "customer_id": "cus_001",
    "leads_list": [
        {"id": "lead_123", "company_name": "AI科技", "industry": "科技", "company_website": "https://aitech.com", "product_desc": "AI智能客服", "product_keywords": ["AI", "客服"], "contact_name": "李雷", "job_title": "CTO", "region": "中国"}
    ]
}
result = agent.run_sync(input_data["customer_id"], input_data["leads_list"])
print(result)
```

### LeadSearchAgent 搜索示例
```python
from agents.LeadSearchAgent.LeadSearchAgent import LeadSearchAgent
from agents.LeadSearchAgent.tools.DataSourceBaseTool import ICP
agent = LeadSearchAgent("configs/data_sources.yaml")
icp = ICP(industry="technology", company_size="50-200")
result = await agent.run({"icp": icp, "limit": 100})
leads = result["leads"]
```

---

## 扩展性说明

- **添加新数据源**：继承 LeadSearchAgent 的 DataSourceBaseTool，实现搜索接口，并在配置文件注册。
- **Prompt热更新**：可直接修改 prompt_templates/ 下的模板文件，无需重启服务。
- **持久化扩展**：支持本地JSON、数据库、分布式存储等多种持久化方式。
- **多模型支持**：LLMClient 可扩展为支持多种大模型（如OpenAI、Claude、百度千帆等）。
- **模块解耦**：各Agent、工具、配置均高度解耦，便于二次开发和业务集成。

---

## 其他说明

- 所有核心代码均有详细中文注释，便于理解和维护。
- 推荐先阅读各Agent目录下的README文档，了解具体实现与扩展方式。
- 测试用例位于 `tests/` 目录，可参考 `test_match_agent.py`。

---

## 许可证

MIT License 