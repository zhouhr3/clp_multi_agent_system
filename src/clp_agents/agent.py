"""
基于MDAgents框架的智能体基类
定义了所有智能体的共同属性和方法
"""

import os
import json
from typing import Dict, List, Optional, Any, Tuple

class Agent:
    """
    智能体基类，所有专科智能体都继承自此类
    """
    def __init__(
        self,
        role: str,
        expertise: str,
        description: str,
        model_info: str = "gpt-4o-mini",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """
        初始化智能体
        
        Args:
            role: 智能体角色名称
            expertise: 智能体专业领域
            description: 智能体详细描述
            model_info: 使用的语言模型信息
            temperature: 生成文本的随机性参数
            api_key: API密钥（可选）
        """
        self.role = role
        self.expertise = expertise
        self.description = description
        self.model_info = model_info
        self.temperature = temperature
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.messages = []
        self.activation_conditions = []
        
    def add_message(self, role: str, content: str) -> None:
        """
        添加消息到智能体的消息历史
        
        Args:
            role: 消息发送者角色（system, user, assistant）
            content: 消息内容
        """
        self.messages.append({"role": role, "content": content})
    
    def clear_messages(self) -> None:
        """清空消息历史"""
        self.messages = []
    
    def add_activation_condition(self, condition: Dict[str, Any]) -> None:
        """
        添加激活条件
        
        Args:
            condition: 激活条件字典，包含条件类型和参数
        """
        self.activation_conditions.append(condition)
    
    def check_activation(self, patient_data: Dict[str, Any]) -> bool:
        """
        检查是否满足激活条件
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            bool: 是否应该激活该智能体
        """
        # 如果没有激活条件，默认不激活
        if not self.activation_conditions:
            return False
        
        # 检查所有激活条件
        for condition in self.activation_conditions:
            condition_type = condition.get("type")
            
            if condition_type == "symptom_present":
                # 检查特定症状是否存在
                symptom = condition.get("symptom")
                if symptom not in patient_data.get("symptoms", []):
                    return False
            
            elif condition_type == "syndrome_type":
                # 检查是否为特定类型的综合征
                syndrome_type = condition.get("syndrome_type")
                if patient_data.get("syndrome_type") != syndrome_type:
                    return False
            
            elif condition_type == "custom":
                # 自定义条件检查函数
                check_func = condition.get("check_function")
                if check_func and not check_func(patient_data):
                    return False
        
        # 所有条件都满足
        return True
    
    async def analyze(self, query: str) -> str:
        """
        分析查询并生成回复
        
        Args:
            query: 查询文本
            
        Returns:
            str: 智能体的回复
        """
        # 添加用户查询到消息历史
        self.add_message("user", query)
        
        # 调用语言模型API获取回复
        # 这里是一个简化的实现，实际应该调用OpenAI API或其他LLM API
        response = await self._call_llm_api()
        
        # 添加回复到消息历史
        self.add_message("assistant", response)
        
        return response
    
    async def _call_llm_api(self) -> str:
        """
        调用语言模型API
        
        Returns:
            str: 语言模型的回复
        """
        # 这里应该实现实际的API调用
        # 简化实现，返回模拟回复
        return f"这是来自{self.role}的回复，基于{self.expertise}专业知识。"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将智能体转换为字典表示
        
        Returns:
            Dict[str, Any]: 智能体的字典表示
        """
        return {
            "role": self.role,
            "expertise": self.expertise,
            "description": self.description,
            "model_info": self.model_info,
            "temperature": self.temperature,
            "activation_conditions": self.activation_conditions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Agent':
        """
        从字典创建智能体
        
        Args:
            data: 智能体的字典表示
            
        Returns:
            Agent: 创建的智能体实例
        """
        agent = cls(
            role=data["role"],
            expertise=data["expertise"],
            description=data["description"],
            model_info=data.get("model_info", "gpt-4o-mini"),
            temperature=data.get("temperature", 0.7)
        )
        
        for condition in data.get("activation_conditions", []):
            agent.add_activation_condition(condition)
        
        return agent
