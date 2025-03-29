"""
遗传学智能体，负责判断遗传异常，提供遗传检测建议
"""

from typing import Dict, List, Optional, Any
from .agent import Agent

class GeneticAgent(Agent):
    """
    遗传学智能体，专注于遗传异常的分析和遗传咨询
    """
    def __init__(
        self,
        model_info: str = "gpt-4o-mini",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        """
        初始化遗传学智能体
        
        Args:
            model_info: 使用的语言模型信息
            temperature: 生成文本的随机性参数
            api_key: API密钥（可选）
        """
        super().__init__(
            role="遗传学专家",
            expertise="遗传异常分析与遗传咨询",
            description="专注于与唇腭裂相关的遗传异常分析、遗传检测建议和遗传咨询，尤其擅长综合征性唇腭裂的遗传学评估",
            model_info=model_info,
            temperature=temperature,
            api_key=api_key
        )
        
        # 添加默认激活条件
        self.add_activation_condition({
            "type": "syndrome_type",
            "syndrome_type": "syndromic"  # 综合征性时激活
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
        你是一位经验丰富的遗传学专家，专注于与唇腭裂相关的遗传异常分析、遗传检测建议和遗传咨询。
        
        你的专业知识包括：
        1. 与唇腭裂相关的遗传综合征识别
        2. 遗传检测方法和解读
        3. 遗传咨询和风险评估
        4. 家族遗传分析
        5. 最新的遗传学研究进展
        
        在回答问题时，请遵循以下原则：
        1. 基于患者的具体情况提供个性化的分析和建议
        2. 使用专业但易于理解的语言
        3. 提供循证医学支持的遗传检测建议
        4. 考虑患者家族史和可能的遗传模式
        5. 强调遗传咨询的重要性
        
        你的主要职责是判断遗传异常，提供遗传检测建议，特别是对综合征性唇腭裂患者。
        """
    
    async def analyze_genetic_factors(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析遗传因素
        
        Args:
            patient_data: 患者数据字典
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 构建分析提示
        prompt = self._build_genetic_analysis_prompt(patient_data)
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API进行分析
        analysis_result = await self._call_llm_api()
        
        # 添加分析结果到消息历史
        self.add_message("assistant", analysis_result)
        
        # 解析分析结果
        return self._parse_genetic_analysis(analysis_result)
    
    def _build_genetic_analysis_prompt(self, patient_data: Dict[str, Any]) -> str:
        """
        构建遗传分析提示
        
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
        family_history = patient_data.get("family_history", "无")
        syndrome_type = patient_data.get("syndrome_type", "unknown")
        possible_syndromes = patient_data.get("possible_syndromes", [])
        
        syndromes_str = ""
        if possible_syndromes:
            syndromes_str = "可能的综合征：\n"
            for syndrome in possible_syndromes:
                syndromes_str += f"- {syndrome.get('name', '')}（置信度：{syndrome.get('confidence', '未知')}）\n"
        
        prompt = f"""
        请分析以下综合征性唇腭裂患者的遗传因素，并提供详细的遗传检测建议和遗传咨询：
        
        患者基本信息：
        - 年龄：{age}
        - 性别：{gender}
        - 症状：{symptoms_str}
        - 病史：{medical_history}
        - 家族史：{family_history}
        - 综合征类型：{syndrome_type}
        {syndromes_str}
        
        请提供以下信息：
        1. 可能的遗传异常分析
        2. 推荐的遗传检测方法和具体检测项目
        3. 遗传模式和家族风险评估
        4. 遗传咨询建议
        5. 是否需要其他专科会诊
        
        请以结构化的方式回答，便于医生理解和使用。
        """
        
        return prompt
    
    def _parse_genetic_analysis(self, analysis_result: str) -> Dict[str, Any]:
        """
        解析遗传分析结果
        
        Args:
            analysis_result: 分析结果文本
            
        Returns:
            Dict[str, Any]: 解析后的分析结果
        """
        # 简化实现，实际应该进行更复杂的解析
        return {
            "analysis": analysis_result,
            "genetic_abnormalities": self._extract_genetic_abnormalities(analysis_result),
            "inheritance_pattern": self._extract_inheritance_pattern(analysis_result),
            "recommended_tests": self._extract_recommended_tests(analysis_result),
            "family_risk": self._extract_family_risk(analysis_result)
        }
    
    def _extract_genetic_abnormalities(self, text: str) -> List[str]:
        """
        从文本中提取可能的遗传异常
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[str]: 可能的遗传异常列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        abnormalities = []
        
        if "IRF6" in text:
            abnormalities.append("IRF6基因突变")
        
        if "TCOF1" in text:
            abnormalities.append("TCOF1基因突变")
        
        if "COL2A1" in text or "COL11A1" in text or "COL11A2" in text:
            abnormalities.append("胶原蛋白基因突变")
        
        if "染色体" in text and "缺失" in text:
            abnormalities.append("染色体缺失")
        
        if "染色体" in text and "重复" in text:
            abnormalities.append("染色体重复")
        
        if len(abnormalities) == 0:
            abnormalities.append("未明确的遗传异常")
        
        return abnormalities
    
    def _extract_inheritance_pattern(self, text: str) -> str:
        """
        从文本中提取遗传模式
        
        Args:
            text: 分析结果文本
            
        Returns:
            str: 遗传模式
        """
        # 简化实现，实际应该使用更复杂的文本分析
        if "常染色体显性" in text:
            return "常染色体显性遗传"
        elif "常染色体隐性" in text:
            return "常染色体隐性遗传"
        elif "X连锁显性" in text:
            return "X连锁显性遗传"
        elif "X连锁隐性" in text:
            return "X连锁隐性遗传"
        elif "多基因" in text:
            return "多基因遗传"
        elif "线粒体" in text:
            return "线粒体遗传"
        else:
            return "未明确的遗传模式"
    
    def _extract_recommended_tests(self, text: str) -> List[Dict[str, str]]:
        """
        从文本中提取推荐的遗传检测
        
        Args:
            text: 分析结果文本
            
        Returns:
            List[Dict[str, str]]: 推荐的遗传检测列表
        """
        # 简化实现，实际应该使用更复杂的文本分析
        tests = []
        
        if "全外显子组测序" in text or "WES" in text:
            tests.append({
                "test": "全外显子组测序(WES)",
                "purpose": "检测编码区域的基因变异"
            })
        
        if "全基因组测序" in text or "WGS" in text:
            tests.append({
                "test": "全基因组测序(WGS)",
                "purpose": "检测全基因组范围的变异"
            })
        
        if "染色体微阵列分析" in text or "CMA" in text:
            tests.append({
                "test": "染色体微阵列分析(CMA)",
                "purpose": "检测染色体拷贝数变异"
            })
        
        if "基因芯片" in text:
            tests.append({
                "test": "基因芯片",
                "purpose": "检测特定基因变异"
            })
        
        if "IRF6" in text and "测序" in text:
            tests.append({
                "test": "IRF6基因测序",
                "purpose": "检测Van der Woude综合征相关变异"
            })
        
        if "TCOF1" in text and "测序" in text:
            tests.append({
                "test": "TCOF1基因测序",
                "purpose": "检测Treacher Collins综合征相关变异"
            })
        
        if len(tests) == 0:
            tests.append({
                "test": "基因检测方案待定",
                "purpose": "需要进一步评估后确定检测方案"
            })
        
        return tests
    
    def _extract_family_risk(self, text: str) -> Dict[str, Any]:
        """
        从文本中提取家族风险评估
        
        Args:
            text: 分析结果文本
            
        Returns:
            Dict[str, Any]: 家族风险评估
        """
        # 简化实现，实际应该使用更复杂的文本分析
        risk_level = "未知"
        if "高风险" in text:
            risk_level = "高"
        elif "中等风险" in text:
            risk_level = "中"
        elif "低风险" in text:
            risk_level = "低"
        
        recurrence_risk = "未知"
        if "50%" in text:
            recurrence_risk = "50%"
        elif "25%" in text:
            recurrence_risk = "25%"
        elif "较低" in text:
            recurrence_risk = "较低"
        
        return {
            "risk_level": risk_level,
            "recurrence_risk": recurrence_risk,
            "description": self._extract_risk_description(text)
        }
    
    def _extract_risk_description(self, text: str) -> str:
        """
        从文本中提取风险描述
        
        Args:
            text: 分析结果文本
            
        Returns:
            str: 风险描述
        """
        # 简化实现，实际应该使用更复杂的文本分析
        # 查找包含"风险"的段落
        paragraphs = text.split("\n\n")
        for paragraph in paragraphs:
            if "风险" in paragraph and len(paragraph) > 20:
                return paragraph
        
        return "需要进一步评估家族风险"
    
    async def provide_genetic_counseling(self, genetic_abnormalities: List[str], inheritance_pattern: str) -> str:
        """
        提供遗传咨询
        
        Args:
            genetic_abnormalities: 遗传异常列表
            inheritance_pattern: 遗传模式
            
        Returns:
            str: 遗传咨询建议
        """
        # 构建遗传咨询提示
        abnormalities_str = ", ".join(genetic_abnormalities)
        
        prompt = f"""
        请为一位具有以下遗传特征的唇腭裂患者提供详细的遗传咨询建议：
        
        - 遗传异常：{abnormalities_str}
        - 遗传模式：{inheritance_pattern}
        
        请包括以下内容：
        1. 遗传异常的详细解释
        2. 对患者及家庭的影响
        3. 后代风险评估
        4. 预防和管理策略
        5. 心理支持和资源推荐
        
        请以易于理解但专业准确的方式提供咨询建议。
        """
        
        # 添加提示到消息历史
        self.add_message("user", prompt)
        
        # 调用语言模型API获取建议
        counseling = await self._call_llm_api()
        
        # 添加建议到消息历史
        self.add_message("assistant", counseling)
        
        return counseling
