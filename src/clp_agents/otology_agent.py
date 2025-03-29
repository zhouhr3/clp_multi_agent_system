"""
外耳智能体，负责分析耳部异常，提供耳科治疗建议
"""

from typing import Dict, List, Optional, Any
from .agent import Agent

class OtologyAgent(Agent):
    """
    外耳智能体，专注于耳部异常的分析和治疗
    """
    def __init__(
        self,
        model_info: str = "gpt-4o-mini",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """
        初始化外耳智能体
        
        Args:
            model_info: 使用的语言模型信息
            temperature: 生成文本的随机性参数
            api_key: API密钥（可选）
        """
        super().__init__(
            role="耳科专家",
            expertise="耳部异常分析与治疗",
            description="专注于与唇腭裂相关的耳部异常分析、诊断和治疗方案制定，尤其擅长综合征性唇腭裂的耳部问题处理",
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
            "symptom": "耳部异常"
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
        你是一位经验丰富的耳科专家，专注于与唇腭裂相关的耳部异常分析、诊断和治疗。
        
        你的专业知识包括：
        1. 耳部畸形的分类和诊断
        2. 与唇腭裂相关的听力问题评估
        3. 中耳炎和听力损失的管理
        4. 耳部重建手术技术
        5. 听力康复和辅助设备
        
        在回答问题时，请遵循以下原则：
        1. 基于患者的具体情况提供个性化的分析和建议
        2. 使用专业但易于理解的语言
        3. 提供循证医学支持的治疗建议
        4. 考虑患者年龄、耳部异常类型和严重程度
        5. 强调听力保护和康复的重要性
        
        你的主要职责是分析耳部异常，提供耳科治疗建议，特别是对综合征性唇腭裂患者。
        """
    
    async def analyze_ear_abnormalities(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析耳部异常
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 构建分析提示
        prompt = self._build_ear_analysis_prompt(patient_data)
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API进行分析
        analysis_result = await self._call_llm_api()
        
        # 添加分析结果到消息历史
        self.add_message("assistant", analysis_result)
        
        # 解析分析结果
        return self._parse_ear_analysis(analysis_result)
    
    def _build_ear_analysis_prompt(self, patient_data: Dict[str, Any]) -> str:
        """
        构建耳部异常分析提示
        
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
        请分析以下综合征性唇腭裂患者的耳部异常情况，并提供详细的诊断和治疗建议：
        
        患者基本信息：
        - 年龄：{age}
        - 性别：{gender}
        - 症状：{symptoms_str}
        - 病史：{medical_history}
        - 综合征类型：{syndrome_type}
        {syndromes_str}
        
        请提供以下信息：
        1. 耳部异常的详细分析和分类
        2. 可能的听力问题评估
        3. 治疗方案建议，包括手术和非手术方案
        4. 听力康复计划
        5. 长期随访和管理建议
        
        请以结构化的方式回答，便于医生理解和使用。
        """
        
        return prompt
    
    def _parse_ear_analysis(self, analysis_result: str) -> Dict[str, Any]:
        """
        解析耳部异常分析结果
        
        Args:
            analysis_result: 分析结果文本
            
        Returns:
            Dict[str, Any]: 解析后的分析结果
        """
        # 简化实现，实际应该进行更复杂的解析
        return {
            "analysis": analysis_result,
            "abnormality_type": self._extract_abnormality_type(analysis_result),
            "hearing_status": self._extract_hearing_status(analysis_result),
            "treatment_plan": self._extract_treatment_plan(analysis_result),
            "rehabilitation_plan": self._extract_rehabilitation_plan(analysis_result)
        }
    
    def _extract_abnormality_type(self, text: str) -> List[str]:
        """
        从文本中提取耳部异常类型
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[str]: 耳部异常类型列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        abnormalities = []
        
        if "小耳" in text or "小耳畸形" in text:
            abnormalities.append("小耳畸形")
        
        if "外耳道闭锁" in text:
            abnormalities.append("外耳道闭锁")
        
        if "耳廓畸形" in text:
            abnormalities.append("耳廓畸形")
        
        if "中耳畸形" in text:
            abnormalities.append("中耳畸形")
        
        if "分泌性中耳炎" in text:
            abnormalities.append("分泌性中耳炎")
        
        if len(abnormalities) == 0:
            abnormalities.append("未明确分类的耳部异常")
        
        return abnormalities
    
    def _extract_hearing_status(self, text: str) -> Dict[str, Any]:
        """
        从文本中提取听力状态
        
        Args:
            text: 分析结果文本
            
        Returns:
            Dict[str, Any]: 听力状态
        """
        # 简化实现，实际应该使用更复杂的文本分析
        hearing_loss = "未知"
        if "重度听力损失" in text:
            hearing_loss = "重度"
        elif "中度听力损失" in text:
            hearing_loss = "中度"
        elif "轻度听力损失" in text:
            hearing_loss = "轻度"
        elif "正常听力" in text:
            hearing_loss = "正常"
        
        type_of_loss = "未知"
        if "传导性听力损失" in text:
            type_of_loss = "传导性"
        elif "感音神经性听力损失" in text:
            type_of_loss = "感音神经性"
        elif "混合性听力损失" in text:
            type_of_loss = "混合性"
        
        return {
            "hearing_loss": hearing_loss,
            "type_of_loss": type_of_loss,
            "description": self._extract_hearing_description(text)
        }
    
    def _extract_hearing_description(self, text: str) -> str:
        """
        从文本中提取听力描述
        
        Args:
            text: 分析结果文本
            
        Returns:
            str: 听力描述
        """
        # 简化实现，实际应该使用更复杂的文本分析
        # 查找包含"听力"的段落
        paragraphs = text.split("\n\n")
        for paragraph in paragraphs:
            if "听力" in paragraph and len(paragraph) > 20:
                return paragraph
        
        return "需要进一步评估听力状态"
    
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
        
        if "耳廓重建" in text:
            treatment_plan.append({
                "procedure": "耳廓重建手术",
                "timing": self._extract_timing(text, "耳廓重建")
            })
        
        if "外耳道成形" in text:
            treatment_plan.append({
                "procedure": "外耳道成形术",
                "timing": self._extract_timing(text, "外耳道成形")
            })
        
        if "鼓膜置管" in text:
            treatment_plan.append({
                "procedure": "鼓膜置管术",
                "timing": self._extract_timing(text, "鼓膜置管")
            })
        
        if "抗生素" in text:
            treatment_plan.append({
                "procedure": "抗生素治疗",
                "timing": "根据感染情况"
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
    
    def _extract_rehabilitation_plan(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取康复计划
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[Dict[str, str]]: 康复计划列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        rehabilitation_plan = []
        
        if "助听器" in text:
            rehabilitation_plan.append({
                "method": "助听器",
                "description": "辅助听力"
            })
        
        if "人工耳蜗" in text:
            rehabilitation_plan.append({
                "method": "人工耳蜗",
                "description": "重度听力损失的听力重建"
            })
        
        if "听力训练" in text:
            rehabilitation_plan.append({
                "method": "听力训练",
                "description": "提高听力感知和辨别能力"
            })
        
        if "言语治疗" in text:
            rehabilitation_plan.append({
                "method": "言语治疗",
                "description": "改善语言发育和沟通能力"
            })
        
        if len(rehabilitation_plan) == 0:
            rehabilitation_plan.append({
                "method": "待定康复计划",
                "description": "需要进一步评估后确定康复方案"
            })
        
        return rehabilitation_plan
    
    async def provide_hearing_aid_recommendation(self, hearing_status: Dict[str, Any], patient_age: str) -> str:
        """
        提供听力辅助设备建议
        
        Args:
            hearing_status: 听力状态
            patient_age: 患者年龄
            
        Returns:
            str: 听力辅助设备建议
        """
        # 构建听力辅助设备建议提示
        hearing_loss = hearing_status.get("hearing_loss", "未知")
        type_of_loss = hearing_status.get("type_of_loss", "未知")
        
        prompt = f"""
        请为一位{patient_age}的患者提供详细的听力辅助设备建议，该患者具有以下听力状况：
        
        - 听力损失程度：{hearing_loss}
        - 听力损失类型：{type_of_loss}
        
        请包括以下内容：
        1. 推荐的听力辅助设备类型
        2. 设备选择的考虑因素
        3. 使用和维护建议
        4. 预期效果和适应过程
        5. 后续随访和调整计划
        
        请考虑患者的年龄和特殊需求，提供个性化的建议。
        """
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API获取建议
        recommendation = await self._call_llm_api()
        
        # 添加建议到消息历史
        self.add_message("assistant", recommendation)
        
        return recommendation
