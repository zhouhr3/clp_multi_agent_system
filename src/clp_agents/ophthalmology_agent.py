"""
眼科智能体，负责分析眼部异常，提供眼科治疗建议
"""

from typing import Dict, List, Optional, Any
from .agent import Agent

class OphthalmologyAgent(Agent):
    """
    眼科智能体，专注于眼部异常的分析和治疗
    """
    def __init__(
        self,
        model_info: str = "gpt-4o-mini",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """
        初始化眼科智能体
        
        Args:
            model_info: 使用的语言模型信息
            temperature: 生成文本的随机性参数
            api_key: API密钥（可选）
        """
        super().__init__(
            role="眼科专家",
            expertise="眼部异常分析与治疗",
            description="专注于与唇腭裂相关的眼部异常分析、诊断和治疗方案制定，尤其擅长综合征性唇腭裂的眼部问题处理",
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
            "symptom": "眼部异常"
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
        你是一位经验丰富的眼科专家，专注于与唇腭裂相关的眼部异常分析、诊断和治疗。
        
        你的专业知识包括：
        1. 眼部畸形的分类和诊断
        2. 与唇腭裂相关综合征的眼部表现
        3. 眼部手术和非手术治疗方法
        4. 视力保护和康复
        5. 儿童眼科特殊考虑
        
        在回答问题时，请遵循以下原则：
        1. 基于患者的具体情况提供个性化的分析和建议
        2. 使用专业但易于理解的语言
        3. 提供循证医学支持的治疗建议
        4. 考虑患者年龄、眼部异常类型和严重程度
        5. 强调视力保护和早期干预的重要性
        
        你的主要职责是分析眼部异常，提供眼科治疗建议，特别是对综合征性唇腭裂患者。
        """
    
    async def analyze_eye_abnormalities(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析眼部异常
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 构建分析提示
        prompt = self._build_eye_analysis_prompt(patient_data)
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API进行分析
        analysis_result = await self._call_llm_api()
        
        # 添加分析结果到消息历史
        self.add_message("assistant", analysis_result)
        
        # 解析分析结果
        return self._parse_eye_analysis(analysis_result)
    
    def _build_eye_analysis_prompt(self, patient_data: Dict[str, Any]) -> str:
        """
        构建眼部异常分析提示
        
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
        请分析以下综合征性唇腭裂患者的眼部异常情况，并提供详细的诊断和治疗建议：
        
        患者基本信息：
        - 年龄：{age}
        - 性别：{gender}
        - 症状：{symptoms_str}
        - 病史：{medical_history}
        - 综合征类型：{syndrome_type}
        {syndromes_str}
        
        请提供以下信息：
        1. 眼部异常的详细分析和分类
        2. 视力问题评估
        3. 治疗方案建议，包括手术和非手术方案
        4. 视力保护和康复计划
        5. 长期随访和管理建议
        
        请以结构化的方式回答，便于医生理解和使用。
        """
        
        return prompt
    
    def _parse_eye_analysis(self, analysis_result: str) -> Dict[str, Any]:
        """
        解析眼部异常分析结果
        
        Args:
            analysis_result: 分析结果文本
            
        Returns:
            Dict[str, Any]: 解析后的分析结果
        """
        # 简化实现，实际应该进行更复杂的解析
        return {
            "analysis": analysis_result,
            "abnormality_type": self._extract_abnormality_type(analysis_result),
            "vision_status": self._extract_vision_status(analysis_result),
            "treatment_plan": self._extract_treatment_plan(analysis_result),
            "follow_up_plan": self._extract_follow_up_plan(analysis_result)
        }
    
    def _extract_abnormality_type(self, text: str) -> List[str]:
        """
        从文本中提取眼部异常类型
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[str]: 眼部异常类型列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        abnormalities = []
        
        if "眼距过宽" in text or "眼距增宽" in text:
            abnormalities.append("眼距过宽")
        
        if "眼睑下垂" in text:
            abnormalities.append("眼睑下垂")
        
        if "眼球突出" in text:
            abnormalities.append("眼球突出")
        
        if "虹膜缺损" in text:
            abnormalities.append("虹膜缺损")
        
        if "视网膜脱离" in text:
            abnormalities.append("视网膜脱离")
        
        if "近视" in text:
            abnormalities.append("近视")
        
        if len(abnormalities) == 0:
            abnormalities.append("未明确分类的眼部异常")
        
        return abnormalities
    
    def _extract_vision_status(self, text: str) -> Dict[str, Any]:
        """
        从文本中提取视力状态
        
        Args:
            text: 分析结果文本
            
        Returns:
            Dict[str, Any]: 视力状态
        """
        # 简化实现，实际应该使用更复杂的文本分析
        vision_impairment = "未知"
        if "重度视力障碍" in text:
            vision_impairment = "重度"
        elif "中度视力障碍" in text:
            vision_impairment = "中度"
        elif "轻度视力障碍" in text:
            vision_impairment = "轻度"
        elif "正常视力" in text:
            vision_impairment = "正常"
        
        return {
            "vision_impairment": vision_impairment,
            "description": self._extract_vision_description(text)
        }
    
    def _extract_vision_description(self, text: str) -> str:
        """
        从文本中提取视力描述
        
        Args:
            text: 分析结果文本
            
        Returns:
            str: 视力描述
        """
        # 简化实现，实际应该使用更复杂的文本分析
        # 查找包含"视力"的段落
        paragraphs = text.split("\n\n")
        for paragraph in paragraphs:
            if "视力" in paragraph and len(paragraph) > 20:
                return paragraph
        
        return "需要进一步评估视力状态"
    
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
        
        if "眼睑下垂矫正" in text:
            treatment_plan.append({
                "procedure": "眼睑下垂矫正手术",
                "timing": self._extract_timing(text, "眼睑下垂矫正")
            })
        
        if "视网膜脱离修复" in text:
            treatment_plan.append({
                "procedure": "视网膜脱离修复手术",
                "timing": self._extract_timing(text, "视网膜脱离修复")
            })
        
        if "眼镜" in text:
            treatment_plan.append({
                "procedure": "配戴眼镜",
                "timing": "立即"
            })
        
        if "眼部锻炼" in text:
            treatment_plan.append({
                "procedure": "眼部锻炼",
                "timing": "定期"
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
    
    def _extract_follow_up_plan(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取随访计划
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[Dict[str, str]]: 随访计划列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        follow_up_plan = []
        
        if "定期视力检查" in text:
            follow_up_plan.append({
                "action": "定期视力检查",
                "frequency": self._extract_frequency(text, "定期视力检查")
            })
        
        if "眼压监测" in text:
            follow_up_plan.append({
                "action": "眼压监测",
                "frequency": self._extract_frequency(text, "眼压监测")
            })
        
        if "视网膜检查" in text:
            follow_up_plan.append({
                "action": "视网膜检查",
                "frequency": self._extract_frequency(text, "视网膜检查")
            })
        
        if len(follow_up_plan) == 0:
            follow_up_plan.append({
                "action": "常规眼科随访",
                "frequency": "每年一次"
            })
        
        return follow_up_plan
    
    def _extract_frequency(self, text: str, action: str) -> str:
        """
        从文本中提取随访频率
        
        Args:
            text: 分析结果文本
            action: 随访行动
            
        Returns:
            str: 随访频率
        """
        # 简化实现，实际应该使用更复杂的文本分析
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if action in line:
                # 查找该行或下一行中的频率信息
                search_range = min(i + 3, len(lines))
                for j in range(i, search_range):
                    if "每" in lines[j] and ("月" in lines[j] or "年" in lines[j] or "周" in lines[j]):
                        # 提取频率信息
                        return lines[j]
        
        return "未明确频率"
    
    async def provide_vision_correction_recommendation(self, vision_status: Dict[str, Any], patient_age: str) -> str:
        """
        提供视力矫正建议
        
        Args:
            vision_status: 视力状态
            patient_age: 患者年龄
            
        Returns:
            str: 视力矫正建议
        """
        # 构建视力矫正建议提示
        vision_impairment = vision_status.get("vision_impairment", "未知")
        
        prompt = f"""
        请为一位{patient_age}的患者提供详细的视力矫正建议，该患者具有{vision_impairment}视力障碍。
        
        请包括以下内容：
        1. 推荐的视力矫正方法（如眼镜、隐形眼镜、手术等）
        2. 各种方法的优缺点和适用条件
        3. 使用和护理建议
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
