#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
威胁情报实体分析脚本
分析提取的实体，生成统计报告
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

def load_entities(file_path='threat_entities_full.csv'):
    """加载实体数据"""
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except:
        df = pd.read_csv(file_path, encoding='utf-8')
    return df

def analyze_entity_distribution(df):
    """分析实体类型分布"""
    print("\n" + "="*70)
    print("实体类型分布分析")
    print("="*70)
    
    label_names = {
        'AG': 'APT组织',
        'AEQ': '攻击工具/恶意软件',
        'AM': '攻击手法',
        'AV': 'CVE漏洞',
        'AE': '攻击事件',
        'AT': '攻击目标',
        'AI': '行业',
        'RL': '区域/国家',
        'SI': '软件/应用',
        'MF': 'IOC指标'
    }
    
    label_counts = df['label'].value_counts()
    
    for label, count in label_counts.items():
        name = label_names.get(label, label)
        percentage = (count / len(df)) * 100
        print(f"{label:5s} {name:20s} {count:4d} ({percentage:5.1f}%)")
    
    print(f"\n总计: {len(df)} 个实体")
    
    return label_counts

def analyze_top_entities(df, top_n=10):
    """分析最常见的实体"""
    print("\n" + "="*70)
    print(f"Top {top_n} 最常见实体")
    print("="*70)
    
    entity_counts = df['normalized'].value_counts().head(top_n)
    
    for idx, (entity, count) in enumerate(entity_counts.items(), 1):
        # 获取该实体的标签
        labels = df[df['normalized'] == entity]['label'].unique()
        label_str = ', '.join(labels)
        print(f"{idx:2d}. {entity:30s} {count:3d}次  [{label_str}]")

def analyze_by_group(df):
    """按APT组织分析"""
    print("\n" + "="*70)
    print("各APT组织实体统计")
    print("="*70)
    
    group_counts = df.groupby('group_name').size().sort_values(ascending=False)
    
    for group, count in group_counts.items():
        print(f"{group:20s} {count:3d} 个实体")

def analyze_attack_tools(df):
    """分析攻击工具"""
    print("\n" + "="*70)
    print("攻击工具/恶意软件 Top 10")
    print("="*70)
    
    tools = df[df['label'] == 'AEQ']['entity_text'].value_counts().head(10)
    
    for idx, (tool, count) in enumerate(tools.items(), 1):
        print(f"{idx:2d}. {tool:25s} {count:2d}次")

def analyze_techniques(df):
    """分析攻击手法"""
    print("\n" + "="*70)
    print("攻击手法 Top 10")
    print("="*70)
    
    techniques = df[df['label'] == 'AM']['entity_text'].value_counts().head(10)
    
    for idx, (tech, count) in enumerate(techniques.items(), 1):
        print(f"{idx:2d}. {tech:30s} {count:2d}次")

def analyze_regions(df):
    """分析地理分布"""
    print("\n" + "="*70)
    print("地理区域分布")
    print("="*70)
    
    regions = df[df['label'] == 'RL']['entity_text'].value_counts()
    
    for idx, (region, count) in enumerate(regions.items(), 1):
        print(f"{idx:2d}. {region:20s} {count:2d}次")

def analyze_industries(df):
    """分析目标行业"""
    print("\n" + "="*70)
    print("目标行业分布")
    print("="*70)
    
    industries = df[df['label'] == 'AI']['entity_text'].value_counts()
    
    for idx, (industry, count) in enumerate(industries.items(), 1):
        print(f"{idx:2d}. {industry:30s} {count:2d}次")

def generate_report(df):
    """生成完整分析报告"""
    print("\n" + "="*70)
    print("威胁情报实体分析报告")
    print("="*70)
    
    # 基本统计
    print(f"\n数据概览:")
    print(f"  总实体数: {len(df)}")
    print(f"  唯一实体数: {df['normalized'].nunique()}")
    print(f"  APT组织数: {df['group_name'].nunique()}")
    print(f"  实体类型数: {df['label'].nunique()}")
    
    # 各类分析
    analyze_entity_distribution(df)
    analyze_top_entities(df)
    analyze_by_group(df)
    analyze_attack_tools(df)
    analyze_techniques(df)
    analyze_regions(df)
    analyze_industries(df)
    
    print("\n" + "="*70)

def export_summary(df, output_file='entity_summary.csv'):
    """导出摘要统计"""
    summary_data = []
    
    # 按组织和标签统计
    for group in df['group_name'].unique():
        group_df = df[df['group_name'] == group]
        
        for label in df['label'].unique():
            count = len(group_df[group_df['label'] == label])
            if count > 0:
                summary_data.append({
                    'group_name': group,
                    'label': label,
                    'count': count
                })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n摘要已保存至: {output_file}")

def main():
    """主函数"""
    # 加载数据
    df = load_entities('threat_entities_full.csv')
    
    # 生成报告
    generate_report(df)
    
    # 导出摘要
    export_summary(df)

if __name__ == '__main__':
    main()
