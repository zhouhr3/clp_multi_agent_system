"""
唇腭裂专科智能体，负责分析唇腭裂类型，提供非综合征性唇腭裂的治疗建议
"""

from typing import Dict, List, Optional, Any
from .agent import Agent

class CleftLipPalateAgent(Agent):
    """
    唇腭裂专科智能体，专注于唇腭裂的分类和治疗
    """
    def __init__(
        self,
        model_info: str = "gpt-4o-mini",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """
        初始化唇腭裂专科智能体
        
        Args:
            model_info: 使用的语言模型信息
            temperature: 生成文本的随机性参数
            api_key: API密钥（可选）
        """
        super().__init__(
            role="唇腭裂专科医生",
            expertise="唇腭裂分类与治疗",
            description="专注于唇腭裂的分类、诊断和治疗方案制定，尤其擅长非综合征性唇腭裂的处理",
            model_info=model_info,
            temperature=temperature,
            api_key=api_key
        )
        
        # 添加默认激活条件
        self.add_activation_condition({
            "type": "syndrome_type",
            "syndrome_type": "non-syndromic"  # 非综合征性时激活
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
        你是一位经验丰富的唇腭裂专科医生，专注于唇腭裂的分类、诊断和治疗方案制定。
        
        你的专业知识包括：
        1. 唇腭裂的分类（单侧/双侧，完全/不完全）
        2. 唇腭裂的诊断标准和评估方法
        3. 非综合征性唇腭裂的治疗方案
        4. 唇腭裂修复手术的时机和方法
        5. 术后护理和语言康复
        
        在回答问题时，请遵循以下原则：
        1. 基于患者的具体情况提供个性化的分析和建议
        2. 使用专业但易于理解的语言
        3. 提供循证医学支持的治疗建议
        4. 考虑患者年龄、唇腭裂类型和严重程度
        5. 在需要时建议多学科协作
        
        你的主要职责是分析唇腭裂类型，提供非综合征性唇腭裂的治疗建议。
        """
    
    async def analyze_cleft_type(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析唇腭裂类型
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 构建分析提示
        prompt = self._build_cleft_analysis_prompt(patient_data)
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API进行分析
        analysis_result = await self._call_llm_api()
        
        # 添加分析结果到消息历史
        self.add_message("assistant", analysis_result)
        
        # 解析分析结果
        return self._parse_cleft_analysis(analysis_result)
    
    def _build_cleft_analysis_prompt(self, patient_data: Dict[str, Any]) -> str:
        """
        构建唇腭裂分析提示
        
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
        
        prompt = f"""
        请分析以下非综合征性唇腭裂患者的情况，并提供详细的分类和治疗建议：
        
        患者基本信息：
        - 年龄：{age}
        - 性别：{gender}
        - 症状：{symptoms_str}
        - 病史：{medical_history}
        
        请提供以下信息：
        1. 唇腭裂分类（单侧/双侧，完全/不完全）
        2. 严重程度评估
        3. 治疗方案建议，包括手术时机和方法
        4. 术后护理和语言康复建议
        5. 是否需要其他专科会诊
        
        请以结构化的方式回答，便于医生理解和使用。
        """
        
        return prompt
    
    def _parse_cleft_analysis(self, analysis_result: str) -> Dict[str, Any]:
        """
        解析唇腭裂分析结果
        
        Args:
            analysis_result: 分析结果文本
            
        Returns:
            Dict[str, Any]: 解析后的分析结果
        """
        # 简化实现，实际应该进行更复杂的解析
        # 这里假设结果已经是结构化的文本
        return {
            "analysis": analysis_result,
            "cleft_type": self._extract_cleft_type(analysis_result),
            "severity": self._extract_severity(analysis_result),
            "treatment_plan": self._extract_treatment_plan(analysis_result)
        }
    
    def _extract_cleft_type(self, text: str) -> str:
        """
        从文本中提取唇腭裂类型
        
        Args:
            text: 分析结果文本
            
        Returns:
            str: 唇腭裂类型
        """
        # 简化实现，实际应该使用更复杂的文本分析
        if "双侧" in text and "完全" in text:
            return "双侧完全性唇腭裂"
        elif "双侧" in text:
            return "双侧不完全性唇腭裂"
        elif "单侧" in text and "完全" in text:
            return "单侧完全性唇腭裂"
        elif "单侧" in text:
            return "单侧不完全性唇腭裂"
        elif "唇裂" in text and "腭裂" not in text:
            return "单纯性唇裂"
        elif "腭裂" in text and "唇裂" not in text:
            return "单纯性腭裂"
        else:
            return "未明确分类的唇腭裂"
    
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
        
        if "3-6个月" in text and "唇裂修复" in text:
            treatment_plan.append({
                "time": "3-6个月",
                "procedure": "唇裂修复手术"
            })
        
        if "9-18个月" in text and "腭裂修复" in text:
            treatment_plan.append({
                "time": "9-18个月",
                "procedure": "腭裂修复手术"
            })
        
        if "语言治疗" in text:
            treatment_plan.append({
                "time": "术后",
                "procedure": "语言治疗和康复"
            })
        
        if len(treatment_plan) == 0:
            treatment_plan.append({
                "time": "待定",
                "procedure": "需要进一步评估后确定治疗计划"
            })
        
        return treatment_plan
    
    async def provide_treatment_recommendation(self, cleft_type: str, patient_age: str) -> str:
        """
        提供治疗建议
        
        Args:
            cleft_type: 唇腭裂类型
            patient_age: 患者年龄
            
        Returns:
            str: 治疗建议
        """
        # 构建治疗建议提示
        prompt = f"""
        请为一位{patient_age}的{cleft_type}患者提供详细的治疗建议，包括：
        
        1. 手术时机和方法
        2. 术前准备
        3. 术后护理
        4. 语言康复计划
        5. 长期随访建议
        
        请基于最新的医学指南和循证医学证据提供建议。
        """
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API获取建议
        recommendation = await self._call_llm_api()
        
        # 添加建议到消息历史
        self.add_message("assistant", recommendation)
        
        return recommendation
