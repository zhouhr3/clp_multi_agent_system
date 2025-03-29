"""
外部API集成组件，用于与医学数据库和服务集成
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
import aiohttp

class ExternalAPIClient:
    """
    外部API客户端基类，提供与医学数据库和服务的集成
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化API客户端
        
        Args:
            api_key: API密钥（可选）
        """
        self.api_key = api_key
        self.session = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def ensure_session(self):
        """确保会话已创建"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close(self):
        """关闭会话"""
        if self.session:
            await self.session.close()
            self.session = None


class PubMedClient(ExternalAPIClient):
    """
    PubMed API客户端，用于检索医学文献
    """
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索PubMed文献
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        await self.ensure_session()
        
        # 构建搜索URL
        search_url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results
        }
        
        try:
            # 执行搜索请求
            async with self.session.get(search_url, params=params) as response:
                if response.status != 200:
                    return []
                
                search_data = await response.json()
                id_list = search_data.get("esearchresult", {}).get("idlist", [])
                
                if not id_list:
                    return []
                
                # 获取文章详情
                return await self.fetch_articles(id_list)
        except Exception as e:
            print(f"PubMed搜索失败: {str(e)}")
            return []
    
    async def fetch_articles(self, id_list: List[str]) -> List[Dict[str, Any]]:
        """
        获取文章详情
        
        Args:
            id_list: 文章ID列表
            
        Returns:
            List[Dict[str, Any]]: 文章详情列表
        """
        if not id_list:
            return []
        
        await self.ensure_session()
        
        # 构建获取详情URL
        fetch_url = f"{self.BASE_URL}/esummary.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "json"
        }
        
        try:
            # 执行获取详情请求
            async with self.session.get(fetch_url, params=params) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                result = data.get("result", {})
                
                # 解析文章详情
                articles = []
                for article_id in id_list:
                    article_data = result.get(article_id, {})
                    if article_data:
                        articles.append({
                            "id": article_id,
                            "title": article_data.get("title", ""),
                            "authors": [author.get("name", "") for author in article_data.get("authors", [])],
                            "journal": article_data.get("fulljournalname", ""),
                            "publication_date": article_data.get("pubdate", ""),
                            "abstract": article_data.get("abstract", ""),
                            "url": f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
                        })
                
                return articles
        except Exception as e:
            print(f"获取PubMed文章详情失败: {str(e)}")
            return []


class MedGenClient(ExternalAPIClient):
    """
    MedGen API客户端，用于获取遗传疾病信息
    """
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    async def search_condition(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索医学条件/疾病
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        await self.ensure_session()
        
        # 构建搜索URL
        search_url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            "db": "medgen",
            "term": query,
            "retmode": "json",
            "retmax": max_results
        }
        
        try:
            # 执行搜索请求
            async with self.session.get(search_url, params=params) as response:
                if response.status != 200:
                    return []
                
                search_data = await response.json()
                id_list = search_data.get("esearchresult", {}).get("idlist", [])
                
                if not id_list:
                    return []
                
                # 获取条件详情
                return await self.fetch_conditions(id_list)
        except Exception as e:
            print(f"MedGen搜索失败: {str(e)}")
            return []
    
    async def fetch_conditions(self, id_list: List[str]) -> List[Dict[str, Any]]:
        """
        获取条件详情
        
        Args:
            id_list: 条件ID列表
            
        Returns:
            List[Dict[str, Any]]: 条件详情列表
        """
        if not id_list:
            return []
        
        await self.ensure_session()
        
        # 构建获取详情URL
        fetch_url = f"{self.BASE_URL}/esummary.fcgi"
        params = {
            "db": "medgen",
            "id": ",".join(id_list),
            "retmode": "json"
        }
        
        try:
            # 执行获取详情请求
            async with self.session.get(fetch_url, params=params) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                result = data.get("result", {})
                
                # 解析条件详情
                conditions = []
                for condition_id in id_list:
                    condition_data = result.get(condition_id, {})
                    if condition_data:
                        conditions.append({
                            "id": condition_id,
                            "name": condition_data.get("title", ""),
                            "definition": condition_data.get("definition", ""),
                            "synonyms": condition_data.get("synonyms", []),
                            "concepts": condition_data.get("concepts", []),
                            "url": f"https://www.ncbi.nlm.nih.gov/medgen/{condition_id}"
                        })
                
                return conditions
        except Exception as e:
            print(f"获取MedGen条件详情失败: {str(e)}")
            return []


