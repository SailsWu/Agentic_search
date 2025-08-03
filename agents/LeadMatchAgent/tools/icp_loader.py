"""
ICPLoader
负责加载客户画像（ICP）。
"""
from typing import Dict

class ICPLoader:
    """
    客户画像加载器
    """
    def load(self, customer_id: str) -> Dict:
        """
        根据 customer_id 加载客户画像（ICP）。此处为 mock 实现，可扩展为数据库/文件读取。
        :param customer_id: 客户ID
        :return: ICP画像 dict
        """
        # TODO: 可扩展为数据库/文件读取
        return {
            "customer_id": customer_id,
            "keywords": ["AI", "SaaS"],
            "countries": ["中国", "美国"],
            "sectors": ["科技", "软件"],
            "job_titles": ["CTO", "产品经理"],
            "company_size": "100-500人"
        } 