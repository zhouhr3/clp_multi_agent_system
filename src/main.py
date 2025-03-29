"""
唇腭裂多智能体系统主程序，用于集成所有智能体并演示系统功能
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any

from clp_agents.agent_manager import AgentManager
from clp_agents.knowledge_base import KnowledgeBase
from clp_agents.api_integration import APIIntegration
from clp_agents.cleft_agent import CleftLipPalateAgent
from clp_agents.craniofacial_agent import CraniofacialAgent
from clp_agents.genetic_agent import GeneticAgent
from clp_agents.otology_agent import OtologyAgent
from clp_agents.ophthalmology_agent import OphthalmologyAgent

class CLPAgentSystem:
    """
    唇腭裂多智能体系统，集成所有智能体并提供统一接口
    """
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        初始化唇腭裂多智能体系统
        
        Args:
            api_keys: API密钥字典，键为API名称，值为密钥
        """
        self.api_keys = api_keys or {}
        self.knowledge_base = KnowledgeBase()
        self.agent_manager = AgentManager()
        self.api_integration = None
        
        # 注册所有专科智能体
        self._register_agents()
    
    def _register_agents(self):
        """注册所有专科智能体"""
        # 创建并注册唇腭裂专科智能体
        cleft_agent = CleftLipPalateAgent(
            api_key=self.api_keys.get("openai")
        )
        self.agent_manager.register_agent("cleft_agent", cleft_agent)
        
        # 创建并注册颅面外科智能体
        craniofacial_agent = CraniofacialAgent(
            api_key=self.api_keys.get("openai")
        )
        self.agent_manager.register_agent("craniofacial_agent", craniofacial_agent)
        
        # 创建并注册遗传学智能体
        genetic_agent = GeneticAgent(
            api_key=self.api_keys.get("openai")
        )
        self.agent_manager.register_agent("genetic_agent", genetic_agent)
        
        # 创建并注册外耳智能体
        otology_agent = OtologyAgent(
            api_key=self.api_keys.get("openai")
        )
        self.agent_manager.register_agent("otology_agent", otology_agent)
        
        # 创建并注册眼科智能体
        ophthalmology_agent = OphthalmologyAgent(
            api_key=self.api_keys.get("openai")
        )
        self.agent_manager.register_agent("ophthalmology_agent", ophthalmology_agent)
    
    async def initialize(self):
        """初始化系统，创建API集成实例"""
        self.api_integration = APIIntegration(self.api_keys)
        await self.api_integration.__aenter__()
    
    async def close(self):
        """关闭系统，释放资源"""
        if self.api_integration:
            await self.api_integration.close()
    
    async def analyze_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析患者数据，提供诊断和治疗建议
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 补充患者数据中的综合征相关信息
        if "symptoms" in patient_data:
            # 使用知识库搜索可能的综合征
            possible_syndromes = self.knowledge_base.search_syndromes(patient_data["symptoms"])
            if possible_syndromes:
                patient_data["possible_syndromes"] = [
                    {
                        "name": syndrome["info"]["name"],
                        "confidence": "high" if syndrome["match_percentage"] > 70 else 
                                     "medium" if syndrome["match_percentage"] > 40 else "low"
                    }
                    for syndrome in possible_syndromes[:3]  # 取匹配度最高的前三个
                ]
        
        # 招募智能体
        print("正在招募智能体...")
        activated_agents = await self.agent_manager.recruit_agents(patient_data)
        print(f"已激活的智能体: {activated_agents}")
        
        if not activated_agents:
            return {
                "status": "error",
                "message": "没有智能体被激活，请检查患者数据",
                "results": {}
            }
        
        # 构建分析查询
        query = self._build_analysis_query(patient_data)
        
        # 协调智能体进行分析
        print("正在进行协作分析...")
        analysis_result = await self.agent_manager.coordinate_analysis(query)
        
        # 补充外部医学信息
        if self.api_integration and "syndrome_type" in patient_data:
            syndrome_name = ""
            if patient_data["syndrome_type"] == "syndromic" and patient_data.get("possible_syndromes"):
                syndrome_name = patient_data["possible_syndromes"][0]["name"]
            
            if syndrome_name:
                print(f"正在搜索相关医学文献: {syndrome_name}")
                literature = await self.api_integration.search_literature(f"{syndrome_name} cleft lip palate", 3)
                if literature:
                    analysis_result["literature"] = literature
        
        return analysis_result
    
    def _build_analysis_query(self, patient_data: Dict[str, Any]) -> str:
        """
        构建分析查询
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            str: 分析查询
        """
        age = patient_data.get("age", "未知")
        gender = patient_data.get("gender", "未知")
        symptoms = patient_data.get("symptoms", [])
        symptoms_str = ", ".join(symptoms)
        medical_history = patient_data.get("medical_history", "无")
        
        query = f"""
        请分析以下唇腭裂患者的情况，并提供详细的诊断和治疗建议：
        
        患者基本信息：
        - 年龄：{age}
        - 性别：{gender}
        - 症状：{symptoms_str}
        - 病史：{medical_history}
        
        请根据您的专业领域，提供相关的分析和建议。
        """
        
        return query
    
    async def get_treatment_guidelines(self, condition_id: str) -> Dict[str, Any]:
        """
        获取治疗指南
        
        Args:
            condition_id: 疾病或综合征ID
            
        Returns:
            Dict[str, Any]: 治疗指南
        """
        return self.knowledge_base.get_treatment_guideline(condition_id)
    
    async def search_medical_literature(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        搜索医学文献
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        if not self.api_integration:
            await self.initialize()
        
        return await self.api_integration.search_literature(query, max_results)


async def demo():
    """演示系统功能"""
    # 创建系统实例
    system = CLPAgentSystem()
    
    try:
        # 初始化系统
        await system.initialize()
        
        # 示例患者数据 - 非综合征性唇腭裂
        non_syndromic_patient = {
            "age": "6个月",
            "gender": "男",
            "symptoms": ["唇裂", "腭裂"],
            "medical_history": "足月顺产，无其他异常",
            "family_history": "无家族史"
        }
        
        # 示例患者数据 - 综合征性唇腭裂
        syndromic_patient = {
            "age": "8个月",
            "gender": "女",
            "symptoms": ["唇裂", "腭裂", "下唇凹陷", "缺牙"],
            "medical_history": "足月顺产，发现唇腭裂和下唇凹陷",
            "family_history": "父亲有下唇凹陷"
        }
        
        # 分析非综合征性患者
        print("\n===== 分析非综合征性唇腭裂患者 =====")
        non_syndromic_result = await system.analyze_patient(non_syndromic_patient)
        print("\n非综合征性唇腭裂患者分析结果:")
        print(json.dumps(non_syndromic_result, ensure_ascii=False, indent=2))
        
        # 分析综合征性患者
        print("\n\n===== 分析综合征性唇腭裂患者 =====")
        syndromic_result = await system.analyze_patient(syndromic_patient)
        print("\n综合征性唇腭裂患者分析结果:")
        print(json.dumps(syndromic_result, ensure_ascii=False, indent=2))
        
        # 获取治疗指南
        print("\n\n===== 获取治疗指南 =====")
        guideline = await system.get_treatment_guidelines("van_der_woude_syndrome")
        print("\nVan der Woude综合征治疗指南:")
        print(json.dumps(guideline, ensure_ascii=False, indent=2))
        
        # 搜索医学文献
        print("\n\n===== 搜索医学文献 =====")
        literature = await system.search_medical_literature("Van der Woude syndrome treatment", 3)
        print("\nVan der Woude综合征治疗相关文献:")
        print(json.dumps(literature, ensure_ascii=False, indent=2))
        
    finally:
        # 关闭系统
        await system.close()


if __name__ == "__main__":
    # 运行演示
    asyncio.run(demo())