class ClinVarClient(ExternalAPIClient):
    """
    ClinVar API客户端，用于获取基因变异信息
    """
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    async def search_variant(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索基因变异
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        await self.ensure_session()
        
        # 构建搜索URL
        search_url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            "db": "clinvar",
            "term": query,
            "retmode": "json",
            "retmax": max_results
        }
        
        try:
            # 执行搜索请求
            async with self.session.get(search_url, params=params) as response:
                if response.status != 200:
                    return []
                
                search_data = await response.json()
                id_list = search_data.get("esearchresult", {}).get("idlist", [])
                
                if not id_list:
                    return []
                
                # 获取变异详情
                return await self.fetch_variants(id_list)
        except Exception as e:
            print(f"ClinVar搜索失败: {str(e)}")
            return []
    
    async def fetch_variants(self, id_list: List[str]) -> List[Dict[str, Any]]:
        """
        获取变异详情
        
        Args:
            id_list: 变异ID列表
            
        Returns:
            List[Dict[str, Any]]: 变异详情列表
        """
        if not id_list:
            return []
        
        await self.ensure_session()
        
        # 构建获取详情URL
        fetch_url = f"{self.BASE_URL}/esummary.fcgi"
        params = {
            "db": "clinvar",
            "id": ",".join(id_list),
            "retmode": "json"
        }
        
        try:
            # 执行获取详情请求
            async with self.session.get(fetch_url, params=params) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                result = data.get("result", {})
                
                # 解析变异详情
                variants = []
                for variant_id in id_list:
                    variant_data = result.get(variant_id, {})
                    if variant_data:
                        variants.append({
                            "id": variant_id,
                            "name": variant_data.get("title", ""),
                            "gene": variant_data.get("gene", ""),
                            "clinical_significance": variant_data.get("clinical_significance", ""),
                            "condition": variant_data.get("condition", ""),
                            "chromosome": variant_data.get("chromosome", ""),
                            "url": f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{variant_id}/"
                        })
                
                return variants
        except Exception as e:
            print(f"获取ClinVar变异详情失败: {str(e)}")
            return []


class APIIntegration:
    """
    API集成管理器，统一管理各种外部API客户端
    """
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        初始化API集成管理器
        
        Args:
            api_keys: API密钥字典，键为API名称，值为密钥
        """
        self.api_keys = api_keys or {}
        self.pubmed_client = None
        self.medgen_client = None
        self.clinvar_client = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.pubmed_client = PubMedClient(self.api_keys.get("pubmed"))
        self.medgen_client = MedGenClient(self.api_keys.get("medgen"))
        self.clinvar_client = ClinVarClient(self.api_keys.get("clinvar"))
        
        await self.pubmed_client.__aenter__()
        await self.medgen_client.__aenter__()
        await self.clinvar_client.__aenter__()
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.pubmed_client:
            await self.pubmed_client.__aexit__(exc_type, exc_val, exc_tb)
        if self.medgen_client:
            await self.medgen_client.__aexit__(exc_type, exc_val, exc_tb)
        if self.clinvar_client:
            await self.clinvar_client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def close(self):
        """关闭所有客户端"""
        if self.pubmed_client:
            await self.pubmed_client.close()
        if self.medgen_client:
            await self.medgen_client.close()
        if self.clinvar_client:
            await self.clinvar_client.close()
    
    async def search_literature(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索医学文献
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        if not self.pubmed_client:
            self.pubmed_client = PubMedClient(self.api_keys.get("pubmed"))
            await self.pubmed_client.__aenter__()
        
        return await self.pubmed_client.search(query, max_results)
    
    async def search_genetic_condition(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索遗传疾病信息
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        if not self.medgen_client:
            self.medgen_client = MedGenClient(self.api_keys.get("medgen"))
            await self.medgen_client.__aenter__()
        
        return await self.medgen_client.search_condition(query, max_results)
    
    async def search_gene_variant(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索基因变异信息
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            
        Returns:
            List[Dict[str, Any]]: 搜索结果列表
        """
        if not self.clinvar_client:
            self.clinvar_client = ClinVarClient(self.api_keys.get("clinvar"))
            await self.clinvar_client.__aenter__()
        
        return await self.clinvar_client.search_variant(query, max_results)
    
    async def search_all(self, query: str, max_results: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        在所有API中搜索
        
        Args:
            query: 搜索查询
            max_results: 每个API的最大结果数
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: 搜索结果字典，键为API名称，值为结果列表
        """
        # 并行执行所有搜索
        literature_task = self.search_literature(query, max_results)
        condition_task = self.search_genetic_condition(query, max_results)
        variant_task = self.search_gene_variant(query, max_results)
        
        literature_results, condition_results, variant_results = await asyncio.gather(
            literature_task, condition_task, variant_task
        )
        
        return {
            "literature": literature_results,
            "genetic_conditions": condition_results,
            "gene_variants": variant_results
        }
