import asyncio
import json
import os
from abc import ABC, abstractmethod
import string
from typing import List, Dict, Any, Optional, Literal, TypedDict
from dataclasses import dataclass, asdict
from pydantic import BaseModel
from dataclasses import field

# 匹配状态离散枚举：未经过大模型的raw数据，经过大模型的scored数据，经过大模型的推荐数据
MatchStatus = Literal["raw","scored","recommended"]

class MatchStatusRecord(TypedDict):
    """状态变更记录结构"""
    from_status:str # 变更前状态
    to_status:str # 变更后状态
    reason:str # 变更原因
    updated_by:str # 变更人
    timestamp:str # 变更时间
    

@dataclass
class StandardizedLead:
    """标准化的Lead数据结构"""
    icp_id: Optional[str] = None # icp_id
    # 公司基本信息
    company_id: Optional[str] = None # 公司id
    company_name: Optional[str] = None # 公司名称
    company_domain: Optional[str] = None # 公司域名
    company_industry: Optional[str] = None # 公司行业
    company_location: Optional[str] = None # 公司位置
    company_country: Optional[str] = None # 公司国家
    company_country_code: Optional[str] = None # 公司国家代码
    company_size: Optional[str] = None # 公司规模

    #联系人信息
    full_name: Optional[str] = None # 联系人全名
    job_title: Optional[str] = None # 联系人职位
    seniority: Optional[str] = None # 联系人职级
    department: Optional[str] = None # 联系人部门
    work_email: Optional[str] = None # 联系人邮箱
    personal_email: Optional[str] = None # 联系人个人邮箱
    language: Optional[str] = None # 联系人语言
    tels: Optional[List[str]] = None # 联系人电话
    facebook: Optional[str] = None # 联系人facebook
    linkedin: Optional[str] = None # 联系人linkedin
    twitter: Optional[str] = None # 联系人twitter
    instagram: Optional[str] = None # 联系人instagram
    youtube: Optional[str] = None # 联系人youtube
    tiktok: Optional[str] = None # 联系人tiktok
    pinterest: Optional[str] = None # 联系人pinterest
    reddit: Optional[str] = None # 联系人reddit
    google_map: Optional[str] = None # 联系人google_map
    line: Optional[str] = None # 联系人line
    whatsapp: Optional[str] = None # 联系人whatsapp
    zalo: Optional[str] = None # 联系人zalo
    telegram: Optional[str] = None # 联系人telegram
    summary: Optional[str] = None # 联系人简介
    educations: Optional[List[str]] = None # 联系人教育经历
    jobs: Optional[List[str]] = None # 联系人工作经历
    
    # Lead拓展上下文
    context: Optional[Dict[str, Any]] = field(default_factory=dict) # 上下文

    # 系统字段（用于评分结果缓存/结果回填）
    lead_score: Optional[float] = None # 评分
    score_detail: Optional[Dict[str, Any]] = None # 大模型输出多维度评分明细
    match_status: Optional[str] = None # 匹配状态
    match_status_history:Optional[List[MatchStatusRecord]] = field(default_factory=list) # 匹配状态历史记录


@dataclass
class ICP:
    """理想客户画像"""
    agent_id: Optional[str] = None # 代理id
    keywords: Optional[List[str]] = None # 关键词列表 
    countries: Optional[List[str]] = None # 国家信息
    sectors: Optional[List[str]] = None # 行业领域
    job_titles: Optional[List[str]] = None # 职位名称
    email_blacklist: Optional[List[str]] = None # 邮箱黑名单
    customer_sources: Optional[List[str]] = None # 客户来源渠道
    company_size: Optional[str] = None # 公司规模


class DataSourceBaseTool(ABC):
    """数据源工具基类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.is_available = self._check_availability()
    
    @abstractmethod
    def _check_availability(self) -> bool:
        """检查工具是否可用"""
        pass
    
    @abstractmethod
    async def search_leads(self, icp: ICP, limit: int = 100) -> List[StandardizedLead]:
        """异步搜索leads"""
        pass
    
    def get_tool_info(self) -> Dict[str, Any]:
        """获取工具信息"""
        return {
            'name': self.name,
            'type': self.config.get('type', 'unknown'),
            'available': self.is_available
        }
    
    def save_raw_data(self, raw_data: Dict[str, Any]) -> str:
        """保存原始数据到本地文件"""
        os.makedirs("raw_data", exist_ok=True)
        filename = f"raw_data/{self.name.lower()}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)
        
        print(f"原始数据已保存到: {filename}")
        return filename 