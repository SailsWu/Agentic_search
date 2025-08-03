import asyncio
import yaml
import os
import importlib
from typing import List, Dict, Any, Optional
from agents.LeadSearchAgent.tools.DataSourceBaseTool import ICP, StandardizedLead
from utils.standardizer import DataStandardizer
from agents.base_agent import BaseAgent


class LeadSearchAgent(BaseAgent):
    """Lead搜索Agent - 核心调度逻辑"""
    
    def __init__(self, config_path: str = "configs/data_sources.yaml"):
        self.config_path = config_path
        self.tools = {}
        self.config = self._load_config() #加载配置文件
        self._initialize_tools() #初始化所有工具
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"成功加载配置文件: {self.config_path}")
            return config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {"data_sources": {}, "global": {}}
    
    def _initialize_tools(self):
        """初始化所有工具"""
        data_sources = self.config.get('data_sources', {})
        
        for source_id, source_config in data_sources.items():
            # 判断现在这个数据源是否启用
            if not source_config.get('enabled', False):
                continue
            
            tool_class_name = source_config.get('tool_class') # 工具类名
            tool_module_path = source_config.get('module_path') # 工具类所在的模块路径
            if not tool_class_name or not tool_module_path:
                print(f"数据源 {source_id} 缺少工具类名 或 模块路径")
                continue
            
            try:
                # 动态导入工具类
                tool_class = self._import_tool_by_path(tool_module_path, tool_class_name)
                if tool_class:
                    tool = tool_class(source_config['name'], source_config.get('config', {}))
                    self.tools[source_id] = tool
                    print(f"已加载工具: {source_config['name']} ({tool_class_name})")
                else:
                    print(f"无法导入工具类: {tool_class_name}")
                    
            except Exception as e:
                print(f"初始化工具 {source_id} 失败: {e}")
    
    def _import_tool_by_path(self,module_path: str, class_name: str):
        """动态导入工具类"""
        # 根据module_path导入类对象，返回类对象
        try:
            # 导入模块
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        except Exception as e:
            print(f"导入模块失败: {e}")
            return None
    
    async def _search_all_sources(self, icp: ICP, limit_per_source: int = 100) -> List[StandardizedLead]:
        """异步并发搜索所有数据源
        icp:理想客户画像
        limit_per_source: 每个数据源的搜索限制
        """
        # self.tools是一个字典{source_id: tool}
        print(f"开始并发搜索，目标数据源: {len(self.tools)}")
        
        # 创建并发任务
        tasks = []
        for source_id, tool in self.tools.items():
            if tool.is_available:
                #如果tool.is_available为True，则创建一个异步任务，并添加到tasks列表中，返回的是一个协程对象
                task = self._search_single_source(source_id, tool, icp, limit_per_source)
                tasks.append(task)
            else:
                print(f"跳过不可用的数据源: {source_id}")
        
        if not tasks:
            print("没有可用的数据源")
            return []
        
        # 并发执行所有任务，并设置最大并发数
        max_concurrent = self.config.get('global', {}).get('max_concurrent', 4)
        # asyncio.Semaphore是并发令牌桶机制，只允许max_concurrent个任务同时执行
        semaphore = asyncio.Semaphore(max_concurrent)
        
        # 创建一个新函数，用于限制并发数
        async def limited_task(task):
            async with semaphore:
                return await task
        # 用limited_task包装每个任务，限制并发数
        limited_tasks = [limited_task(task) for task in tasks]
        # 并发执行所有封装好的任务，并设置最大并发数；return_exceptions=True表示即使有异常，也继续执行其他任务
        results = await asyncio.gather(*limited_tasks, return_exceptions=True)
        
        # 处理结果
        all_leads = []
        # 遍历每个搜索结果
        for i, result in enumerate(results):
            # 如果result是异常，就记录哪个数据源失败
            if isinstance(result, Exception):
                print(f"数据源 {list(self.tools.keys())[i]} 搜索失败: {result}")
            # 如果result是列表，就说明搜索成功，将其加入总结果集中
            elif isinstance(result, list):
                all_leads.extend(result)
        
        # 将所有数据源返回的leads合并和去重
        merged_leads = DataStandardizer.merge_leads([all_leads])
        print(f"搜索完成，找到 {len(merged_leads)} 个唯一leads")
        # 返回最终的搜索结果
        return merged_leads
    
    async def _search_single_source(self, source_id: str, tool, icp: ICP, limit: int) -> List[StandardizedLead]:
        """搜索单个数据源"""
        try:
            print(f"正在搜索数据源: {source_id}")
            leads = await tool.search_leads(icp, limit)
            print(f"{source_id} 找到 {len(leads)} 个leads")
            return leads
            
        except Exception as e:
            print(f"{source_id} 搜索出错: {e}")
            return []
    
    async def _search_specific_source(self, source_id: str, icp: ICP, limit: int = 100) -> List[StandardizedLead]:
        """搜索指定数据源"""
        if source_id not in self.tools:
            print(f"数据源不存在: {source_id}")
            return []
        
        tool = self.tools[source_id]
        if not tool.is_available:
            print(f"数据源不可用: {source_id}")
            return []
        
        return await self._search_single_source(source_id, tool, icp, limit)
    
    def _get_available_sources(self) -> List[Dict[str, Any]]:
        """获取可用数据源信息"""
        sources = []
        for source_id, tool in self.tools.items():
            sources.append({
                'id': source_id,
                'name': tool.name,
                'available': tool.is_available,
                'info': tool.get_tool_info()
            })
        return sources
    
    def _filter_leads(self, leads: List[StandardizedLead], filters: Dict[str, Any]) -> List[StandardizedLead]:
        """过滤leads"""
        return DataStandardizer.filter_leads(leads, filters) 
    
    async def run(self, input: Dict) -> Dict:
        """执行主流程统一异步入口，兼容 BaseAgent 规范。
        :param input: {"icp": ICP, "limit": int}
        """
        # 获取可用数据源
        available_sources = self._get_available_sources()
        print(f"\n可用数据源 ({len(available_sources)}):")
        for source in available_sources:
            status = "yes" if source['available'] else "no"
            print(f"  {status} {source['name']} ({source['id']})")
        
        icp = input['icp']
        # 异步并发搜索所有数据源
        print(f"\n开始异步并发搜索...")
        leads = await self._search_all_sources(icp, input['limit'])
        return {"leads": leads}