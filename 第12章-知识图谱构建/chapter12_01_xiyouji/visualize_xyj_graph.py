#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
西游记知识图谱可视化工具
从 entities.csv 和 relations.csv 读取数据，生成知识图谱可视化
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体，避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载实体和关系数据"""
    print("正在加载数据...")
    entities = pd.read_csv('entities.csv', encoding='utf-8')
    relations = pd.read_csv('relations.csv', encoding='utf-8')
    print(f"成功加载 {len(entities)} 个实体和 {len(relations)} 条关系")
    return entities, relations

def build_graph(entities, relations):
    """构建知识图谱"""
    print("正在构建知识图谱...")
    G = nx.DiGraph()
    
    # 添加节点
    for _, row in entities.iterrows():
        G.add_node(row['label'], entity_type=row['type'], entity_id=row['id'])
    
    # 添加边
    for _, row in relations.iterrows():
        G.add_edge(row['head'], row['tail'], relation=row['relation'])
    
    print(f"图谱包含 {G.number_of_nodes()} 个节点和 {G.number_of_edges()} 条边")
    return G

def visualize_graph(G, entities, output_file='xyj_graph.png'):
    """可视化知识图谱"""
    print("正在生成可视化图谱...")
    
    # 创建大图
    plt.figure(figsize=(24, 18))
    
    # 使用spring布局
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # 定义实体类型对应的颜色
    color_map = {
        '人物': '#FF6B6B',  # 红色
        '地点': '#4ECDC4',  # 青色
        '法宝': '#FFD93D',  # 黄色
        '事件': '#95E1D3'   # 绿色
    }
    
    # 为每个节点分配颜色
    node_colors = []
    entity_type_map = dict(zip(entities['label'], entities['type']))
    
    for node in G.nodes():
        entity_type = entity_type_map.get(node, '人物')
        node_colors.append(color_map.get(entity_type, '#CCCCCC'))
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=1500,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=2)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          arrows=True,
                          arrowsize=15,
                          arrowstyle='->',
                          width=1.5,
                          alpha=0.6,
                          connectionstyle='arc3,rad=0.1')
    
    # 绘制节点标签
    nx.draw_networkx_labels(G, pos,
                           font_size=10,
                           font_weight='bold',
                           font_family='sans-serif')
    
    # 绘制边标签（关系）
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=edge_labels,
                                 font_size=8,
                                 font_color='darkred',
                                 bbox=dict(boxstyle='round,pad=0.3', 
                                          facecolor='white', 
                                          edgecolor='none',
                                          alpha=0.7))
    
    # 添加图例
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_map['人物'], edgecolor='black', label='人物'),
        Patch(facecolor=color_map['地点'], edgecolor='black', label='地点'),
        Patch(facecolor=color_map['法宝'], edgecolor='black', label='法宝'),
        Patch(facecolor=color_map['事件'], edgecolor='black', label='事件')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14, framealpha=0.9)
    
    # 设置标题
    plt.title('《西游记》知识图谱', fontsize=24, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"知识图谱已保存至: {output_file}")
    
    # 显示图片
    plt.show()

def print_statistics(entities, relations):
    """打印统计信息"""
    print("\n" + "="*50)
    print("知识图谱统计信息")
    print("="*50)
    
    # 实体统计
    print("\n【实体统计】")
    entity_counts = entities['type'].value_counts()
    for entity_type, count in entity_counts.items():
        print(f"  {entity_type}: {count} 个")
    print(f"  总计: {len(entities)} 个实体")
    
    # 关系统计
    print("\n【关系统计】")
    relation_counts = relations['relation'].value_counts()
    for relation, count in relation_counts.items():
        print(f"  {relation}: {count} 条")
    print(f"  总计: {len(relations)} 条关系")
    print("="*50 + "\n")

def main():
    """主函数"""
    print("\n" + "="*50)
    print("《西游记》知识图谱可视化系统")
    print("="*50 + "\n")
    
    # 加载数据
    entities, relations = load_data()
    
    # 打印统计信息
    print_statistics(entities, relations)
    
    # 构建图谱
    graph = build_graph(entities, relations)
    
    # 可视化
    visualize_graph(graph, entities, 'xyj_graph.png')
    
    print("\n处理完成！")

if __name__ == '__main__':
    main()
