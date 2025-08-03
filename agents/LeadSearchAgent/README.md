# LeadSearchAgent

## 概述

LeadSearchAgent 是一个多数据源线索搜索代理，支持异步并发搜索多个数据源，并自动合并和去重搜索结果。

## 目录结构

```
LeadSearchAgent/
├── __init__.py                 # 包初始化文件
├── LeadSearchAgent.py          # 主代理类 - 核心调度逻辑
├── tools/                      # 工具模块目录
│   ├── __init__.py            # 工具包初始化
│   ├── clay_tool.py           # Clay数据源工具 - 连接Clay API搜索企业数据
│   ├── DataSourceBaseTool.py  # 数据源基础工具类 - 定义工具接口规范
│   └── internal_db_tool.py    # 内部数据库工具 - 本地JSON数据源
└── README.md                   # 本文档
```

## 文件职责

### LeadSearchAgent.py
- **主代理类**：负责调度和管理所有数据源工具
- **配置管理**：动态加载和初始化数据源配置
- **并发搜索**：异步并发执行多个数据源的搜索任务
- **结果处理**：合并、去重和标准化搜索结果

### tools/DataSourceBaseTool.py
- **接口定义**：定义所有数据源工具必须实现的接口
- **基础框架**：提供工具类的基础功能和规范
- **数据模型**：定义ICP（理想客户画像）和StandardizedLead（标准化线索）数据结构

### tools/clay_tool.py
- **Clay数据源**：连接Clay API进行企业数据搜索
- **企业筛选**：根据ICP条件筛选匹配的企业
- **数据提取**：提取企业基本信息、联系方式、技术栈等

### tools/internal_db_tool.py
- **本地数据源**：从本地JSON数据库读取企业数据
- **离线支持**：提供离线数据源支持，适用于测试环境
- **快速搜索**：支持本地快速搜索和筛选

## 工作流程

1. **初始化**：加载配置文件，动态初始化启用的数据源工具
2. **搜索执行**：异步并发搜索所有可用数据源
3. **结果合并**：自动合并和去重所有数据源的搜索结果
4. **返回结果**：返回标准化的线索数据列表

## 运行方式

### 基本运行
```python
from agents.LeadSearchAgent.LeadSearchAgent import LeadSearchAgent
from agents.LeadSearchAgent.tools.DataSourceBaseTool import ICP

# 创建代理实例
agent = LeadSearchAgent("configs/data_sources.yaml")

# 定义搜索条件
icp = ICP(industry="technology", company_size="50-200")

# 执行搜索
result = await agent.run({"icp": icp, "limit": 100})
leads = result["leads"]
```

### 指定数据源运行
```python
# 只搜索特定数据源
leads = await agent._search_specific_source("clay", icp, 50)
```

### 获取可用数据源
```python
# 查看所有可用数据源状态
sources = agent._get_available_sources()
for source in sources:
    print(f"{source['name']}: {'可用' if source['available'] else '不可用'}")
```

## 扩展方式

- **添加新数据源**：继承DataSourceBaseTool，实现搜索接口
- **配置管理**：在data_sources.yaml中添加新数据源配置
- **动态加载**：系统会自动加载和初始化新添加的数据源工具 