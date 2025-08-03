from typing import List, Dict, Any
from agents.LeadSearchAgent.tools.DataSourceBaseTool import StandardizedLead


class DataStandardizer:
    """数据标准化工具"""
    
    @staticmethod
    def standardize_leads(raw_data: List[Dict[str, Any]], source_name: str) -> List[StandardizedLead]:
        """标准化leads数据"""
        standardized_leads = []
        
        for item in raw_data:
            lead = StandardizedLead(
                name=DataStandardizer._extract_name(item),
                url=DataStandardizer._extract_url(item),
                email=DataStandardizer._extract_email(item),
                industry=DataStandardizer._extract_industry(item),
                source_name=source_name,
                raw_data=item
            )
            standardized_leads.append(lead)
        
        return standardized_leads
    
    @staticmethod
    def _extract_name(item: Dict[str, Any]) -> str:
        """提取公司名称"""
        name_fields = ['company_name', 'name', 'company', 'organization']
        for field in name_fields:
            if item.get(field):
                return str(item[field])
        return ''
    
    @staticmethod
    def _extract_url(item: Dict[str, Any]) -> str:
        """提取公司网址"""
        url_fields = ['website', 'url', 'homepage', 'domain']
        for field in url_fields:
            if item.get(field):
                return str(item[field])
        return ""
    
    @staticmethod
    def _extract_email(item: Dict[str, Any]) -> str:
        """提取联系邮箱"""
        email_fields = ['email', 'contact_email', 'primary_email']
        for field in email_fields:
            if item.get(field):
                return str(item[field])
        return ""
    
    @staticmethod
    def _extract_industry(item: Dict[str, Any]) -> str:
        """提取所属行业"""
        industry_fields = ['industry', 'sector', 'business_type', 'category']
        for field in industry_fields:
            if item.get(field):
                return str(item[field])
        return ""
    
    @staticmethod
    def merge_leads(all_leads: List[List[StandardizedLead]]) -> List[StandardizedLead]:
        """合并多个数据源的leads"""
        merged_leads = []
        # 判断是否重复，用id来判断
        seen_ids = set()
        
        for leads_batch in all_leads:
            for lead in leads_batch:
                lead_id = lead.company_id
                # 简单的去重逻辑：基于公司名称
                if lead and lead_id not in seen_ids:
                    merged_leads.append(lead)
                    seen_ids.add(lead_id)
        
        return merged_leads
    
    @staticmethod
    def filter_leads(leads: List[StandardizedLead], filters: Dict[str, Any]) -> List[StandardizedLead]:
        """根据条件过滤leads"""
        filtered_leads = []
        
        for lead in leads:
            # 检查关键词过滤
            if 'keywords' in filters and filters['keywords']:
                keywords = filters['keywords'].lower().split(',')
                if not any(keyword in lead.name.lower() for keyword in keywords):
                    continue
            
            # 检查行业过滤
            if 'industry' in filters and filters['industry'] and lead.industry:
                if filters['industry'].lower() not in lead.industry.lower():
                    continue
            
            # 检查邮箱黑名单
            if 'email_blacklist' in filters and filters['email_blacklist'] and lead.email:
                blacklist = filters['email_blacklist'].lower().split(',')
                if any(blacklisted in lead.email.lower() for blacklisted in blacklist):
                    continue
            
            filtered_leads.append(lead)
        
        return filtered_leads 