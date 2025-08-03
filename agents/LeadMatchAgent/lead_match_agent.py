"""
LeadMatchAgent
主调度器，负责智能线索匹配流程控制。
"""
from tools.icp_loader import ICPLoader
from tools.context_loader import ContextLoader
from tools.llm_client import LLMClient
from tools.result_persister import MatchResultPersister
from typing import List, Dict
import datetime
from agents.base_agent import BaseAgent

class LeadMatchAgent(BaseAgent):
    """
    智能线索匹配主调度器
    """
    def __init__(self, icp_loader=None, context_loader=None, llm_client=None, persister=None):
        self.icp_loader = icp_loader or ICPLoader()
        self.context_loader = context_loader or ContextLoader()
        self.llm_client = llm_client or LLMClient()
        self.persister = persister or MatchResultPersister()

    def run_sync(self, customer_id: str, leads_list: List[Dict]) -> List[Dict]:
        """
        执行主流程：对每个lead进行智能匹配，返回结构化结果列表。
        :param customer_id: 客户ID
        :param leads_list: 线索列表，每条为dict
        :return: 匹配结果列表
        """
        icp = self.icp_loader.load(customer_id)
        results = []
        for lead in leads_list:
            context = self.context_loader.load(lead)
            match_result = self.llm_client.match(icp, lead, context)
            result_record = {
                "customer_id": customer_id,
                "lead_id": lead.get("id"),
                **match_result,
                "model": self.llm_client.model_name,
                "prompt_version": self.llm_client.prompt_version,
                "timestamp": datetime.datetime.now().isoformat()
            }
            results.append(result_record)
        self.persister.save_batch(results)
        return results

    async def run(self, input: Dict) -> Dict:
        """
        统一异步入口，兼容 BaseAgent 规范。
        :param input: {"customer_id": str, "leads_list": List[Dict]}
        :return: {"results": List[Dict]}
        """
        customer_id = input.get("customer_id")
        if not customer_id:
            raise ValueError("customer_id 不能为空")
        leads_list = input.get("leads_list", [])
        results = self.run_sync(customer_id, leads_list)
        return {"results": results} 