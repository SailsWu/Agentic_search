import sqlite3
import asyncio
import aiohttp
from typing import List, Dict, Any
from .DataSourceBaseTool import DataSourceBaseTool, ICP, StandardizedLead
import requests
import traceback
import json

class InternalDBTool(DataSourceBaseTool):
    """内部数据库工具"""
    
    def _check_availability(self) -> bool:
        """检查API是否可用"""
        return True
    
    async def search_leads(self, icp: ICP, limit: int = 100) -> List[StandardizedLead]:
        """异步搜索leads"""
        if not self.is_available:
            return []
        
        try:
            # 构建查询条件
            query_conditions = self._build_query_conditions(icp, limit)
            # 查询数据库
            raw_data = await self._query_database(query_conditions)
            
            # 保存原始数据
            self.save_raw_data(raw_data)
            
            # 标准化数据
            standardized_leads = self._standardize_data(raw_data, icp)
            
            return standardized_leads
            
        except Exception as e:
            print(f"内部数据库搜索出错: {e}")
            print(f"内部数据库搜索出错: {traceback.print_exc()}")
            return []
    
    def _build_query_conditions(self, icp: ICP, limit: int) -> Dict[str, Any]:
        """构建查询条件"""
        conditions = {}
        if icp.agent_id:
            conditions['agent_id'] = icp.agent_id        
        if icp.sectors:
            conditions['company_type'] = icp.sectors
        if icp.keywords:
            conditions['products_keywords'] = icp.keywords
        if icp.countries:
            conditions['countries'] = icp.countries
        if icp.email_blacklist:
            conditions['blacklinks'] = icp.email_blacklist
        if icp.job_titles:
            conditions['job_title'] = icp.job_titles
        conditions['product_industry'] = []
        conditions['expect_cnt'] = 10
        conditions['limit'] = limit
        conditions['offset'] = 0
        if icp.customer_sources:
            conditions['source'] = icp.customer_sources
        return conditions
    
    async def _query_database(self, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """查询数据库"""
        base_url = self.config.get('base_url', 'http://120.26.142.54/api/contacts/getAgentContacts')
        headers = {
            "Content-Type": "application/json",
        }
        timeout = self.config.get('timeout', 60)
        try:
            response = requests.post(base_url, headers=headers, json=conditions, timeout=timeout)
            if response.status_code == 200:
                print("状态码：", response.status_code)
                print(response.text)
                return response.json()
            else:
                raise RuntimeError(f"InternalDB API错误: {response.status_code}，详情: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
        
        # 异步请求失败，采用同步请求
        # async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
        #     async with session.post(
        #         f"{base_url}",
        #         headers=headers,
        #         json=payload
        #     ) as response:
        #         if response.status == 200:
        #             data = await response.json()
        #             print("完整响应：", json.dumps(data, indent=2))
        #             return data.get('results', [])
        #         else:
        #             error_data = await response.text()
        #             print(f"InternalDB API错误: {response.status}")
        #             print(f"InternalDB API错误: {error_data}")
        #             print(conditions)
        #             raise RuntimeError(f"InternalDB API错误: {response.status}，详情: {error_data}")
    
    def _standardize_data(self, raw_data: Dict[str, Any], icp: ICP) -> List[StandardizedLead]:
        """标准化内部数据库数据"""
        standardized_leads = []
        all_leads = raw_data.get('contacts', [])
        print(all_leads)
        for lead in all_leads:
            standard_lead = StandardizedLead(
            icp_id=icp.agent_id,
            company_id=lead.get('company_id',None),
            company_name=lead.get('company_name',None),
            company_domain=lead.get('company_domain',None),
            company_industry=lead.get('company_industry',None),
            company_location=lead.get('company_location',None),
            company_size=lead.get('company_size',None),
            company_country=lead.get('company_country',None),
            company_country_code=lead.get('company_country_code',None),
            
    
            # 联系人信息
            full_name=lead.get('full_name',None),
            job_title=lead.get('job_title',None),
            seniority=lead.get('seniority',None),
            department=lead.get('department',None),
            work_email=lead.get('work_email',None),
            personal_email=lead.get('personal_email',None),
            language=lead.get('language',None),
            tels=lead.get('tels',None),
            facebook=lead.get('facebook',None),
            linkedin=lead.get('linkedin',None),
            twitter=lead.get('twitter',None),
            instagram=lead.get('instagram',None),
            youtube=lead.get('youtube',None),
            tiktok=lead.get('tiktok',None),
            pinterest=lead.get('pinterest',None),
            reddit=lead.get('reddit',None),
            google_map=lead.get('google_map',None),
            line=lead.get('line',None),
            whatsapp=lead.get('whatsapp',None),
            zalo=lead.get('zalo',None),
            telegram=lead.get('telegram',None),
            summary=lead.get('summary',None),
            educations=lead.get('educations',None),
            jobs=lead.get('jobs',None),

            # 系统字段
            match_status="raw"
          )
        standardized_leads.append(standard_lead)

        # for item in raw_data:
        #     lead = StandardizedLead(
        #         name=item.get('company_name', ''),
        #         url=item.get('website'),
        #         email=item.get('email'),
        #         industry=item.get('industry'),
        #         source_name=self.name,
        #         raw_data=item
        #     )
        #     standardized_leads.append(lead)
        
        return standardized_leads 
