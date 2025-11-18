#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import re
import csv

# 实体模式定义
PATTERNS = {
    'AG': [r'\b(APT\d+|APT-\d+|[A-Z][a-z]+\s+Spider|BRONZE\s+[A-Z]+|Kimsuky|Naikon|Bluenoroff|Stardust Chollima)\b'],
    'AEQ': [r'\b(Mimikatz|TrickBot|Ryuk|Conti|X-Agent|X-Tunnel|WinIDS|Responder|HAMMERTOSS|CHOPSTICK|POSHSPY|HIGHNOON|POISONPLUG|HOMEUNIX|NESTEGG|NACHOCHEESE|Daserf|xxmm|PowerShell Empire|WinRAR)\b'],
    'AM': [r'\b(spearphishing|credential dumping|lateral movement|persistence|exfiltration|timestomping|keylogging|credential harvesting|password spraying|supply chain compromise)\b', r'\b(web compromise|web shell)\b'],
    'AE': [r'\b(SolarWinds Compromise|Bangladesh Bank heist|Hillary Clinton campaign|Democratic National Committee)\b'],
    'AT': [r'\b(Democratic National Committee|Democratic Congressional Campaign Committee|Hillary Clinton campaign|Bangladesh Bank)\b'],
    'AI': [r'\b(telecommunications|healthcare|telecom|technology|video game|biotechnology|electronics manufacturing|industrial chemistry|oil and gas|financial|banking|cryptocurrency)\b'],
    'RL': [r'\b(Vietnam|Russia|China|Iran|North Korea|Southeast Asia|Europe|NATO|Philippines|Laos|Cambodia|Japan|South Korea)\b'],
    'SI': [r'\b(PowerShell|Microsoft Office|WMI|Registry|RDP|cloud storage)\b']
}

def extract_entities(text, url, group_name, row_id):
    results = []
    sentences = re.split(r'[.!?]\s+|\s+\|\s+', text)
    seen = set()
    
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 10:
            continue
            
        for label, patterns in PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, sent, re.IGNORECASE)
                for match in matches:
                    entity = match.group(0).strip()
                    normalized = entity.lower().replace('-', ' ').strip()
                    key = f"{normalized}_{label}"
                    
                    if key not in seen:
                        seen.add(key)
                        results.append({
                            'row_id': row_id,
                            'entity_text': entity,
                            'label': label,
                            'normalized': normalized,
                            'std_id': '',
                            'context_sentence': sent[:200],
                            'source_url': url,
                            'group_name': group_name
                        })
    return results

def main():
    df = pd.read_csv('attack_groups_sample.csv', encoding='gbk')
    all_entities = []
    
    for idx, row in df.iterrows():
        text = str(row['描述']) + ' ' + str(row['Use用法'])
        entities = extract_entities(text, row['网址'], row['APT组织名称'], idx+1)
        all_entities.extend(entities)
    
    output_df = pd.DataFrame(all_entities)
    output_df.to_csv('threat_entities.csv', index=False, encoding='utf-8')
    print(f"提取完成！共 {len(all_entities)} 个实体")

if __name__ == '__main__':
    main()
