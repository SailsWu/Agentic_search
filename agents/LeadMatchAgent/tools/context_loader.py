"""
ContextLoader
负责提取 lead 上下文信息。

"""
from typing import Dict

class ContextLoader:
    """
    上下文信息提取器
    """
    def load(self, lead: Dict) -> Dict:
        """
        根据 lead 信息提取上下文（公司、产品、联系人等）。此处为 mock 实现。
        :param lead: 线索 dict
        :return: 上下文 dict
        """
        # TODO: 可扩展为数据库/API读取
        return {
            "company": {
                "name": lead.get("company_name", "未知公司"),
                "industry": lead.get("industry", "科技"),
                "website": lead.get("company_website", "https://example.com")
            },
            "product": {
                "desc": lead.get("product_desc", "AI智能产品"),
                "keywords": lead.get("product_keywords", ["AI", "智能"])
            },
            "contact": {
                "name": lead.get("contact_name", "张三"),
                "job_title": lead.get("job_title", "CTO"),
                "region": lead.get("region", "中国")
            }
        } 