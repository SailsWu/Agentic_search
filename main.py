#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lead搜索系统主程序
异步并发多数据源搜索
"""

# 新增：智能线索匹配 Agent（Match Agent）模块已集成，详见 match_agent 目录。
import asyncio
import json
from datetime import datetime
from agents.LeadSearchAgent.LeadSearchAgent import LeadSearchAgent
from agents.LeadSearchAgent.tools.DataSourceBaseTool import ICP, StandardizedLead
from dataclasses import asdict

async def test_lead_search_agent():
    """主程序入口"""
    print("启动Lead搜索Agent系统...")
    start_time = datetime.now()
    # 初始化Agent
    lead_search_agent = LeadSearchAgent()
    # 创建ICP
    icp = ICP(
        agent_id="string",
        keywords= ['Apple'],
        countries=["US"],
        sectors=["Wholesale"],
        job_titles=["CEO"],
        email_blacklist=["string"],
        company_size="50",
        customer_sources=["google"]

    )
    lead_search_output = await lead_search_agent.run({"icp": icp,"limit":20})
    leads = lead_search_output["leads"]
    
    
    print(f"\n使用ICP搜索:")
    print(f"  关键词: {icp.keywords}")
    print(f"  国家: {icp.countries}")
    print(f"  行业: {icp.sectors}")
    print(f"  职位: {icp.job_titles}")
    print(f"  公司规模: {icp.company_size}")
    print(f"  客户来源: {icp.customer_sources}")
    print(f"  邮箱黑名单: {icp.email_blacklist}")
    

    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n搜索耗时: {duration:.2f}秒")
    print(f"找到 {len(leads)} 个唯一leads")
    
    # 显示结果
    if leads:
        print(f"\n前5个leads:")
        for i, lead in enumerate(leads[:5]):
            print(f"  {i+1}. {lead.company_name}")
            print(f"     网址: {lead.company_domain or 'N/A'}")
            print(f"     邮箱: {lead.work_email or 'N/A'}")
            print()
        
        # 保存结果
        save_results(leads, icp)
    else:
        print("未找到任何leads")


def save_results(leads, icp):
    """保存搜索结果"""
    # 创建结果目录
    import os
    os.makedirs("results", exist_ok=True)
    
    # 保存标准化结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"results/merged_leads_{icp.agent_id}.json"
    
    results_data = [asdict(lead) for lead in leads]
    # for lead in leads:
    #     standard_lead = StandardizedLead(
    #         icp_id=icp.agent_id,
    #         company_id=lead.get('company_id',None),
    #         company_name=lead.get('company_name',None),
    #         company_domain=lead.get('company_domain',None),
    #         company_industry=lead.get('company_industry',None),
    #         company_location=lead.get('company_location',None),
    #         company_size=lead.get('company_size',None),
    #         # 联系人信息
    #         full_name=lead.get('full_name',None),
    #         job_title=lead.get('job_title',None),
    #         seniority=lead.get('seniority',None),
    #         department=lead.get('department',None),

    #         # 系统字段
    #         match_status="raw"
    #     )
    #     results_data.append(standard_lead)
    # 保存ICP配置
    icp_data = {
        "agent_id":icp.agent_id,
        "keywords": icp.keywords,
        "countries": icp.countries,
        "sectors": icp.sectors,
        "job_titles": icp.job_titles,
        "email_blacklist": icp.email_blacklist,
        "company_size": icp.company_size,
        "customer_sources": icp.customer_sources
    }
    data = {
        "leads": results_data,
        "icp": icp_data
    }
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"标准化结果已保存到: {results_file}")


async def search_specific_source_example():
    """搜索特定数据源示例"""
    print("\n搜索特定数据源示例...")
    
    agent = LeadSearchAgent()
    icp = ICP(keywords=['AI'], countries=['美国'], sectors=['科技'])
    
    # 搜索Clay数据源
    clay_leads = await agent.search_specific_source("clay", icp, limit=10)
    print(f"Clay找到 {len(clay_leads)} 个leads")
    
    # 搜索内部数据库
    db_leads = await agent.search_specific_source("internal_db", icp, limit=10)
    print(f"内部数据库找到 {len(db_leads)} 个leads")


if __name__ == "__main__":
    try:
        # 运行主程序
        asyncio.run(test_lead_search_agent())
        
        # 可选：运行特定数据源搜索示例
        # asyncio.run(search_specific_source_example())
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        raise 