# LeadMatchAgent 目录说明

本目录为智能线索匹配主调度模块，负责线索与客户ICP的智能匹配流程。各文件/子目录说明如下：

## 1. lead_match_agent.py
- 主要内容：LeadMatchAgent 主调度类，继承自 BaseAgent。
- 作用：负责整个线索与客户ICP的智能匹配流程，包括数据加载、上下文构建、调用大模型进行匹配、结果持久化等。
- 主要类/方法：
  - LeadMatchAgent：主调度器类。
  - run_sync：同步执行主流程。
  - run：异步统一入口，兼容 BaseAgent 规范。

## 2. __init__.py
- 主要内容：包初始化文件。
- 作用：用于将 LeadMatchAgent 目录标记为 Python 包，便于模块导入。

## 3. prompt_templates/
- 主要内容：存放大模型提示词模板。
- 作用：用于存放与线索匹配相关的 prompt 模板文件。
- 典型文件：
  - match_prompt.txt：线索匹配任务的 prompt 模板。

## 4. tools/
- 主要内容：LeadMatchAgent 专用工具类集合。
- 作用：为主流程提供数据加载、上下文构建、模型调用、结果保存等功能的工具类。
- 典型文件：
  - context_loader.py：上下文信息加载器，负责为每条线索构建上下文。
  - icp_loader.py：ICP（理想客户画像）加载器，负责加载客户的ICP信息。
  - llm_client.py：大模型客户端，负责与大模型进行交互，实现线索与ICP的智能匹配。
  - result_persister.py：结果持久化工具，负责将匹配结果保存到指定位置。

---

如需详细了解每个类或方法的具体实现，请查阅对应的 Python 源码文件。 