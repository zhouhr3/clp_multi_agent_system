"""
唇腭裂多智能体系统用户界面
简单的Web界面，用于与唇腭裂多智能体系统交互
"""

import os
import json
import asyncio
import sys
from typing import Dict, Any
import gradio as gr

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import CLPAgentSystem

# 创建系统实例
system = CLPAgentSystem()

async def initialize_system():
    """初始化系统"""
    await system.initialize()
    print("系统初始化完成")

# 初始化系统
asyncio.run(initialize_system())

async def analyze_patient_async(age, gender, symptoms, medical_history, family_history):
    """异步分析患者数据"""
    # 构建患者数据
    patient_data = {
        "age": age,
        "gender": gender,
        "symptoms": [s.strip() for s in symptoms.split(',')],
        "medical_history": medical_history,
        "family_history": family_history
    }
    
    # 分析患者数据
    result = await system.analyze_patient(patient_data)
    
    # 格式化结果
    if "integrated_result" in result:
        return result["integrated_result"]
    else:
        return json.dumps(result, ensure_ascii=False, indent=2)

def analyze_patient(age, gender, symptoms, medical_history, family_history):
    """分析患者数据的同步包装函数"""
    return asyncio.run(analyze_patient_async(age, gender, symptoms, medical_history, family_history))

async def get_treatment_guidelines_async(syndrome_type):
    """异步获取治疗指南"""
    guideline = await system.get_treatment_guidelines(syndrome_type)
    return json.dumps(guideline, ensure_ascii=False, indent=2)

def get_treatment_guidelines(syndrome_type):
    """获取治疗指南的同步包装函数"""
    return asyncio.run(get_treatment_guidelines_async(syndrome_type))

async def search_medical_literature_async(query, max_results):
    """异步搜索医学文献"""
    literature = await system.search_medical_literature(query, max_results)
    return json.dumps(literature, ensure_ascii=False, indent=2)

def search_medical_literature(query, max_results):
    """搜索医学文献的同步包装函数"""
    return asyncio.run(search_medical_literature_async(query, int(max_results)))

# 创建Gradio界面
with gr.Blocks(title="唇腭裂多智能体系统") as demo:
    gr.Markdown("# 唇腭裂多智能体系统")
    gr.Markdown("本系统能够分析唇腭裂患者数据，区分综合征性和非综合征性唇腭裂，并提供诊断和治疗建议。")
    
    with gr.Tab("患者分析"):
        with gr.Row():
            with gr.Column():
                age_input = gr.Textbox(label="年龄", placeholder="例如：6个月")
                gender_input = gr.Radio(["男", "女"], label="性别")
                symptoms_input = gr.Textbox(label="症状（用逗号分隔）", placeholder="例如：唇裂,腭裂,下唇凹陷")
                medical_history_input = gr.Textbox(label="病史", placeholder="例如：足月顺产，无其他异常")
                family_history_input = gr.Textbox(label="家族史", placeholder="例如：无家族史")
                analyze_button = gr.Button("分析患者")
            
            with gr.Column():
                analysis_output = gr.Textbox(label="分析结果", lines=20)
    
    with gr.Tab("治疗指南"):
        with gr.Row():
            with gr.Column():
                syndrome_type_input = gr.Radio([
                    "non_syndromic_cleft_lip", 
                    "non_syndromic_cleft_palate", 
                    "van_der_woude_syndrome"
                ], label="综合征类型")
                guideline_button = gr.Button("获取治疗指南")
            
            with gr.Column():
                guideline_output = gr.Textbox(label="治疗指南", lines=20)
    
    with gr.Tab("医学文献搜索"):
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(label="搜索关键词", placeholder="例如：Van der Woude syndrome treatment")
                max_results_input = gr.Slider(minimum=1, maximum=10, value=3, step=1, label="最大结果数")
                search_button = gr.Button("搜索文献")
            
            with gr.Column():
                literature_output = gr.Textbox(label="搜索结果", lines=20)
    
    # 设置事件处理
    analyze_button.click(
        analyze_patient,
        inputs=[age_input, gender_input, symptoms_input, medical_history_input, family_history_input],
        outputs=analysis_output
    )
    
    guideline_button.click(
        get_treatment_guidelines,
        inputs=[syndrome_type_input],
        outputs=guideline_output
    )
    
    search_button.click(
        search_medical_literature,
        inputs=[query_input, max_results_input],
        outputs=literature_output
    )

# 启动应用
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")
