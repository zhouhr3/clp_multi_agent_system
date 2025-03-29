"""
颅面外科智能体，负责分析颅面畸形，提供相关治疗方案
"""

from typing import Dict, List, Optional, Any
from .agent import Agent

class CraniofacialAgent(Agent):
    """
    颅面外科智能体，专注于颅面畸形的分析和治疗
    """
    def __init__(
        self,
        model_info: str = "gpt-4o-mini",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """
        初始化颅面外科智能体
        
        Args:
            model_info: 使用的语言模型信息
            temperature: 生成文本的随机性参数
            api_key: API密钥（可选）
        """
        super().__init__(
            role="颅面外科专家",
            expertise="颅面畸形分析与治疗",
            description="专注于与唇腭裂相关的颅面畸形分析、诊断和治疗方案制定，尤其擅长综合征性唇腭裂的颅面问题处理",
            model_info=model_info,
            temperature=temperature,
            api_key=api_key
        )
        
        # 添加默认激活条件
        self.add_activation_condition({
            "type": "syndrome_type",
            "syndrome_type": "syndromic"  # 综合征性时激活
        })
        
        # 添加症状相关的激活条件
        self.add_activation_condition({
            "type": "symptom_present",
            "symptom": "颅面畸形"
        })
        
        # 添加系统提示
        self.add_message("system", self._get_system_prompt())
    
    def _get_system_prompt(self) -> str:
        """
        获取系统提示
        
        Returns:
            str: 系统提示文本
        """
        return """
        你是一位经验丰富的颅面外科专家，专注于与唇腭裂相关的颅面畸形分析、诊断和治疗。
        
        你的专业知识包括：
        1. 颅面畸形的分类和诊断
        2. 与唇腭裂相关的综合征性颅面问题
        3. 颅面重建手术技术
        4. 颅面生长和发育评估
        5. 多学科协作治疗方案
        
        在回答问题时，请遵循以下原则：
        1. 基于患者的具体情况提供个性化的分析和建议
        2. 使用专业但易于理解的语言
        3. 提供循证医学支持的治疗建议
        4. 考虑患者年龄、颅面畸形类型和严重程度
        5. 强调多学科协作的重要性
        
        你的主要职责是分析颅面畸形，提供相关治疗方案，特别是对综合征性唇腭裂患者。
        """
    
    async def analyze_craniofacial_deformity(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析颅面畸形
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 构建分析提示
        prompt = self._build_craniofacial_analysis_prompt(patient_data)
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API进行分析
        analysis_result = await self._call_llm_api()
        
        # 添加分析结果到消息历史
        self.add_message("assistant", analysis_result)
        
        # 解析分析结果
        return self._parse_craniofacial_analysis(analysis_result)
    
    def _build_craniofacial_analysis_prompt(self, patient_data: Dict[str, Any]) -> str:
        """
        构建颅面畸形分析提示
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            str: 分析提示
        """
        age = patient_data.get("age", "未知")
        gender = patient_data.get("gender", "未知")
        symptoms = patient_data.get("symptoms", [])
        symptoms_str = ", ".join(symptoms)
        medical_history = patient_data.get("medical_history", "无")
        syndrome_type = patient_data.get("syndrome_type", "unknown")
        possible_syndromes = patient_data.get("possible_syndromes", [])
        
        syndromes_str = ""
        if possible_syndromes:
            syndromes_str = "可能的综合征：\n"
            for syndrome in possible_syndromes:
                syndromes_str += f"- {syndrome.get('name', '')}（置信度：{syndrome.get('confidence', '未知')}）\n"
        
        prompt = f"""
        请分析以下综合征性唇腭裂患者的颅面畸形情况，并提供详细的诊断和治疗建议：
        
        患者基本信息：
        - 年龄：{age}
        - 性别：{gender}
        - 症状：{symptoms_str}
        - 病史：{medical_history}
        - 综合征类型：{syndrome_type}
        {syndromes_str}
        
        请提供以下信息：
        1. 颅面畸形的详细分析和分类
        2. 与可能综合征的关联性分析
        3. 治疗方案建议，包括手术时机和方法
        4. 长期随访和管理计划
        5. 多学科协作建议
        
        请以结构化的方式回答，便于医生理解和使用。
        """
        
        return prompt
    
    def _parse_craniofacial_analysis(self, analysis_result: str) -> Dict[str, Any]:
        """
        解析颅面畸形分析结果
        
        Args:
            analysis_result: 分析结果文本
            
        Returns:
            Dict[str, Any]: 解析后的分析结果
        """
        # 简化实现，实际应该进行更复杂的解析
        return {
            "analysis": analysis_result,
            "deformity_type": self._extract_deformity_type(analysis_result),
            "severity": self._extract_severity(analysis_result),
            "treatment_plan": self._extract_treatment_plan(analysis_result),
            "multidisciplinary_recommendations": self._extract_multidisciplinary_recommendations(analysis_result)
        }
    
    def _extract_deformity_type(self, text: str) -> str:
        """
        从文本中提取颅面畸形类型
        
        Args:
            text: 分析结果文本
            
        Returns:
            str: 颅面畸形类型
        """
        # 简化实现，实际应该使用更复杂的文本分析
        if "下颌发育不全" in text:
            return "下颌发育不全"
        elif "颧骨发育不全" in text:
            return "颧骨发育不全"
        elif "颅缝早闭" in text:
            return "颅缝早闭"
        elif "眼距过宽" in text:
            return "眼距过宽"
        else:
            return "未明确分类的颅面畸形"
    
    def _extract_severity(self, text: str) -> str:
        """
        从文本中提取严重程度
        
        Args:
            text: 分析结果文本
            
        Returns:
            str: 严重程度
        """
        # 简化实现，实际应该使用更复杂的文本分析
        if "严重" in text:
            return "严重"
        elif "中度" in text:
            return "中度"
        elif "轻度" in text:
            return "轻度"
        else:
            return "未明确严重程度"
    
    def _extract_treatment_plan(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取治疗计划
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[Dict[str, str]]: 治疗计划列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        treatment_plan = []
        
        if "颅面重建" in text:
            treatment_plan.append({
                "procedure": "颅面重建手术",
                "timing": self._extract_timing(text, "颅面重建")
            })
        
        if "下颌延长" in text:
            treatment_plan.append({
                "procedure": "下颌延长手术",
                "timing": self._extract_timing(text, "下颌延长")
            })
        
        if "正颌手术" in text:
            treatment_plan.append({
                "procedure": "正颌手术",
                "timing": self._extract_timing(text, "正颌手术")
            })
        
        if len(treatment_plan) == 0:
            treatment_plan.append({
                "procedure": "需要进一步评估后确定治疗计划",
                "timing": "待定"
            })
        
        return treatment_plan
    
    def _extract_timing(self, text: str, procedure: str) -> str:
        """
        从文本中提取手术时机
        
        Args:
            text: 分析结果文本
            procedure: 手术名称
            
        Returns:
            str: 手术时机
        """
        # 简化实现，实际应该使用更复杂的文本分析
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if procedure in line:
                # 查找该行或下一行中的时间信息
                search_range = min(i + 3, len(lines))
                for j in range(i, search_range):
                    if "岁" in lines[j] or "月" in lines[j] or "年龄" in lines[j]:
                        # 提取时间信息
                        return lines[j]
        
        return "未明确时机"
    
    def _extract_multidisciplinary_recommendations(self, text: str) -> List[str]:
        """
        从文本中提取多学科协作建议
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[str]: 多学科协作建议列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        recommendations = []
        
        if "正畸" in text or "牙齿" in text:
            recommendations.append("正畸科会诊")
        
        if "语言" in text or "发音" in text:
            recommendations.append("语言治疗师会诊")
        
        if "耳鼻喉" in text or "听力" in text:
            recommendations.append("耳鼻喉科会诊")
        
        if "心理" in text:
            recommendations.append("心理咨询")
        
        if "遗传" in text:
            recommendations.append("遗传咨询")
        
        if len(recommendations) == 0:
            recommendations.append("暂无特定多学科协作建议")
        
        return recommendations
    
    async def provide_surgical_recommendation(self, deformity_type: str, patient_age: str, syndrome: str) -> str:
        """
        提供手术建议
        
        Args:
            deformity_type: 颅面畸形类型
            patient_age: 患者年龄
            syndrome: 综合征名称
            
        Returns:
            str: 手术建议
        """
        # 构建手术建议提示
        prompt = f"""
        请为一位{patient_age}的{syndrome}患者提供详细的{deformity_type}手术治疗建议，包括：
        
        1. 手术时机和方法选择
        2. 术前准备和评估
        3. 手术风险和预期效果
        4. 术后护理和康复
        5. 长期随访计划
        
        请基于最新的医学指南和循证医学证据提供建议，并考虑患者的年龄和综合征特点。
        """
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API获取建议
        recommendation = await self._call_llm_api()
        
        # 添加建议到消息历史
        self.add_message("assistant", recommendation)
        
        return recommendation
