"""
MatchResultPersister
负责持久化匹配结果。
作者：AI助手
"""
from typing import List, Dict
import json
import os

class MatchResultPersister:
    """
    匹配结果持久化器
    """
    def __init__(self, output_path=None):
        self.output_path = output_path or os.path.join(os.path.dirname(__file__), "match_results.json")

    def save_batch(self, results: List[Dict]):
        """
        批量写入匹配结果到本地 JSON 文件。
        :param results: 匹配结果列表
        """
        try:
            if os.path.exists(self.output_path):
                with open(self.output_path, "r", encoding="utf-8") as f:
                    old = json.load(f)
            else:
                old = []
            old.extend(results)
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(old, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"持久化失败: {e}")