"""
唇腭裂多智能体系统集成测试脚本
"""

import os
import json
import asyncio
import sys
from typing import Dict, Any

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.main import CLPAgentSystem

async def run_test_cases():
    """运行测试用例"""
    print("开始运行唇腭裂多智能体系统测试...")
    
    # 创建系统实例
    system = CLPAgentSystem()
    
    try:
        # 初始化系统
        await system.initialize()
        
        # 测试用例1: 非综合征性唇腭裂
        test_case1 = {
            "age": "4个月",
            "gender": "男",
            "symptoms": ["单侧唇裂", "腭裂"],
            "medical_history": "足月顺产，无其他异常",
            "family_history": "无家族史"
        }
        
        # 测试用例2: 疑似Van der Woude综合征
        test_case2 = {
            "age": "6个月",
            "gender": "女",
            "symptoms": ["双侧唇裂", "腭裂", "下唇凹陷"],
            "medical_history": "足月顺产，发现唇腭裂和下唇凹陷",
            "family_history": "父亲有下唇凹陷"
        }
        
        # 测试用例3: 疑似Treacher Collins综合征
        test_case3 = {
            "age": "5个月",
            "gender": "男",
            "symptoms": ["腭裂", "下颌发育不全", "颧骨发育不全", "耳廓畸形", "眼睑下垂"],
            "medical_history": "足月顺产，发现多发畸形",
            "family_history": "无明显家族史"
        }
        
        # 测试用例4: 疑似Stickler综合征
        test_case4 = {
            "age": "7个月",
            "gender": "女",
            "symptoms": ["腭裂", "小下颌", "近视", "关节疼痛"],
            "medical_history": "足月顺产，3个月时发现视力问题",
            "family_history": "母亲有关节问题"
        }
        
        # 运行测试用例并保存结果
        test_results = {}
        
        print("\n测试用例1: 非综合征性唇腭裂")
        test_results["test_case1"] = await system.analyze_patient(test_case1)
        save_test_result("test_case1_result.json", test_results["test_case1"])
        
        print("\n测试用例2: 疑似Van der Woude综合征")
        test_results["test_case2"] = await system.analyze_patient(test_case2)
        save_test_result("test_case2_result.json", test_results["test_case2"])
        
        print("\n测试用例3: 疑似Treacher Collins综合征")
        test_results["test_case3"] = await system.analyze_patient(test_case3)
        save_test_result("test_case3_result.json", test_results["test_case3"])
        
        print("\n测试用例4: 疑似Stickler综合征")
        test_results["test_case4"] = await system.analyze_patient(test_case4)
        save_test_result("test_case4_result.json", test_results["test_case4"])
        
        # 测试知识库功能
        print("\n测试知识库功能")
        guideline1 = await system.get_treatment_guidelines("non_syndromic_cleft_lip")
        save_test_result("guideline_non_syndromic_result.json", guideline1)
        
        guideline2 = await system.get_treatment_guidelines("van_der_woude_syndrome")
        save_test_result("guideline_vdw_result.json", guideline2)
        
        # 测试API集成功能
        print("\n测试API集成功能")
        literature = await system.search_medical_literature("cleft lip palate treatment", 2)
        save_test_result("literature_search_result.json", literature)
        
        print("\n所有测试用例执行完成，结果已保存到test_results目录")
        
    finally:
        # 关闭系统
        await system.close()

def save_test_result(filename: str, result: Dict[str, Any]):
    """保存测试结果到文件"""
    # 创建测试结果目录
    os.makedirs(os.path.join(os.path.dirname(__file__), 'test_results'), exist_ok=True)
    
    # 保存结果到文件
    result_path = os.path.join(os.path.dirname(__file__), 'test_results', filename)
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"测试结果已保存到: {result_path}")

if __name__ == "__main__":
    # 运行测试用例
    asyncio.run(run_test_cases())
