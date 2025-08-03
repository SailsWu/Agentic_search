import requests
from agents.LeadSearchAgent.tools.internal_db_tool import  InternalDBTool
def test1():
    url = "http://120.26.142.54/api/contacts/getAgentContacts"  #
    headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_TOKEN_HERE"  # 如有鉴权
    }
    payload = {
    "agent_id": "string",
    "company_type": [
    "Wholesale"
    ],
    "products_keywords": [
        "Apple"
    ],
    "countries": [
        "US"
    ],
  "blacklinks": [
    "string",
    "string"
  ],
  "job_title": [
    "CEO"
  ],
  "product_industry": [],
  "expect_cnt": 10,
  "limit": 10,
  "offset": 0,
  "source": [
    "google"
  ]
}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        print("状态码：", response.status_code)
        print("响应内容：", response.json())
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
def test2():
    internal_db_tool = InternalDBTool(name="internal_db_tool", config={})
    leads = internal_db_tool._query_database(conditions={"agent_id": "string"}, limit=10)
    print(leads)
if __name__ == "__main__":
    test2()
