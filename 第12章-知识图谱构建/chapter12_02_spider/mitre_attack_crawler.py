#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MITRE ATT&CK APT 组织威胁情报爬虫
自动采集指定 APT 组织的威胁情报数据
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 目标 APT 组织 ID 列表
TARGET_GROUPS = ['G0050', 'G0007', 'G0016', 'G0013', 'G0064', 
                 'G0067', 'G0087', 'G1002', 'G0098', 'G0012']

# 基础 URL
BASE_URL = 'https://attack.mitre.org/groups/'

# 请求头，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

# 代理配置（如需使用代理，请取消注释并配置）
PROXIES = None
# PROXIES = {
#     'http': 'http://127.0.0.1:7890',
#     'https': 'http://127.0.0.1:7890',
# }


def clean_text(text):
    """清洁文本，去除多余空白字符"""
    if not text:
        return ""
    # 替换多个空白字符为单个空格
    text = ' '.join(text.split())
    return text.strip()


def fetch_page(url, group_id):
    """
    获取网页内容
    
    Args:
        url: 目标网址
        group_id: APT 组织 ID
    
    Returns:
        BeautifulSoup 对象或 None
    """
    try:
        logging.info(f"正在访问: {url}")
        response = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=30, verify=True)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        logging.info(f"成功获取 {group_id} 页面")
        return soup
        
    except requests.exceptions.Timeout:
        logging.error(f"{group_id} - 请求超时")
        return None
    except requests.exceptions.ConnectionError:
        logging.error(f"{group_id} - 网络连接错误")
        return None
    except requests.exceptions.HTTPError as e:
        logging.error(f"{group_id} - HTTP错误: {e}")
        return None
    except Exception as e:
        logging.error(f"{group_id} - 未知错误: {e}")
        return None


def extract_apt_name(soup, group_id):
    """
    提取 APT 组织名称
    
    Args:
        soup: BeautifulSoup 对象
        group_id: APT 组织 ID
    
    Returns:
        APT 组织名称
    """
    try:
        # 尝试从 h1 标签获取
        h1_tag = soup.find('h1')
        if h1_tag:
            name = clean_text(h1_tag.get_text())
            logging.info(f"{group_id} - 组织名称: {name}")
            return name
        
        # 备选方案：从 title 获取
        title_tag = soup.find('title')
        if title_tag:
            name = clean_text(title_tag.get_text().split('|')[0])
            logging.info(f"{group_id} - 从标题获取名称: {name}")
            return name
        
        logging.warning(f"{group_id} - 未找到组织名称，使用ID")
        return group_id
        
    except Exception as e:
        logging.error(f"{group_id} - 提取名称时出错: {e}")
        return group_id


def extract_description(soup, group_id):
    """
    提取描述信息
    
    Args:
        soup: BeautifulSoup 对象
        group_id: APT 组织 ID
    
    Returns:
        描述文本
    """
    try:
        # 优先查找 div.description-body
        desc_div = soup.find('div', class_='description-body')
        
        # 回退方案：查找 id 为 description 的元素
        if not desc_div:
            desc_div = soup.find(id='description')
        
        # 再次回退：查找包含 description 类的 div
        if not desc_div:
            desc_div = soup.find('div', class_=lambda x: x and 'description' in x)
        
        if desc_div:
            # 提取所有段落文本
            paragraphs = desc_div.find_all('p')
            if paragraphs:
                description = ' '.join([clean_text(p.get_text()) for p in paragraphs])
            else:
                description = clean_text(desc_div.get_text())
            
            logging.info(f"{group_id} - 描述长度: {len(description)} 字符")
            return description
        
        logging.warning(f"{group_id} - 未找到描述信息")
        return "无描述信息"
        
    except Exception as e:
        logging.error(f"{group_id} - 提取描述时出错: {e}")
        return "提取失败"


