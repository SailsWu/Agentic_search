"""
LLMClient
负责 prompt 构建与大模型 API 调用。
"""
from typing import Dict
import openai
import os

class LLMClient:
    """
    大模型调用客户端
    """
    def __init__(self, model_name="gpt-3.5-turbo", prompt_version="v1.2"):
        self.model_name = model_name
        self.prompt_version = prompt_version
        self.prompt_template_path = os.path.join(os.path.dirname(__file__), "prompt_templates", "match_prompt.txt")

    def _load_prompt_template(self) -> str:
        """
        加载 prompt 模板，可热更新。
        """
        try:
            with open(self.prompt_template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            # 默认模板
            return "请根据客户画像与线索上下文，判断是否匹配，并说明理由。"

    def match(self, icp: Dict, lead: Dict, context: Dict) -> Dict:
        """
        构建 prompt 并调用大模型 API，返回结构化判断结果。
        :param icp: 客户画像 dict
        :param lead: 线索 dict
        :param context: 上下文 dict
        :return: {qualified, reason, source}
        """
        prompt = self._build_prompt(icp, lead, context)
        # 调用 OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            content = response["choices"][0]["message"]["content"]
            # 简单结构化解析（实际可用正则/JSON等）
            qualified = "是" in content or "匹配" in content
            return {
                "qualified": qualified,
                "reason": content,
                "source": "自动解析"
            }
        except Exception as e:
            return {
                "qualified": False,
                "reason": f"模型调用失败: {e}",
                "source": "异常"
            }

    def _build_prompt(self, icp: Dict, lead: Dict, context: Dict) -> str:
        """
        构建 prompt 内容。
        """
        template = self._load_prompt_template()
        return template.format(icp=icp, lead=lead, context=context) 