"""
PubMed服务模块，提供与PubMed API的交互功能
"""
from typing import Dict, Any, List, Optional
import aiohttp
import logging
import json
from datetime import datetime, date
import xml.etree.ElementTree as ET

from ..config.settings import settings

# 配置日志
logger = logging.getLogger("pubmed_service")

# PubMed API基础URL
PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

async def search_pubmed(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    date_range: Optional[str] = None
) -> Dict[str, Any]:
    """
    搜索PubMed文献
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
        sort_by: 排序方式，可选值：relevance, date
        date_range: 日期范围，可选值：1y, 5y, 10y
        
    Returns:
        Dict[str, Any]: 搜索结果
    """
    try:
        # 构建查询参数
        params = {
            "db": "pubmed",
            "term": f"{query} AND \"cleft lip\"[MeSH Terms]",
            "retmode": "json",
            "retmax": max_results,
            "sort": "relevance" if sort_by == "relevance" else "pub date",
            "api_key": settings.PUBMED_API_KEY
        }
        
        # 添加日期范围
        if date_range:
            years = int(date_range.replace("y", ""))
            date_from = (datetime.now().date().replace(year=datetime.now().year - years)).strftime("%Y/%m/%d")
            params["datetype"] = "pdat"
            params["mindate"] = date_from
            params["maxdate"] = datetime.now().date().strftime("%Y/%m/%d")
        
        # 发送搜索请求
        async with aiohttp.ClientSession() as session:
            # 首先获取ID列表
            search_url = f"{PUBMED_BASE_URL}/esearch.fcgi"
            async with session.get(search_url, params=params) as response:
                if response.status != 200:
                    logger.error(f"PubMed search failed: {response.status}")
                    return {"error": "PubMed搜索失败", "status": response.status}
                
                search_data = await response.json()
                id_list = search_data["esearchresult"]["idlist"]
                
                if not id_list:
                    return {
                        "total": 0,
                        "items": [],
                        "query": query
                    }
                
                # 获取文献详情
                summary_url = f"{PUBMED_BASE_URL}/esummary.fcgi"
                summary_params = {
                    "db": "pubmed",
                    "id": ",".join(id_list),
                    "retmode": "json",
                    "api_key": settings.PUBMED_API_KEY
                }
                
                async with session.get(summary_url, params=summary_params) as summary_response:
                    if summary_response.status != 200:
                        logger.error(f"PubMed summary failed: {summary_response.status}")
                        return {"error": "PubMed摘要获取失败", "status": summary_response.status}
                    
                    summary_data = await summary_response.json()
                    
                    # 解析结果
                    results = []
                    for pubmed_id in id_list:
                        article_data = summary_data["result"][pubmed_id]
                        
                        # 提取作者信息
                        authors = []
                        for author in article_data.get("authors", []):
                            if author.get("authtype") == "Author":
                                authors.append({
                                    "name": author.get("name", ""),
                                    "affiliation": ""
                                })
                        
                        # 提取发表日期
                        pub_date = None
                        try:
                            pub_date_parts = article_data.get("pubdate", "").split()
                            if len(pub_date_parts) >= 2:
                                year = int(pub_date_parts[0])
                                month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                                         "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}.get(pub_date_parts[1], 1)
                                day = 1
                                if len(pub_date_parts) >= 3 and pub_date_parts[2].isdigit():
                                    day = int(pub_date_parts[2])
                                pub_date = f"{year}-{month:02d}-{day:02d}"
                        except Exception as e:
                            logger.warning(f"Error parsing publication date: {e}")
                            pub_date = None
                        
                        # 构建文献信息
                        article = {
                            "pubmed_id": pubmed_id,
                            "title": article_data.get("title", "").replace(".", ""),
                            "authors": authors,
                            "journal": article_data.get("fulljournalname", ""),
                            "publication_date": pub_date,
                            "abstract": "",  # 摘要需要单独获取
                            "doi": article_data.get("elocationid", "").replace("doi: ", "") if "elocationid" in article_data else None
                        }
                        
                        results.append(article)
                    
                    return {
                        "total": int(search_data["esearchresult"]["count"]),
                        "items": results,
                        "query": query
                    }
    
    except Exception as e:
        logger.error(f"Error searching PubMed: {str(e)}")
        return {"error": f"搜索PubMed时发生错误: {str(e)}"}

async def get_pubmed_article(pubmed_id: str) -> Dict[str, Any]:
    """
    获取PubMed文献详情
    
    Args:
        pubmed_id: PubMed ID
        
    Returns:
        Dict[str, Any]: 文献详情
    """
    try:
        async with aiohttp.ClientSession() as session:
            # 获取文献摘要
            fetch_url = f"{PUBMED_BASE_URL}/efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": pubmed_id,
                "retmode": "xml",
                "api_key": settings.PUBMED_API_KEY
            }
            
            async with session.get(fetch_url, params=fetch_params) as response:
                if response.status != 200:
                    logger.error(f"PubMed fetch failed: {response.status}")
                    return {"error": "PubMed文献获取失败", "status": response.status}
                
                xml_data = await response.text()
                
                # 解析XML
                root = ET.fromstring(xml_data)
                
                # 提取标题
                title_element = root.find(".//ArticleTitle")
                title = title_element.text if title_element is not None else ""
                
                # 提取作者
                authors = []
                author_list = root.findall(".//Author")
                for author in author_list:
                    last_name = author.find("LastName")
                    fore_name = author.find("ForeName")
                    affiliation = author.find("Affiliation")
                    
                    name = ""
                    if last_name is not None and fore_name is not None:
                        name = f"{fore_name.text} {last_name.text}"
                    elif last_name is not None:
                        name = last_name.text
                    
                    authors.append({
                        "name": name,
                        "affiliation": affiliation.text if affiliation is not None else ""
                    })
                
                # 提取期刊
                journal_element = root.find(".//Journal/Title")
                journal = journal_element.text if journal_element is not None else ""
                
                # 提取发表日期
                pub_date = None
                pub_date_element = root.find(".//PubDate")
                if pub_date_element is not None:
                    year = pub_date_element.find("Year")
                    month = pub_date_element.find("Month")
                    day = pub_date_element.find("Day")
                    
                    year_val = year.text if year is not None else "2000"
                    month_val = month.text if month is not None else "01"
                    day_val = day.text if day is not None else "01"
                    
                    # 处理月份名称
                    if month_val in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                        month_val = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
                                    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}[month_val]
                    
                    try:
                        pub_date = date(int(year_val), int(month_val), int(day_val))
                    except:
                        try:
                            pub_date = date(int(year_val), int(month_val), 1)
                        except:
                            try:
                                pub_date = date(int(year_val), 1, 1)
                            except:
                                pub_date = date(2000, 1, 1)
                
                # 提取摘要
                abstract_elements = root.findall(".//AbstractText")
                abstract = " ".join([elem.text for elem in abstract_elements if elem.text]) if abstract_elements else ""
                
                # 提取DOI
                doi_element = root.find(".//ArticleId[@IdType='doi']")
                doi = doi_element.text if doi_element is not None else None
                
                # 提取关键词
                keyword_elements = root.findall(".//Keyword")
                keywords = [elem.text for elem in keyword_elements if elem.text]
                
                return {
                    "pubmed_id": pubmed_id,
                    "title": title,
                    "authors": authors,
                    "journal": journal,
                    "publication_date": pub_date,
                    "abstract": abstract,
                    "doi": doi,
                    "keywords": keywords
                }
    
    except Exception as e:
        logger.error(f"Error fetching PubMed article: {str(e)}")
        return {"error": f"获取PubMed文献时发生错误: {str(e)}"}