def extract_techniques_use(soup, group_id):
    """
    提取 Techniques Used 中的 Use 列内容
    
    Args:
        soup: BeautifulSoup 对象
        group_id: APT 组织 ID
    
    Returns:
        Use 用法文本（合并后）
    """
    try:
        # 查找 techniques-used 区域
        techniques_div = soup.find('div', id='techniques-used')
        
        # 备选方案：查找包含 techniques 的 div
        if not techniques_div:
            techniques_div = soup.find('div', class_=lambda x: x and 'techniques' in x.lower() if x else False)
        
        if not techniques_div:
            logging.warning(f"{group_id} - 未找到 techniques-used 区域")
            return "无Use信息"
        
        # 查找表格
        table = techniques_div.find('table')
        if not table:
            logging.warning(f"{group_id} - techniques-used 区域中未找到表格")
            return "无Use信息"
        
        # 查找所有行
        rows = table.find_all('tr')
        if len(rows) <= 1:  # 只有表头或没有数据
            logging.warning(f"{group_id} - 表格中无数据行")
            return "无Use信息"
        
        use_texts = []
        
        # 遍历数据行（跳过表头）
        for row in rows[1:]:
            cells = row.find_all('td')
            if cells:
                # Use 列是最后一列
                use_cell = cells[-1]
                use_text = clean_text(use_cell.get_text())
                if use_text:
                    use_texts.append(use_text)
        
        if use_texts:
            # 合并所有 Use 文本，用分号分隔
            combined_use = ' | '.join(use_texts)
            logging.info(f"{group_id} - 提取到 {len(use_texts)} 条 Use 记录")
            return combined_use
        else:
            logging.warning(f"{group_id} - Use 列无有效内容")
            return "无Use信息"
        
    except Exception as e:
        logging.error(f"{group_id} - 提取 Use 信息时出错: {e}")
        return "提取失败"


def crawl_apt_group(group_id, index):
    """
    爬取单个 APT 组织的信息
    
    Args:
        group_id: APT 组织 ID
        index: 序号
    
    Returns:
        包含组织信息的字典或 None
    """
    url = f"{BASE_URL}{group_id}/"
    
    # 获取页面
    soup = fetch_page(url, group_id)
    if not soup:
        return None
    
    # 提取各项信息
    apt_name = extract_apt_name(soup, group_id)
    description = extract_description(soup, group_id)
    use_info = extract_techniques_use(soup, group_id)
    
    # 构建结果
    result = {
        '序号': index,
        'APT组织名称': apt_name,
        '网址': url,
        '描述': description,
        'Use用法': use_info
    }
    
    logging.info(f"{group_id} - 数据采集完成")
    return result


def save_to_csv(data_list, filename='attack_groups.csv'):
    """
    将数据保存到 CSV 文件
    
    Args:
        data_list: 数据列表
        filename: 输出文件名
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['序号', 'APT组织名称', '网址', '描述', 'Use用法']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)
        
        logging.info(f"数据已成功保存到 {filename}")
        print(f"\n✅ 数据已保存到: {filename}")
        
    except Exception as e:
        logging.error(f"保存 CSV 文件时出错: {e}")
        print(f"\n❌ 保存失败: {e}")


def main():
    """主函数"""
    print("="*70)
    print("MITRE ATT&CK APT 组织威胁情报爬虫")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"目标组织数量: {len(TARGET_GROUPS)}")
    print("="*70 + "\n")
    
    logging.info("="*50)
    logging.info("开始采集 MITRE ATT&CK 威胁情报")
    logging.info(f"目标组织: {', '.join(TARGET_GROUPS)}")
    logging.info("="*50)
    
    results = []
    success_count = 0
    fail_count = 0
    
    # 遍历所有目标组织
    for index, group_id in enumerate(TARGET_GROUPS, start=1):
        print(f"\n[{index}/{len(TARGET_GROUPS)}] 正在采集 {group_id}...")
        
        # 爬取数据
        data = crawl_apt_group(group_id, index)
        
        if data:
            results.append(data)
            success_count += 1
            print(f"✅ {group_id} 采集成功")
        else:
            fail_count += 1
            print(f"❌ {group_id} 采集失败")
        
        # 礼貌性延迟，避免请求过快
        if index < len(TARGET_GROUPS):
            time.sleep(2)
    
    # 保存结果
    if results:
        save_to_csv(results)
    else:
        logging.warning("没有成功采集到任何数据")
        print("\n⚠️  警告: 没有采集到任何数据")
    
    # 打印统计信息
    print("\n" + "="*70)
    print("采集完成统计")
    print("="*70)
    print(f"成功: {success_count} 个组织")
    print(f"失败: {fail_count} 个组织")
    print(f"总计: {len(TARGET_GROUPS)} 个组织")
    print(f"成功率: {success_count/len(TARGET_GROUPS)*100:.1f}%")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    logging.info("="*50)
    logging.info(f"采集完成 - 成功: {success_count}, 失败: {fail_count}")
    logging.info("="*50)


if __name__ == '__main__':
    main()
