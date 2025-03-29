"""
智能体服务模块，提供与多智能体系统的交互功能
"""
from typing import List, Dict, Any, Optional
import json
import logging
import os
from datetime import datetime

# 导入OpenAI API
import openai
from ..config.settings import settings

# 配置OpenAI API密钥
openai.api_key = settings.OPENAI_API_KEY

# 配置日志
logger = logging.getLogger("agent_service")

async def analyze_patient_data(
    symptoms: List[str],
    age: str,
    gender: str,
    medical_history: Optional[str] = None,
    family_history: Optional[str] = None
) -> Dict[str, Any]:
    """
    使用多智能体系统分析患者数据
    
    Args:
        symptoms: 症状列表
        age: 患者年龄
        gender: 患者性别
        medical_history: 患者病史
        family_history: 患者家族史
        
    Returns:
        Dict[str, Any]: 分析结果
    """
    try:
        # 准备输入数据
        patient_data = {
            "symptoms": symptoms,
            "age": age,
            "gender": gender,
            "medical_history": medical_history,
            "family_history": family_history
        }
        
        # 构建系统提示词
        system_prompt = """
        你是唇腭裂多智能体系统的协调者，负责根据患者信息进行分析并招募相关专科智能体。
        你需要判断患者是否患有综合征性唇腭裂，并提供诊断和治疗建议。
        
        请按照以下步骤进行分析：
        1. 判断是否为综合征性唇腭裂（如Van der Woude综合征等）
        2. 确定唇腭裂类型和严重程度
        3. 提供治疗建议
        4. 确定需要招募的专科智能体（如颅面外科、遗传学、外耳科、眼科等）
        5. 制定随访计划
        
        请以JSON格式返回分析结果，包含以下字段：
        - syndrome_type: "syndromic" 或 "non_syndromic"
        - syndrome_name: 如果是综合征性，则提供综合征名称
        - cleft_type: 唇腭裂类型
        - severity: 严重程度
        - treatment_recommendations: 治疗建议
        - specialist_recommendations: 专科会诊建议
        - follow_up_plan: 随访计划
        """
        
        # 构建用户提示词
        user_prompt = f"""
        请分析以下患者信息：
        
        症状: {', '.join(symptoms)}
        年龄: {age}
        性别: {gender}
        病史: {medical_history if medical_history else '无'}
        家族史: {family_history if family_history else '无'}
        
        请提供完整的分析结果，包括综合征判断、唇腭裂分类、治疗建议、专科会诊建议和随访计划。
        """
        
        # 调用OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        # 解析响应
        result = json.loads(response.choices[0].message.content)
        
        # 记录分析结果
        logger.info(f"Patient analysis completed: {result['syndrome_type']}, {result.get('syndrome_name', 'N/A')}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error analyzing patient data: {str(e)}")
        # 返回默认分析结果
        return {
            "syndrome_type": "unknown",
            "cleft_type": "unknown",
            "severity": "unknown",
            "treatment_recommendations": {
                "error": "分析过程中发生错误，请稍后重试"
            }
        }
