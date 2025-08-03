# LeadMatchAgent（LeadSearchAgent）模块说明

## 模块简介

LeadMatchAgent（也可称为 LeadSearchAgent）是一个基于大模型（LLM）的智能线索匹配与筛选系统。它通过加载客户画像（ICP）、提取线索上下文、构建 Prompt 并调用大模型进行智能判断，最终输出结构化的匹配结果并持久化，支持后续排序、打分与人工复审。

---

## 主要功能流程

1. **加载客户画像（ICP）**：根据 customer_id 获取客户画像信息，包括关键词、行业、职位、公司规模、地区等。
2. **提取线索上下文**：根据 lead 信息提取公司、产品、联系人等上下文信息。
3. **构建 Prompt 并调用大模型**：将 ICP、lead、上下文信息拼接为 Prompt，调用 LLM（如 OpenAI GPT）判断是否匹配。
4. **结构化输出**：输出是否匹配、理由、主要依据字段等结构化结果。
5. **结果持久化**：将所有判断结果批量写入本地 JSON 文件，便于后续分析和复审。

---

## 目录结构

```
match_agent/
  ├── base_agent.py           # Agent基类，定义统一异步入口
  ├── lead_match_agent.py     # 主调度器（LeadMatchAgent/LeadSearchAgent）
  ├── icp_loader.py           # ICP加载模块
  ├── context_loader.py       # 上下文提取模块
  ├── llm_client.py           # LLM调用模块
  ├── result_persister.py     # 结果持久化模块
  └── prompt_templates/
        └── match_prompt.txt  # Prompt模板
```

---

## 主要类与接口说明

### 1. BaseAgent
- 定义所有 Agent 的统一异步入口：`async def run(self, input: Dict) -> Dict`
- 便于多种 Agent 拓展和统一调度

### 2. LeadMatchAgent（LeadSearchAgent）
- 继承 BaseAgent，实现主流程控制
- 支持同步和异步两种调用方式
- 主要方法：
  - `run_sync(customer_id, leads_list)`：同步主流程
  - `async run(input)`：异步统一入口，兼容 BaseAgent

### 3. ICPLoader
- 根据 customer_id 加载客户画像（mock，可扩展为数据库/接口）

### 4. ContextLoader
- 根据 lead 信息提取上下文（mock，可扩展为数据库/接口）

### 5. LLMClient
- 构建 Prompt 并调用大模型 API
- 支持 prompt 模板热更新

### 6. MatchResultPersister
- 批量持久化匹配结果到本地 JSON 文件
- 支持后续扩展为数据库、MongoDB、PostgreSQL 等

---

## 用法示例

```python
from match_agent.lead_match_agent import LeadMatchAgent
import asyncio

agent = LeadMatchAgent()
input_data = {
    "customer_id": "cus_001",
    "leads_list": [
        {"id": "lead_123", "company_name": "AI科技", "industry": "科技", "company_website": "https://aitech.com", "product_desc": "AI智能客服", "product_keywords": ["AI", "客服"], "contact_name": "李雷", "job_title": "CTO", "region": "中国"}
    ]
}

# 异步调用
result = asyncio.run(agent.run(input_data))
print(result)
```

---

## 扩展方式
- 替换 ICPLoader/ContextLoader 的 mock 实现为真实数据库或 API
- 修改 prompt_templates/match_prompt.txt 实现 prompt 热更新
- 持久化可扩展为数据库、分布式存储等
- 支持多模型切换（如 OpenAI、Claude、百度千帆等）

---

## 备注
- 所有核心代码均有详细中文注释，便于理解和维护
- 如需进一步扩展或对接实际业务，请根据各模块注释进行修改 