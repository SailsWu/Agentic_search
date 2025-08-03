import aiohttp
import asyncio
from typing import List, Dict, Any
from .DataSourceBaseTool import DataSourceBaseTool, ICP, StandardizedLead


class ClaySearchTool(DataSourceBaseTool):
    """Clay数据源工具"""
    
    def _check_availability(self) -> bool:
        """检查Clay API是否可用"""
        api_key = self.config.get('api_key', '')
        return bool(api_key and api_key != "${CLAY_API_KEY}")
    
    async def search_leads(self, icp: ICP, limit: int = 100) -> List[StandardizedLead]:
        """异步搜索leads"""
        if not self.is_available:
            return []
        
        try:
            # 构建搜索参数
            search_params = self._build_search_params(icp, limit)
            
            # 调用Clay API
            raw_data = await self._call_clay_api(search_params)
            
            # 保存原始数据
            self.save_raw_data(raw_data)
            
            # 标准化数据
            standardized_leads = self._standardize_data(raw_data)
            
            return standardized_leads
            
        except Exception as e:
            print(f"Clay搜索出错: {e}")
            return []
    
    def _build_search_params(self, icp: ICP, limit: int) -> Dict[str, Any]:
        """构建Clay搜索参数"""
        params = {
            "limit": limit,
            "filters": {}
        }
        
        if icp.keywords:
            params["filters"]["keywords"] = icp.keywords
        
        if icp.countries:
            params["filters"]["countries"] = icp.countries
        
        if icp.sectors:
            params["filters"]["industries"] = icp.sectors
        
        if icp.company_size:
            params["filters"]["company_size"] = icp.company_size
        
        return params
    
    async def _call_clay_api(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """调用Clay API"""
        api_key = self.config.get('api_key')
        base_url = self.config.get('base_url', 'https://api.clay.com/v1')
        timeout = self.config.get('timeout', 30)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.post(
                f"{base_url}/search",
                headers=headers,
                json=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('results', [])
                else:
                    print(f"Clay API错误: {response.status}")
                    return []
    
    def _standardize_data(self, raw_data: List[Dict[str, Any]]) -> List[StandardizedLead]:
        """标准化Clay数据"""
        standardized_leads = []
        
        for item in raw_data:
            lead = StandardizedLead(
                name=item.get('company_name', ''),
                url=item.get('website'),
                email=item.get('email'),
                industry=item.get('industry'),
                source_name=self.name,
                raw_data=item
            )
            standardized_leads.append(lead)
        
        return standardized_leads 