"""
测试智能线索匹配 Agent 主流程
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from match_agent import LeadMatchAgent

def test_run():
    agent = LeadMatchAgent()
    customer_id = "cus_001"
    leads_list = [
        {"id": "lead_123", "company_name": "AI科技", "industry": "科技", "company_website": "https://aitech.com", "product_desc": "AI智能客服", "product_keywords": ["AI", "客服"], "contact_name": "李雷", "job_title": "CTO", "region": "中国"},
        {"id": "lead_456", "company_name": "SaaS软件", "industry": "软件", "company_website": "https://saas.com", "product_desc": "SaaS管理平台", "product_keywords": ["SaaS", "管理"], "contact_name": "韩梅梅", "job_title": "产品经理", "region": "美国"}
    ]
    results = agent.run(customer_id, leads_list)
    for r in results:
        print(r)

if __name__ == "__main__":
    test_run() 