"""
智能体管理器，负责智能体的招募、激活和协调
"""

import os
import json
from typing import Dict, List, Optional, Any, Tuple
import asyncio

from .agent import Agent

class AgentManager:
    """
    智能体招募管理Agent，作为系统的核心协调者
    负责分析患者数据，招募和协调各专科智能体
    """
    def __init__(
        self,
        model_info: str = "gpt-4o",
        temperature: float = 0.5,
        api_key: Optional[str] = None
    ):
        """
        初始化智能体管理器
        
        Args:
            model_info: 使用的语言模型信息
            temperature: 生成文本的随机性参数
            api_key: API密钥（可选）
        """
        self.model_info = model_info
        self.temperature = temperature
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.agents = {}  # 存储所有注册的智能体
        self.active_agents = {}  # 当前激活的智能体
        self.messages = []  # 管理器的消息历史
        
    def register_agent(self, agent_id: str, agent: Agent) -> None:
        """
        注册智能体到管理器
        
        Args:
            agent_id: 智能体唯一标识符
            agent: 智能体实例
        """
        self.agents[agent_id] = agent
        
    def unregister_agent(self, agent_id: str) -> None:
        """
        从管理器注销智能体
        
        Args:
            agent_id: 智能体唯一标识符
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
        if agent_id in self.active_agents:
            del self.active_agents[agent_id]
            
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        获取指定ID的智能体
        
        Args:
            agent_id: 智能体唯一标识符
            
        Returns:
            Optional[Agent]: 智能体实例，如果不存在则返回None
        """
        return self.agents.get(agent_id)
    
    def add_message(self, role: str, content: str) -> None:
        """
        添加消息到管理器的消息历史
        
        Args:
            role: 消息发送者角色
            content: 消息内容
        """
        self.messages.append({"role": role, "content": content})
    
    def clear_messages(self) -> None:
        """清空消息历史"""
        self.messages = []
        
    async def analyze_patient_data(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析患者数据，确定是综合征性还是非综合征性唇腭裂
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            Dict[str, Any]: 分析结果，包括综合征类型和需要激活的智能体
        """
        # 构建分析提示
        prompt = self._build_analysis_prompt(patient_data)
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API进行分析
        analysis_result = await self._call_llm_api()
        
        # 添加分析结果到消息历史
        self.add_message("assistant", analysis_result)
        
        # 解析分析结果
        parsed_result = self._parse_analysis_result(analysis_result)
        
        return parsed_result
    
    def _build_analysis_prompt(self, patient_data: Dict[str, Any]) -> str:
        """
        构建分析提示
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            str: 分析提示
        """
        symptoms = patient_data.get("symptoms", [])
        symptoms_str = ", ".join(symptoms)
        
        medical_history = patient_data.get("medical_history", "")
        
        prompt = f"""
        作为唇腭裂诊断专家，请分析以下患者信息，判断是综合征性还是非综合征性唇腭裂。
        
        患者症状: {symptoms_str}
        
        患者病史: {medical_history}
        
        请根据以上信息，回答以下问题:
        1. 这是综合征性还是非综合征性唇腭裂？请给出判断依据。
        2. 如果是综合征性，可能属于哪种综合征？请列出可能性最高的三种综合征及其置信度（高/中/低）。
        3. 需要激活哪些专科智能体进行进一步分析？请从以下选项中选择：唇腭裂Agent、颅面外科Agent、遗传Agent、外耳Agent、眼科Agent。
        
        请以JSON格式回答，包含以下字段：
        - syndrome_type: "syndromic" 或 "non-syndromic"
        - confidence: 判断的置信度 (high/medium/low)
        - possible_syndromes: 可能的综合征列表（如果是综合征性），每个包含名称和置信度
        - activated_agents: 需要激活的智能体列表
        - reasoning: 推理过程和依据
        """
        
        return prompt
    
    async def _call_llm_api(self) -> str:
        """
        调用语言模型API
        
        Returns:
            str: 语言模型的回复
        """
        # 这里应该实现实际的API调用
        # 简化实现，返回模拟回复
        return """
        {
            "syndrome_type": "syndromic",
            "confidence": "high",
            "possible_syndromes": [
                {"name": "Van der Woude syndrome", "confidence": "high"},
                {"name": "Treacher Collins syndrome", "confidence": "medium"},
                {"name": "Stickler syndrome", "confidence": "low"}
            ],
            "activated_agents": ["唇腭裂Agent", "颅面外科Agent", "遗传Agent"],
            "reasoning": "患者表现出唇腭裂伴随其他系统性异常，包括颅面部特征异常和家族史，符合综合征性唇腭裂的特征。Van der Woude综合征的特征与患者症状高度吻合。"
        }
        """
    
    def _parse_analysis_result(self, analysis_result: str) -> Dict[str, Any]:
        """
        解析分析结果
        
        Args:
            analysis_result: 分析结果文本
            
        Returns:
            Dict[str, Any]: 解析后的分析结果
        """
        try:
            # 提取JSON部分
            json_str = analysis_result.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            
            result = json.loads(json_str)
            return result
        except Exception as e:
            # 解析失败，返回默认结果
            return {
                "syndrome_type": "unknown",
                "confidence": "low",
                "possible_syndromes": [],
                "activated_agents": ["唇腭裂Agent"],
                "reasoning": f"解析分析结果失败: {str(e)}"
            }
    
    async def recruit_agents(self, patient_data: Dict[str, Any]) -> List[str]:
        """
        根据患者数据招募智能体
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            List[str]: 已激活的智能体ID列表
        """
        # 清空当前激活的智能体
        self.active_agents = {}
        
        # 分析患者数据
        analysis_result = await self.analyze_patient_data(patient_data)
        
        # 更新患者数据中的综合征类型
        patient_data["syndrome_type"] = analysis_result.get("syndrome_type", "unknown")
        patient_data["possible_syndromes"] = analysis_result.get("possible_syndromes", [])
        
        # 获取需要激活的智能体列表
        agent_names = analysis_result.get("activated_agents", [])
        
        # 激活智能体
        activated_agent_ids = []
        for agent_id, agent in self.agents.items():
            if agent.role in agent_names or agent.check_activation(patient_data):
                self.active_agents[agent_id] = agent
                activated_agent_ids.append(agent_id)
        
        return activated_agent_ids
    
    async def coordinate_analysis(self, query: str) -> Dict[str, Any]:
        """
        协调各智能体进行分析
        
        Args:
            query: 查询文本
            
        Returns:
            Dict[str, Any]: 综合分析结果
        """
        if not self.active_agents:
            return {
                "status": "error",
                "message": "没有激活的智能体，请先招募智能体",
                "results": {}
            }
        
        # 收集各智能体的分析结果
        analysis_results = {}
        tasks = []
        
        for agent_id, agent in self.active_agents.items():
            tasks.append(self._get_agent_analysis(agent_id, agent, query))
        
        # 并行执行所有智能体的分析
        results = await asyncio.gather(*tasks)
        
        for agent_id, result in results:
            analysis_results[agent_id] = result
        
        # 整合分析结果
        integrated_result = await self._integrate_analysis_results(analysis_results, query)
        
        return {
            "status": "success",
            "message": "分析完成",
            "results": analysis_results,
            "integrated_result": integrated_result
        }
    
    async def _get_agent_analysis(self, agent_id: str, agent: Agent, query: str) -> Tuple[str, str]:
        """
        获取单个智能体的分析结果
        
        Args:
            agent_id: 智能体ID
            agent: 智能体实例
            query: 查询文本
            
        Returns:
            Tuple[str, str]: 智能体ID和分析结果
        """
        try:
            result = await agent.analyze(query)
            return agent_id, result
        except Exception as e:
            return agent_id, f"分析过程中出错: {str(e)}"
    
    async def _integrate_analysis_results(self, analysis_results: Dict[str, str], original_query: str) -> str:
        """
        整合各智能体的分析结果
        
        Args:
            analysis_results: 各智能体的分析结果
            original_query: 原始查询
            
        Returns:
            str: 整合后的分析结果
        """
        # 构建整合提示
        results_text = ""
        for agent_id, result in analysis_results.items():
            agent = self.agents.get(agent_id)
            if agent:
                results_text += f"\n\n{agent.role} ({agent.expertise}) 的分析:\n{result}"
        
        prompt = f"""
        作为唇腭裂多智能体系统的协调者，请整合以下各专科智能体的分析结果，形成最终的诊断和治疗建议。
        
        原始查询: {original_query}
        
        各智能体分析结果:{results_text}
        
        请提供:
        1. 最终诊断（综合征性/非综合征性，具体综合征类型）
        2. 诊断的置信度和依据
        3. 治疗建议
        4. 需要进一步检查的项目
        
        请以结构化的方式回答，便于医生理解和使用。
        """
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API进行整合
        integrated_result = await self._call_llm_api_for_integration()
        
        # 添加整合结果到消息历史
        self.add_message("assistant", integrated_result)
        
        return integrated_result
    
    async def _call_llm_api_for_integration(self) -> str:
        """
        调用语言模型API进行结果整合
        
        Returns:
            str: 语言模型的回复
        """
        # 这里应该实现实际的API调用
        # 简化实现，返回模拟回复
        return """
        # 最终诊断报告
        
        ## 诊断结果
        - **类型**: 综合征性唇腭裂
        - **具体综合征**: Van der Woude综合征
        - **置信度**: 高
        
        ## 诊断依据
        1. 患者表现出典型的唇腭裂症状
        2. 下唇凹陷（特征性表现）
        3. 家族史阳性（常染色体显性遗传模式）
        4. 无明显其他系统异常
        
        ## 治疗建议
        1. **手术治疗**:
           - 3-6个月进行唇裂修复
           - 9-18个月进行腭裂修复
           - 考虑分阶段手术方案
        
        2. **多学科协作**:
           - 口腔颌面外科
           - 语言治疗
           - 遗传咨询
        
        3. **长期随访**:
           - 语言发育监测
           - 牙齿和颌面发育监测
           - 心理支持
        
        ## 进一步检查建议
        1. **遗传检测**: IRF6基因突变分析
        2. **家族成员筛查**: 评估其他家庭成员的风险
        3. **听力评估**: 排除听力问题
        4. **3D颅面CT**: 评估颅面骨骼结构
        
        ## 预后
        在适当的多学科治疗下，预后良好。患者需要长期随访，但大多数患者可以获得良好的功能和美观恢复。
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将管理器转换为字典表示
        
        Returns:
            Dict[str, Any]: 管理器的字典表示
        """
        return {
            "model_info": self.model_info,
            "temperature": self.temperature,
            "agents": {agent_id: agent.to_dict() for agent_id, agent in self.agents.items()},
            "active_agents": list(self.active_agents.keys())
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], agents_data: Dict[str, Dict[str, Any]]) -> 'AgentManager':
        """
        从字典创建管理器
        
        Args:
            data: 管理器的字典表示
            agents_data: 智能体数据字典
            
        Returns:
            AgentManager: 创建的管理器实例
        """
        manager = cls(
            model_info=data.get("model_info", "gpt-4o"),
            temperature=data.get("temperature", 0.5)
        )
        
        # 注册智能体
        for agent_id, agent_data in agents_data.items():
            agent = Agent.from_dict(agent_data)
            manager.register_agent(agent_id, agent)
        
        # 激活指定的智能体
        for agent_id in data.get("active_agents", []):
            if agent_id in manager.agents:
                manager.active_agents[agent_id] = manager.agents[agent_id]
        
        return manager
