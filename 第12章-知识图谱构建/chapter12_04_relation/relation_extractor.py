#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
威胁情报关系抽取系统
从MITRE ATT&CK威胁情报中提取实体间关系
"""

import pandas as pd
import re
from collections import defaultdict

# 关系类型定义
RELATION_PATTERNS = {
    'uses': [
        r'(has\s+used|used|using|uses|deployed|employs)',
        r'(with|including|such\s+as)'
    ],
    'targets': [
        r'(target|targeting|targeted|focus\s+on|against)',
        r'(attack|attacking|attacked|compromise|compromised)'
    ],
    'operates_in': [
        r'(based|operates?\s+in|active\s+in|located\s+in)',
        r'(from|origins?)'
    ],
    'attacks': [
        r'(compromised|breached|attacked|interfere)',
        r'(linked\s+to|attributed\s+to|perpetrated)'
    ],
    'exploits_vuln': [
        r'(exploit|exploited|exploiting|leverag)',
        r'(CVE-\d{4}-\d+)'
    ],
    'exploits_software': [
        r'(via|through|using)',
        r'(PowerShell|WMI|Registry|RDP)'
    ]
}

def load_data():
    """加载数据"""
    # 加载原始CSV
    try:
        threat_df = pd.read_csv('attack_groups_sample.csv', encoding='utf-8')
    except:
        threat_df = pd.read_csv('attack_groups_sample.csv', encoding='gbk')
    
    # 加载实体CSV
    try:
        entities_df = pd.read_csv('threat_entities_full.csv', encoding='utf-8-sig')
    except:
        entities_df = pd.read_csv('threat_entities_full.csv', encoding='utf-8')
    
    return threat_df, entities_df

def build_entity_index(entities_df):
    """构建实体索引"""
    entity_map = defaultdict(list)
    
    for _, row in entities_df.iterrows():
        entity_text = row['entity_text'].lower()
        entity_map[entity_text].append({
            'text': row['entity_text'],
            'label': row['label'],
            'normalized': row['normalized'],
            'group': row['group_name']
        })
    
    return entity_map

def extract_relations_from_sentence(sentence, group_name, entity_map, url):
    """从句子中提取关系"""
    relations = []
    sentence_lower = sentence.lower()
    
    # 查找句子中的实体
    found_entities = []
    for entity_key, entity_list in entity_map.items():
        if entity_key in sentence_lower:
            for entity_info in entity_list:
                found_entities.append(entity_info)
    
    if len(found_entities) < 2:
        return relations
    
    # 关系1: 组织 → 使用 → 工具/家族
    if re.search(r'(has\s+used|used|deployed)', sentence_lower):
        for entity in found_entities:
            if entity['label'] == 'AEQ':  # 工具
                relations.append({
                    'head': group_name,
                    'relation': 'uses',
                    'tail': entity['text'],
                    'evidence': sentence[:200]
                })
    
    # 关系2: 组织 → 针对 → 行业/目标
    if re.search(r'(target|targeting|targeted)', sentence_lower):
        for entity in found_entities:
            if entity['label'] in ['AI', 'AT']:  # 行业或目标
                relations.append({
                    'head': group_name,
                    'relation': 'targets',
                    'tail': entity['text'],
                    'evidence': sentence[:200]
                })
    
    # 关系3: 组织 → 活动于 → 区域/国家
    if re.search(r'(based|operates|active|origins?)', sentence_lower):
        for entity in found_entities:
            if entity['label'] == 'RL':  # 区域
                relations.append({
                    'head': group_name,
                    'relation': 'operates_in',
                    'tail': entity['text'],
                    'evidence': sentence[:200]
                })
    
    # 关系4: 组织 → 攻击 → 机构/国家
    if re.search(r'(compromised|attacked|breached|interfere)', sentence_lower):
        for entity in found_entities:
            if entity['label'] in ['AT', 'RL']:  # 目标或区域
                relations.append({
                    'head': group_name,
                    'relation': 'attacks',
                    'tail': entity['text'],
                    'evidence': sentence[:200]
                })
    
    # 关系5: 组织 → 利用 → 软件
    if re.search(r'(via|through|using|with)', sentence_lower):
        for entity in found_entities:
            if entity['label'] == 'SI':  # 软件
                relations.append({
                    'head': group_name,
                    'relation': 'exploits_software',
                    'tail': entity['text'],
                    'evidence': sentence[:200]
                })
    
    # 关系6: 事件 → 涉及 → 组织
    for entity in found_entities:
        if entity['label'] == 'AE':  # 事件
            relations.append({
                'head': entity['text'],
                'relation': 'involves',
                'tail': group_name,
                'evidence': sentence[:200]
            })
    
    return relations

def extract_all_relations(threat_df, entities_df):
    """提取所有关系"""
    entity_map = build_entity_index(entities_df)
    all_relations = []
    seen_relations = set()
    
    print("开始提取关系...")
    
    for idx, row in threat_df.iterrows():
        group_name = row['APT组织名称']
        url = row['网址']
        
        # 合并描述和Use用法
        description = str(row['描述']) if pd.notna(row['描述']) else ''
        use_info = str(row['Use用法']) if pd.notna(row['Use用法']) else ''
        combined_text = f"{description} {use_info}"
        
        # 分句
        sentences = re.split(r'[.!?]\s+|\s*\|\s*', combined_text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 15:
                continue
            
            # 提取关系
            relations = extract_relations_from_sentence(
                sentence, group_name, entity_map, url
            )
            
            for rel in relations:
                # 去重
                rel_key = f"{rel['head']}_{rel['relation']}_{rel['tail']}"
                if rel_key not in seen_relations:
                    seen_relations.add(rel_key)
                    all_relations.append(rel)
        
        print(f"  [{idx+1}] {group_name}: 提取 {len([r for r in all_relations if r['head'] == group_name or r['tail'] == group_name])} 个关系")
    
    return all_relations

def save_relations(relations, output_file='threat_relations.csv'):
    """保存关系到CSV"""
    df = pd.DataFrame(relations)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n关系已保存到: {output_file}")
    return df

def analyze_relations(relations_df):
    """分析关系统计"""
    print("\n" + "="*70)
    print("关系抽取统计")
    print("="*70)
    
    print(f"\n总关系数: {len(relations_df)}")
    
    print("\n关系类型分布:")
    relation_counts = relations_df['relation'].value_counts()
    for rel, count in relation_counts.items():
        print(f"  {rel:20s} {count:3d}")
    
    print("\n示例关系（前15条）:")
    print(relations_df.head(15)[['head', 'relation', 'tail']].to_string(index=False))

def main():
    """主函数"""
    print("="*70)
    print("威胁情报关系抽取系统")
    print("="*70 + "\n")
    
    # 加载数据
    threat_df, entities_df = load_data()
    print(f"加载 {len(threat_df)} 个APT组织")
    print(f"加载 {len(entities_df)} 个实体\n")
    
    # 提取关系
    relations = extract_all_relations(threat_df, entities_df)
    
    # 保存关系
    relations_df = save_relations(relations)
    
    # 分析统计
    analyze_relations(relations_df)
    
    print("\n" + "="*70)

if __name__ == '__main__':
    main()
