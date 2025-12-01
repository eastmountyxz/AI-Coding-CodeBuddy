# -*- coding: utf-8 -*-
"""
新媒体营销与热榜系统 - 数据采集模块
支持多平台内容采集、数据清洗、去重和关键信息提取
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import hashlib
from datetime import datetime
from typing import List, Dict
import random

class ContentCrawler:
    """多平台内容爬虫类"""
    
    def __init__(self):
        # 反爬策略：设置User-Agent池
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # 已采集内容的哈希集合，用于去重
        self.content_hashes = set()
        self.load_existing_hashes()
    
    def get_random_headers(self) -> Dict:
        """获取随机请求头（反爬策略）"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def load_existing_hashes(self):
        """加载已存在的内容哈希用于去重"""
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    if 'content_hash' in item:
                        self.content_hashes.add(item['content_hash'])
        except FileNotFoundError:
            pass
    
    def generate_content_hash(self, title: str, content: str) -> str:
        """生成内容哈希用于去重"""
        hash_string = f"{title}{content}"
        return hashlib.md5(hash_string.encode('utf-8')).hexdigest()
    
    def is_duplicate(self, content_hash: str) -> bool:
        """检查内容是否重复"""
        return content_hash in self.content_hashes
    
    def crawl_weibo_hot(self) -> List[Dict]:
        """
        爬取微博热搜（示例模板）
        注意：实际使用需要根据目标网站的robots.txt和服务条款调整
        """
        results = []
        try:
            url = "https://s.weibo.com/top/summary"
            headers = self.get_random_headers()
            
            # 反爬策略：添加延时
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 示例：解析热搜列表（需根据实际HTML结构调整）
                hot_items = soup.find_all('td', class_='td-02')[:20]
                
                for idx, item in enumerate(hot_items):
                    try:
                        title = item.find('a').text.strip()
                        link = item.find('a')['href']
                        
                        # 数据清洗：提取关键信息
                        content_data = {
                            'platform': '微博',
                            'title': title,
                            'link': f"https://s.weibo.com{link}" if link.startswith('/') else link,
                            'rank': idx + 1,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'category': '热搜',
                            'content_hash': self.generate_content_hash(title, '')
                        }
                        
                        # 去重检查
                        if not self.is_duplicate(content_data['content_hash']):
                            results.append(content_data)
                            self.content_hashes.add(content_data['content_hash'])
                    except Exception as e:
                        print(f"解析单条数据出错: {e}")
                        continue
                        
        except Exception as e:
            print(f"爬取微博热搜失败: {e}")
        
        return results
    
    def crawl_zhihu_hot(self) -> List[Dict]:
        """
        爬取知乎热榜（示例模板）
        """
        results = []
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            headers = self.get_random_headers()
            headers['Referer'] = 'https://www.zhihu.com/'
            
            # 反爬策略：添加延时
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for idx, item in enumerate(data.get('data', [])[:20]):
                    try:
                        target = item.get('target', {})
                        title = target.get('title', '')
                        excerpt = target.get('excerpt', '')
                        
                        content_data = {
                            'platform': '知乎',
                            'title': title,
                            'excerpt': excerpt[:100],  # 数据清洗：截取摘要
                            'link': f"https://www.zhihu.com/question/{target.get('id', '')}",
                            'rank': idx + 1,
                            'hot_score': item.get('detail_text', ''),
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'category': '热榜',
                            'content_hash': self.generate_content_hash(title, excerpt)
                        }
                        
                        # 去重检查
                        if not self.is_duplicate(content_data['content_hash']):
                            results.append(content_data)
                            self.content_hashes.add(content_data['content_hash'])
                    except Exception as e:
                        print(f"解析单条数据出错: {e}")
                        continue
                        
        except Exception as e:
            print(f"爬取知乎热榜失败: {e}")
        
        return results
    
    def crawl_douyin_hot(self) -> List[Dict]:
        """
        爬取抖音热榜（示例模板）
        注意：抖音有较强的反爬机制，实际使用可能需要更复杂的策略
        """
        results = []
        # 模拟数据示例（实际需要根据API或页面结构实现）
        try:
            # 这里提供模板，实际需要分析抖音的API接口
            print("抖音热榜采集需要配置具体API接口")
            
            # 示例模拟数据
            for i in range(5):
                content_data = {
                    'platform': '抖音',
                    'title': f'抖音热门话题 #{i+1}',
                    'link': f'https://www.douyin.com/hot/{i+1}',
                    'rank': i + 1,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'category': '热榜',
                    'content_hash': self.generate_content_hash(f'抖音热门话题 #{i+1}', '')
                }
                
                if not self.is_duplicate(content_data['content_hash']):
                    results.append(content_data)
                    self.content_hashes.add(content_data['content_hash'])
                    
        except Exception as e:
            print(f"爬取抖音热榜失败: {e}")
        
        return results
    
    def crawl_all_platforms(self) -> List[Dict]:
        """
        爬取所有平台内容
        """
        all_results = []
        
        print("开始采集微博热搜...")
        all_results.extend(self.crawl_weibo_hot())
        
        print("开始采集知乎热榜...")
        all_results.extend(self.crawl_zhihu_hot())
        
        print("开始采集抖音热榜...")
        all_results.extend(self.crawl_douyin_hot())
        
        print(f"采集完成，共获取 {len(all_results)} 条新内容（已去重）")
        
        return all_results


# 反爬策略说明
"""
反爬虫策略实施要点：

1. User-Agent轮换
   - 使用多个真实浏览器的User-Agent
   - 随机选择，避免被识别为爬虫

2. 请求延时
   - 在请求之间添加随机延时（1-3秒）
   - 避免频繁请求导致IP被封

3. 请求头完善
   - 设置完整的HTTP请求头
   - 包括Accept、Accept-Language、Referer等

4. IP代理池（可选）
   - 使用代理IP轮换
   - 避免单一IP被封禁

5. Cookie管理
   - 维护Session会话
   - 模拟真实用户行为

6. 遵守robots.txt
   - 检查目标网站的robots.txt
   - 遵守网站的爬取规则

7. 数据去重
   - 使用哈希算法检测重复内容
   - 避免重复存储

8. 异常处理
   - 完善的错误捕获机制
   - 避免程序崩溃
"""

if __name__ == "__main__":
    crawler = ContentCrawler()
    results = crawler.crawl_all_platforms()
    print(f"采集到 {len(results)} 条数据")
