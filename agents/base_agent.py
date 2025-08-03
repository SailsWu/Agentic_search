
from typing import Dict, Any
import abc

class BaseAgent(abc.ABC):
    """
    智能Agent基类，所有Agent应继承本类，实现统一接口。
    """
    @abc.abstractmethod
    async def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一异步入口方法。
        :param input: 结构化输入（如参数字典）
        :return: 结构化输出（如结果字典）
        """
        pass 