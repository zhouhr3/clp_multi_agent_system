"""
知识库组件，提供医学知识支持
"""

import os
import json
from typing import Dict, List, Optional, Any, Tuple
import asyncio

class KnowledgeBase:
    """
    知识库基类，提供医学知识支持
    """
    def __init__(self, knowledge_dir: str = None):
        """
        初始化知识库
        
        Args:
            knowledge_dir: 知识库文件目录
        """
        self.knowledge_dir = knowledge_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'knowledge')
        self.syndrome_data = {}
        self.symptom_mapping = {}
        self.treatment_guidelines = {}
        
        # 确保知识库目录存在
        os.makedirs(self.knowledge_dir, exist_ok=True)
        
        # 加载知识库数据
        self._load_knowledge()
    
    def _load_knowledge(self) -> None:
        """加载知识库数据"""
        self._load_syndrome_data()
        self._load_symptom_mapping()
        self._load_treatment_guidelines()
    
    def _load_syndrome_data(self) -> None:
        """加载综合征数据"""
        syndrome_file = os.path.join(self.knowledge_dir, 'syndromes.json')
        if os.path.exists(syndrome_file):
            try:
                with open(syndrome_file, 'r', encoding='utf-8') as f:
                    self.syndrome_data = json.load(f)
            except Exception as e:
                print(f"加载综合征数据失败: {str(e)}")
        else:
            # 创建默认综合征数据
            self.syndrome_data = {
                "van_der_woude_syndrome": {
                    "name": "Van der Woude综合征",
                    "description": "常染色体显性遗传病，特征为唇腭裂和下唇凹陷",
                    "symptoms": ["唇裂", "腭裂", "下唇凹陷", "缺牙"],
                    "genes": ["IRF6"],
                    "inheritance": "常染色体显性",
                    "prevalence": "1/35,000-1/100,000",
                    "references": ["PMID:15316113", "PMID:24124023"]
                },
                "treacher_collins_syndrome": {
                    "name": "Treacher Collins综合征",
                    "description": "常染色体显性遗传病，特征为颅面发育不全",
                    "symptoms": ["下颌发育不全", "颧骨发育不全", "耳廓畸形", "眼睑下垂", "腭裂"],
                    "genes": ["TCOF1", "POLR1C", "POLR1D"],
                    "inheritance": "常染色体显性",
                    "prevalence": "1/50,000",
                    "references": ["PMID:18627481", "PMID:28944301"]
                },
                "stickler_syndrome": {
                    "name": "Stickler综合征",
                    "description": "结缔组织疾病，特征为面部异常、眼部问题和关节问题",
                    "symptoms": ["腭裂", "小下颌", "近视", "视网膜脱离", "关节疼痛"],
                    "genes": ["COL2A1", "COL11A1", "COL11A2"],
                    "inheritance": "常染色体显性",
                    "prevalence": "1/7,500-1/9,000",
                    "references": ["PMID:15316113", "PMID:17492793"]
                }
            }
            # 保存默认数据
            self._save_syndrome_data()
    
    def _load_symptom_mapping(self) -> None:
        """加载症状映射数据"""
        mapping_file = os.path.join(self.knowledge_dir, 'symptom_mapping.json')
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    self.symptom_mapping = json.load(f)
            except Exception as e:
                print(f"加载症状映射数据失败: {str(e)}")
        else:
            # 创建默认症状映射
            self.symptom_mapping = {
                "唇裂": ["van_der_woude_syndrome", "stickler_syndrome"],
                "腭裂": ["van_der_woude_syndrome", "treacher_collins_syndrome", "stickler_syndrome"],
                "下唇凹陷": ["van_der_woude_syndrome"],
                "下颌发育不全": ["treacher_collins_syndrome"],
                "颧骨发育不全": ["treacher_collins_syndrome"],
                "耳廓畸形": ["treacher_collins_syndrome"],
                "眼睑下垂": ["treacher_collins_syndrome"],
                "近视": ["stickler_syndrome"],
                "视网膜脱离": ["stickler_syndrome"],
                "关节疼痛": ["stickler_syndrome"]
            }
            # 保存默认数据
            self._save_symptom_mapping()
    
    def _load_treatment_guidelines(self) -> None:
        """加载治疗指南数据"""
        guidelines_file = os.path.join(self.knowledge_dir, 'treatment_guidelines.json')
        if os.path.exists(guidelines_file):
            try:
                with open(guidelines_file, 'r', encoding='utf-8') as f:
                    self.treatment_guidelines = json.load(f)
            except Exception as e:
                print(f"加载治疗指南数据失败: {str(e)}")
        else:
            # 创建默认治疗指南
            self.treatment_guidelines = {
                "non_syndromic_cleft_lip": {
                    "name": "非综合征性唇裂治疗指南",
                    "timeline": [
                        {"age": "0-3个月", "treatment": "术前正畸治疗，喂养指导"},
                        {"age": "3-6个月", "treatment": "唇裂修复手术"},
                        {"age": "6-12个月", "treatment": "语言发育监测"},
                        {"age": "12-18个月", "treatment": "腭裂修复手术（如有需要）"}
                    ],
                    "follow_up": ["语言治疗", "牙齿和颌面发育监测", "心理支持"],
                    "references": ["PMID:25187187", "PMID:28944301"]
                },
                "non_syndromic_cleft_palate": {
                    "name": "非综合征性腭裂治疗指南",
                    "timeline": [
                        {"age": "0-3个月", "treatment": "喂养指导，特殊奶嘴使用"},
                        {"age": "9-18个月", "treatment": "腭裂修复手术"},
                        {"age": "2-4岁", "treatment": "语言治疗评估和干预"}
                    ],
                    "follow_up": ["听力检查", "语言治疗", "牙齿和颌面发育监测"],
                    "references": ["PMID:25187187", "PMID:26361258"]
                },
                "van_der_woude_syndrome": {
                    "name": "Van der Woude综合征治疗指南",
                    "timeline": [
                        {"age": "0-3个月", "treatment": "喂养指导，遗传咨询"},
                        {"age": "3-6个月", "treatment": "唇裂修复手术"},
                        {"age": "9-18个月", "treatment": "腭裂修复手术"},
                        {"age": "5-7岁", "treatment": "下唇凹陷修复（如需要）"}
                    ],
                    "follow_up": ["语言治疗", "牙齿和颌面发育监测", "遗传咨询"],
                    "references": ["PMID:15316113", "PMID:24124023"]
                }
            }
            # 保存默认数据
            self._save_treatment_guidelines()
    
    def _save_syndrome_data(self) -> None:
        """保存综合征数据"""
        syndrome_file = os.path.join(self.knowledge_dir, 'syndromes.json')
        try:
            with open(syndrome_file, 'w', encoding='utf-8') as f:
                json.dump(self.syndrome_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存综合征数据失败: {str(e)}")
    
    def _save_symptom_mapping(self) -> None:
        """保存症状映射数据"""
        mapping_file = os.path.join(self.knowledge_dir, 'symptom_mapping.json')
        try:
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(self.symptom_mapping, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存症状映射数据失败: {str(e)}")
    
    def _save_treatment_guidelines(self) -> None:
        """保存治疗指南数据"""
        guidelines_file = os.path.join(self.knowledge_dir, 'treatment_guidelines.json')
        try:
            with open(guidelines_file, 'w', encoding='utf-8') as f:
                json.dump(self.treatment_guidelines, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存治疗指南数据失败: {str(e)}")
    
    def get_syndrome_info(self, syndrome_id: str) -> Dict[str, Any]:
        """
        获取综合征信息
        
        Args:
            syndrome_id: 综合征ID
            
        Returns:
            Dict[str, Any]: 综合征信息
        """
        return self.syndrome_data.get(syndrome_id, {})
    
    def get_syndromes_by_symptom(self, symptom: str) -> List[str]:
        """
        根据症状获取可能的综合征
        
        Args:
            symptom: 症状名称
            
        Returns:
            List[str]: 可能的综合征ID列表
        """
        return self.symptom_mapping.get(symptom, [])
    
    def get_treatment_guideline(self, condition_id: str) -> Dict[str, Any]:
        """
        获取治疗指南
        
        Args:
            condition_id: 疾病或综合征ID
            
        Returns:
            Dict[str, Any]: 治疗指南
        """
        return self.treatment_guidelines.get(condition_id, {})
    
    def add_syndrome(self, syndrome_id: str, syndrome_info: Dict[str, Any]) -> None:
        """
        添加综合征信息
        
        Args:
            syndrome_id: 综合征ID
            syndrome_info: 综合征信息
        """
        self.syndrome_data[syndrome_id] = syndrome_info
        
        # 更新症状映射
        for symptom in syndrome_info.get("symptoms", []):
            if symptom not in self.symptom_mapping:
                self.symptom_mapping[symptom] = []
            if syndrome_id not in self.symptom_mapping[symptom]:
                self.symptom_mapping[symptom].append(syndrome_id)
        
        # 保存数据
        self._save_syndrome_data()
        self._save_symptom_mapping()
    
    def add_treatment_guideline(self, condition_id: str, guideline: Dict[str, Any]) -> None:
        """
        添加治疗指南
        
        Args:
            condition_id: 疾病或综合征ID
            guideline: 治疗指南
        """
        self.treatment_guidelines[condition_id] = guideline
        self._save_treatment_guidelines()
    
    def search_syndromes(self, symptoms: List[str]) -> List[Dict[str, Any]]:
        """
        根据症状列表搜索可能的综合征
        
        Args:
            symptoms: 症状列表
            
        Returns:
            List[Dict[str, Any]]: 可能的综合征列表，按匹配度排序
        """
        # 计算每个综合征的匹配度
        syndrome_scores = {}
        for symptom in symptoms:
            syndrome_ids = self.get_syndromes_by_symptom(symptom)
            for syndrome_id in syndrome_ids:
                if syndrome_id not in syndrome_scores:
                    syndrome_scores[syndrome_id] = 0
                syndrome_scores[syndrome_id] += 1
        
        # 获取综合征详细信息并按匹配度排序
        results = []
        for syndrome_id, score in syndrome_scores.items():
            syndrome_info = self.get_syndrome_info(syndrome_id)
            if syndrome_info:
                # 计算匹配度百分比
                total_symptoms = len(syndrome_info.get("symptoms", []))
                if total_symptoms > 0:
                    match_percentage = (score / total_symptoms) * 100
                else:
                    match_percentage = 0
                
                results.append({
                    "id": syndrome_id,
                    "info": syndrome_info,
                    "matched_symptoms": score,
                    "total_symptoms": total_symptoms,
                    "match_percentage": match_percentage
                })
        
        # 按匹配度百分比降序排序
        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        return results
