#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成威胁情报知识图谱HTML"""
import pandas as pd
import json

# 读取数据
entities = pd.read_csv('threat_entities_full.csv', encoding='utf-8-sig')
relations = pd.read_csv('threat_relations.csv', encoding='utf-8-sig')

# 准备节点和边数据
nodes_dict = {}
for _, row in entities.iterrows():
    node_id = row['entity_text']
    if node_id not in nodes_dict:
        nodes_dict[node_id] = {
            'id': node_id,
            'label': row['label'],
            'group': row['group_name'],
            'normalized': row['normalized']
        }

nodes = list(nodes_dict.values())
links = []
for _, row in relations.iterrows():
    links.append({
        'source': row['head'],
        'target': row['tail'],
        'relation': row['relation'],
        'evidence': row['evidence'][:100]
    })

# 生成HTML
html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>威胁情报安全知识图谱</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; overflow: hidden; }}
        #container {{ display: flex; height: 100vh; }}
        #graph {{ flex: 1; background: #1a1a2e; position: relative; }}
        #sidebar {{ width: 350px; background: #16213e; color: #fff; padding: 20px; overflow-y: auto; border-left: 2px solid #0f3460; }}
        #controls {{ position: absolute; top: 20px; left: 20px; z-index: 100; }}
        .btn {{ background: #0f3460; color: #fff; border: none; padding: 10px 20px; margin: 5px; cursor: pointer; border-radius: 5px; font-size: 14px; }}
        .btn:hover {{ background: #1a5490; }}
        #search {{ width: 250px; padding: 10px; border: 2px solid #0f3460; border-radius: 5px; font-size: 14px; }}
        #legend {{ position: absolute; bottom: 20px; left: 20px; background: rgba(15,52,96,0.9); padding: 15px; border-radius: 10px; color: #fff; }}
        .legend-item {{ margin: 5px 0; display: flex; align-items: center; }}
        .legend-color {{ width: 20px; height: 20px; border-radius: 50%; margin-right: 10px; }}
        .node {{ cursor: pointer; stroke: #fff; stroke-width: 2px; }}
        .link {{ stroke: #666; stroke-opacity: 0.6; }}
        .link-label {{ font-size: 10px; fill: #aaa; pointer-events: none; }}
        .tooltip {{ position: absolute; background: rgba(0,0,0,0.9); color: #fff; padding: 10px; border-radius: 5px; pointer-events: none; display: none; max-width: 300px; z-index: 1000; }}
        h2 {{ color: #4ecca3; margin-bottom: 15px; }}
        .relation-item {{ background: #0f3460; padding: 10px; margin: 10px 0; border-radius: 5px; border-left: 3px solid #4ecca3; }}
        .relation-item strong {{ color: #4ecca3; }}
    </style>
</head>
<body>
    <div id="container">
        <div id="graph">
            <div id="controls">
                <input type="text" id="search" placeholder="搜索节点..." />
                <button class="btn" onclick="resetView()">重置视图</button>
                <button class="btn" onclick="exportPNG()">导出PNG</button>
            </div>
            <div id="legend">
                <div style="font-weight:bold;margin-bottom:10px;">节点类型</div>
                <div class="legend-item"><div class="legend-color" style="background:#ff6b6b"></div>APT组织 (AG)</div>
                <div class="legend-item"><div class="legend-color" style="background:#4ecdc4"></div>攻击工具 (AEQ)</div>
                <div class="legend-item"><div class="legend-color" style="background:#ffd93d"></div>攻击手法 (AM)</div>
                <div class="legend-item"><div class="legend-color" style="background:#95e1d3"></div>攻击事件 (AE)</div>
                <div class="legend-item"><div class="legend-color" style="background:#ff9ff3"></div>攻击目标 (AT)</div>
                <div class="legend-item"><div class="legend-color" style="background:#a8dadc"></div>行业 (AI)</div>
                <div class="legend-item"><div class="legend-color" style="background:#f4a261"></div>区域/国家 (RL)</div>
                <div class="legend-item"><div class="legend-color" style="background:#e76f51"></div>软件/应用 (SI)</div>
            </div>
            <div class="tooltip" id="tooltip"></div>
        </div>
        <div id="sidebar">
            <h2>知识图谱信息</h2>
            <div id="info">
                <p>节点数: {len(nodes)}</p>
                <p>关系数: {len(links)}</p>
                <p style="margin-top:15px;color:#aaa;">点击节点查看详情</p>
            </div>
        </div>
    </div>

    <script>
        const graphData = {json.dumps({'nodes': nodes, 'links': links}, ensure_ascii=False)};
        
        const width = window.innerWidth - 350;
        const height = window.innerHeight;
        
        const colorMap = {{
            'AG': '#ff6b6b', 'AEQ': '#4ecdc4', 'AM': '#ffd93d', 'AE': '#95e1d3',
            'AT': '#ff9ff3', 'AI': '#a8dadc', 'RL': '#f4a261', 'SI': '#e76f51', 'AV': '#e63946', 'MF': '#06ffa5'
        }};
        
        const svg = d3.select('#graph').append('svg')
            .attr('width', width).attr('height', height);
        
        const g = svg.append('g');
        
        const zoom = d3.zoom()
            .scaleExtent([0.1, 10])
            .on('zoom', (event) => g.attr('transform', event.transform));
        svg.call(zoom);
        
        const simulation = d3.forceSimulation(graphData.nodes)
            .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(30));
        
        const link = g.append('g').selectAll('line')
            .data(graphData.links).enter().append('line')
            .attr('class', 'link').attr('stroke-width', 2);
        
        const linkLabel = g.append('g').selectAll('text')
            .data(graphData.links).enter().append('text')
            .attr('class', 'link-label')
            .text(d => d.relation);
        
        const node = g.append('g').selectAll('circle')
            .data(graphData.nodes).enter().append('circle')
            .attr('class', 'node')
            .attr('r', d => d.label === 'AG' ? 12 : 8)
            .attr('fill', d => colorMap[d.label] || '#999')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended))
            .on('click', nodeClicked)
            .on('mouseover', showTooltip)
            .on('mouseout', hideTooltip);
        
        const nodeLabel = g.append('g').selectAll('text')
            .data(graphData.nodes).enter().append('text')
            .attr('font-size', 10).attr('fill', '#fff')
            .attr('text-anchor', 'middle').attr('dy', 20)
            .text(d => d.id.length > 15 ? d.id.substring(0, 15) + '...' : d.id);
        
        simulation.on('tick', () => {{
            link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
            linkLabel.attr('x', d => (d.source.x + d.target.x) / 2)
                .attr('y', d => (d.source.y + d.target.y) / 2);
            node.attr('cx', d => d.x).attr('cy', d => d.y);
            nodeLabel.attr('x', d => d.x).attr('y', d => d.y);
        }});
        
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
        }}
        function dragged(event, d) {{ d.fx = event.x; d.fy = event.y; }}
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
        }}
        
        function showTooltip(event, d) {{
            const tooltip = d3.select('#tooltip');
            tooltip.style('display', 'block')
                .html(`<strong>${{d.id}}</strong><br>Type: ${{d.label}}<br>Group: ${{d.group}}`)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 10) + 'px');
        }}
        
        function hideTooltip() {{ d3.select('#tooltip').style('display', 'none'); }}
        
        function nodeClicked(event, d) {{
            const neighbors = new Set();
            const relations = [];
            
            graphData.links.forEach(link => {{
                if (link.source.id === d.id) {{
                    neighbors.add(link.target.id);
                    relations.push({{type: 'out', relation: link.relation, target: link.target.id, evidence: link.evidence}});
                }}
                if (link.target.id === d.id) {{
                    neighbors.add(link.source.id);
                    relations.push({{type: 'in', relation: link.relation, source: link.source.id, evidence: link.evidence}});
                }}
            }});
            
            node.attr('opacity', n => n.id === d.id || neighbors.has(n.id) ? 1 : 0.2);
            link.attr('opacity', l => l.source.id === d.id || l.target.id === d.id ? 1 : 0.1);
            
            let html = `<h2>${{d.id}}</h2><p>Type: ${{d.label}}<br>Group: ${{d.group}}</p><hr style="border-color:#4ecca3;margin:15px 0">`;
            html += `<h3 style="color:#4ecca3">关联关系 (${{relations.length}})</h3>`;
            relations.forEach(r => {{
                if (r.type === 'out') {{
                    html += `<div class="relation-item"><strong>${{d.id}}</strong> → ${{r.relation}} → ${{r.target}}<br><small>${{r.evidence}}</small></div>`;
                }} else {{
                    html += `<div class="relation-item"><strong>${{r.source}}</strong> → ${{r.relation}} → ${{d.id}}<br><small>${{r.evidence}}</small></div>`;
                }}
            }});
            document.getElementById('sidebar').innerHTML = html;
        }}
        
        d3.select('#search').on('input', function() {{
            const term = this.value.toLowerCase();
            if (!term) {{ resetView(); return; }}
            const found = graphData.nodes.find(n => n.id.toLowerCase().includes(term));
            if (found) {{
                const transform = d3.zoomIdentity.translate(width/2 - found.x*2, height/2 - found.y*2).scale(2);
                svg.transition().duration(750).call(zoom.transform, transform);
                node.attr('opacity', n => n.id === found.id ? 1 : 0.3);
            }}
        }});
        
        function resetView() {{
            svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity);
            node.attr('opacity', 1);
            link.attr('opacity', 1);
            document.getElementById('search').value = '';
        }}
        
        function exportPNG() {{
            const svgElement = document.querySelector('#graph svg');
            const serializer = new XMLSerializer();
            const svgString = serializer.serializeToString(svgElement);
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            const img = new Image();
            img.onload = () => {{
                ctx.drawImage(img, 0, 0);
                const link = document.createElement('a');
                link.download = 'threat_knowledge_graph.png';
                link.href = canvas.toDataURL();
                link.click();
            }};
            img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgString)));
        }}
    </script>
</body>
</html>'''

# 保存文件
with open('threat_knowledge_graph.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ 知识图谱HTML文件已生成: threat_knowledge_graph.html")
print(f"   节点数: {len(nodes)}")
print(f"   关系数: {len(links)}")
print("\n请在浏览器中打开该文件查看知识图谱")
