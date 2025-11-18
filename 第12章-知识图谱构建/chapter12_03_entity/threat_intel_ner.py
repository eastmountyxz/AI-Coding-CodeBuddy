#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
威胁情报实体识别系统
从MITRE ATT&CK威胁情报CSV中提取安全实体
"""

import pandas as pd
import re
import csv
from collections import defaultdict

# 实体识别模式（按优先级排序）
ENTITY_PATTERNS = {
    # AG - APT组织
    'AG': [
        r'\b(APT\d+|APT-\d+)\b',
        r'\b(Wizard\s+Spider|BRONZE\s+BUTLER|Kimsuky|Naikon|Bluenoroff|Stardust\s+Chollima)\b'
    ],
    
    # AEQ - 攻击工具/恶意软件家族
    'AEQ': [
        r'\b(Mimikatz|TrickBot|Ryuk|Conti|NESTEGG|NACHOCHEESE|Daserf|xxmm)\b',
        r'\b(X-Agent|X-Tunnel|WinIDS|Responder|HAMMERTOSS|CHOPSTICK|POSHSPY)\b',
        r'\b(HIGHNOON|POISONPLUG|HOMEUNIX|PowerShell\s+Empire|WinRAR)\b',
        r'\b(backdoor|ransomware|malware|implant|web\s+shell)s?\b'
    ],
    
    # AM - 攻击手法
    'AM': [
        r'\b(spearphishing|phishing)\b',
        r'\b(credential\s+dumping|credential\s+theft|credential\s+harvesting)\b',
        r'\b(lateral\s+movement|privilege\s+escalation)\b',
        r'\b(persistence|exfiltration|timestomping)\b',
        r'\b(keylogging|password\s+spraying)\b',
        r'\b(supply\s+chain\s+compromise|web\s+compromise)\b',
        r'\b(command\s+and\s+control|C2)\b'
    ],
    
    # AE - 攻击事件
    'AE': [
        r'\b(SolarWinds\s+Compromise)\b',
        r'\b(Bangladesh\s+Bank\s+heist)\b',
        r'\b(Hillary\s+Clinton\s+campaign)\b',
        r'\b(Democratic\s+National\s+Committee)\b',
        r'\b(Democratic\s+Congressional\s+Campaign\s+Committee)\b'
    ],
    
    # AT - 攻击目标/受害方
    'AT': [
        r'\b(Hillary\s+Clinton\s+campaign)\b',
        r'\b(Democratic\s+National\s+Committee)\b',
        r'\b(Democratic\s+Congressional\s+Campaign\s+Committee)\b',
        r'\b(Bangladesh\s+Bank)\b',
        r'\b(government|military|security\s+organizations)\b'
    ],
    
    # AI - 行业
    'AI': [
        r'\b(telecommunications?|telecom)\b',
        r'\b(healthcare|hospital)s?\b',
        r'\b(technology|tech)\b',
        r'\b(video\s+game|gaming)\b',
        r'\b(biotechnology|biotech)\b',
        r'\b(electronics\s+manufacturing)\b',
        r'\b(industrial\s+chemistry)\b',
        r'\b(oil\s+and\s+gas|energy)\b',
        r'\b(financial|banking|finance)\b',
        r'\b(cryptocurrency|crypto)\b'
    ],
    
    # RL - 区域/国家
    'RL': [
        r'\b(Vietnam|Vietnamese)\b',
        r'\b(Russia|Russian)\b',
        r'\b(China|Chinese)\b',
        r'\b(Iran|Iranian)\b',
        r'\b(North\s+Korea|North\s+Korean)\b',
        r'\b(South\s+Korea|South\s+Korean)\b',
        r'\b(Southeast\s+Asia)\b',
        r'\b(Europe|European)\b',
        r'\b(NATO)\b',
        r'\b(Philippines|Laos|Cambodia|Japan)\b',
        r'\b(U\.S\.|United\s+States|UK)\b'
    ],
    
    # SI - 软件/应用
    'SI': [
        r'\b(PowerShell)\b',
        r'\b(Microsoft\s+Office)\b',
        r'\b(WMI)\b',
        r'\b(Registry)\b',
        r'\b(RDP)\b',
        r'\b(cloud\s+storage)\b'
    ],
    
    # AV - CVE漏洞
    'AV': [
        r'\b(CVE-\d{4}-\d{4,})\b'
    ]
}

# 实体规范化映射
NORMALIZATION_MAP = {
    'telecoms': 'telecommunications',
    'telecom': 'telecommunications',
    'crypto': 'cryptocurrency',
    'biotech': 'biotechnology',
    'tech': 'technology',
    'u.s.': 'united states',
    'vietnamese': 'vietnam',
    'russian': 'russia',
    'chinese': 'china',
    'iranian': 'iran',
    'north korean': 'north korea',
    'south korean': 'south korea',
    'european': 'europe'
}

def normalize_entity(text):
    """规范化实体文本"""
    normalized = text.lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = re.sub(r'[^\w\s.-]', '', normalized)
    
    # 应用规范化映射
    for old, new in NORMALIZATION_MAP.items():
        if normalized == old:
            return new
    
    return normalized

def split_into_sentences(text):
    """将文本分割为句子"""
    # 按句号、问号、感叹号或管道符分割
    sentences = re.split(r'[.!?]\s+|\s*\|\s*', text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def extract_entities_from_text(text, url, group_name, row_id):
    """从文本中提取实体"""
    entities = []
    seen_entities = set()
    
    sentences = split_into_sentences(text)
    
    for sentence in sentences:
        if len(sentence) < 10:
            continue
        
        # 按标签类型提取实体
        for label, patterns in ENTITY_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                
                for match in matches:
                    entity_text = match.group(0).strip()
                    normalized = normalize_entity(entity_text)
                    
                    # 去重键：normalized_text + label
                    dedup_key = f"{normalized}_{label}"
                    
                    if dedup_key not in seen_entities:
                        seen_entities.add(dedup_key)
                        
                        # 提取标准ID（如CVE编号）
                        std_id = ''
                        if label == 'AV':
                            std_id = entity_text.upper()
                        
                        entities.append({
                            'row_id': row_id,
                            'entity_text': entity_text,
                            'label': label,
                            'normalized': normalized,
                            'std_id': std_id,
                            'context_sentence': sentence[:250],  # 限制上下文长度
                            'source_url': url,
                            'group_name': group_name
                        })
    
    return entities

def process_csv(input_file, output_file):
    """处理CSV文件并提取实体"""
    print(f"正在读取文件: {input_file}")
    
    # 读取CSV（尝试不同编码）
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(input_file, encoding='gbk')
        except:
            df = pd.read_csv(input_file, encoding='latin1')
    
    print(f"成功读取 {len(df)} 行数据")
    
    all_entities = []
    
    # 处理每一行
    for idx, row in df.iterrows():
        row_id = idx + 1
        group_name = str(row['APT组织名称'])
        url = str(row['网址'])
        
        # 合并描述和Use用法
        description = str(row['描述']) if pd.notna(row['描述']) else ''
        use_info = str(row['Use用法']) if pd.notna(row['Use用法']) else ''
        combined_text = f"{description} {use_info}"
        
        # 提取实体
        entities = extract_entities_from_text(combined_text, url, group_name, row_id)
        all_entities.extend(entities)
        
        print(f"  [{row_id}] {group_name}: 提取 {len(entities)} 个实体")
    
    # 保存结果
    output_df = pd.DataFrame(all_entities)
    output_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n提取完成！")
    print(f"  总实体数: {len(all_entities)}")
    print(f"  输出文件: {output_file}")
    
    # 打印统计信息
    print("\n实体类型统计:")
    label_counts = output_df['label'].value_counts()
    for label, count in label_counts.items():
        label_name = {
            'AG': 'APT组织',
            'AEQ': '攻击工具',
            'AM': '攻击手法',
            'AV': 'CVE漏洞',
            'AE': '攻击事件',
            'AT': '攻击目标',
            'AI': '行业',
            'RL': '区域/国家',
            'SI': '软件/应用',
            'MF': 'IOC指标'
        }.get(label, label)
        print(f"  {label} ({label_name}): {count}")
    
    return output_df

def main():
    """主函数"""
    print("="*70)
    print("威胁情报实体识别系统")
    print("="*70)
    
    input_file = 'attack_groups_sample.csv'
    output_file = 'threat_entities_full.csv'
    
    result_df = process_csv(input_file, output_file)
    
    print("\n示例实体（前10条）:")
    print(result_df.head(10)[['entity_text', 'label', 'group_name']].to_string())
    
    print("\n" + "="*70)

if __name__ == '__main__':
    main()
