# 威胁情报实体识别系统

## 📋 项目概述

本系统从 MITRE ATT&CK 威胁情报 CSV 文件中自动提取安全实体，支持句级实体识别、去重、规范化处理。

## 🎯 功能特性

### 支持的实体类型（10类）

| 标签 | 类型 | 示例 |
|------|------|------|
| **AG** | APT组织 | APT32, APT28, Wizard Spider |
| **AEQ** | 攻击工具/恶意软件 | Mimikatz, TrickBot, Ryuk |
| **AM** | 攻击手法 | spearphishing, credential dumping |
| **AV** | 漏洞/CVE | CVE-2021-1234 |
| **AE** | 攻击事件 | SolarWinds Compromise |
| **AT** | 攻击目标/受害方 | Democratic National Committee |
| **AI** | 行业 | telecommunications, healthcare |
| **RL** | 区域/国家 | Vietnam, Russia, China |
| **SI** | 软件/应用 | PowerShell, Microsoft Office |
| **MF** | IOC指标 | hash/IP/domain |

## 📊 处理结果

### 统计数据
- **总实体数**: 137 个
- **处理组织数**: 10 个 APT 组织
- **去重处理**: 自动去除重复实体

### 实体类型分布
```
AEQ (攻击工具):    35 个
AM  (攻击手法):    30 个
RL  (区域/国家):   18 个
AI  (行业):        14 个
AG  (APT组织):     13 个
AT  (攻击目标):    12 个
SI  (软件/应用):    9 个
AE  (攻击事件):     6 个
```

## 📁 文件说明

### 输入文件
- `attack_groups_sample.csv` - MITRE ATT&CK 威胁情报数据
  - 字段：序号, APT组织名称, 网址, 描述, Use用法

### 输出文件
- `threat_entities_full.csv` - 完整实体识别结果
  - 字段：row_id, entity_text, label, normalized, std_id, context_sentence, source_url, group_name

### 脚本文件
- `threat_intel_ner.py` - 完整版实体识别脚本（推荐）
- `extract.py` - 简化版脚本

## 🚀 使用方法

### 1. 安装依赖
```bash
pip install pandas
```

### 2. 运行识别
```bash
python threat_intel_ner.py
```

### 3. 查看结果
```bash
# 查看CSV文件
cat threat_entities_full.csv

# 使用Python查看统计
python -c "import pandas as pd; df=pd.read_csv('threat_entities_full.csv', encoding='utf-8-sig'); print(df.head(20))"
```

## 📖 输出格式说明

### CSV字段详解

| 字段名 | 说明 | 示例 |
|--------|------|------|
| row_id | 源CSV行号 | 1 |
| entity_text | 原始实体文本 | APT32 |
| label | 实体标签 | AG |
| normalized | 规范化后的文本 | apt32 |
| std_id | 标准ID（如CVE编号） | CVE-2021-1234 |
| context_sentence | 上下文句子（最多250字符） | APT32 is a suspected... |
| source_url | 来源网址 | https://attack.mitre.org/groups/G0050/ |
| group_name | APT组织名称 | APT32 |

## 🔍 实体识别规则

### 1. 句级抽取
- 按句号、问号、感叹号或管道符分割文本
- 每个句子独立识别实体
- 保留完整上下文信息

### 2. 去重机制
- 基于 `normalized_text + label` 组合去重
- 同一实体在不同句子中只保留首次出现

### 3. 规范化处理
- 转小写
- 去除多余空白
- 统一同义词（如 telecom → telecommunications）

### 4. 特殊处理
- **CVE识别**: 自动提取CVE编号并填入std_id
- **ATT&CK编号**: 识别技术编号（如T1566）
- **IOC指标**: IP、域名、hash归入MF类别

## 📈 示例输出

```csv
row_id,entity_text,label,normalized,std_id,context_sentence,source_url,group_name
1,APT32,AG,apt32,,APT32 is a suspected Vietnam-based threat group...,https://attack.mitre.org/groups/G0050/,APT32
1,Vietnam,RL,vietnam,,APT32 is a suspected Vietnam-based threat group...,https://attack.mitre.org/groups/G0050/,APT32
2,Mimikatz,AEQ,mimikatz,,APT28 has used credential dumping tools such as Mimikatz,https://attack.mitre.org/groups/G0007/,APT28
```

## 🎨 扩展功能

### 自定义实体类型
编辑 `threat_intel_ner.py` 中的 `ENTITY_PATTERNS` 字典：

```python
ENTITY_PATTERNS = {
    'NEW_TYPE': [
        r'\b(pattern1|pattern2)\b',
        r'\b(pattern3)\b'
    ]
}
```

### 添加规范化规则
编辑 `NORMALIZATION_MAP` 字典：

```python
NORMALIZATION_MAP = {
    'old_term': 'new_term',
    'synonym': 'canonical_form'
}
```

## 📊 后续应用

提取的实体可用于：
1. **知识图谱构建** - 构建APT组织关系图谱
2. **威胁情报分析** - 分析攻击模式和趋势
3. **安全态势感知** - 识别潜在威胁
4. **情报关联分析** - 关联不同来源的威胁情报

## 🔧 常见问题

### Q: 编码错误怎么办？
A: 脚本自动尝试 utf-8、gbk、latin1 编码，通常可自动处理。

### Q: 如何添加新的APT组织？
A: 在输入CSV中添加新行，脚本会自动处理。

### Q: 实体识别不准确？
A: 调整 `ENTITY_PATTERNS` 中的正则表达式模式。

### Q: 如何过滤特定类型实体？
A: 使用pandas过滤：
```python
df = pd.read_csv('threat_entities_full.csv')
tools = df[df['label'] == 'AEQ']  # 只看攻击工具
```

## 📝 注意事项

1. **敏感信息**: 脚本跳过敏感或不确定内容
2. **上下文长度**: 限制为250字符，避免过长
3. **去重策略**: 基于规范化文本+标签，确保唯一性
4. **性能**: 处理10行数据约1-2秒

## 🎯 最佳实践

1. **定期更新模式**: 根据新威胁更新识别模式
2. **人工审核**: 对关键实体进行人工验证
3. **增量处理**: 新数据追加到现有结果
4. **版本控制**: 保存不同版本的识别结果

## 📞 技术支持

如有问题或建议，请查看：
- MITRE ATT&CK官网：https://attack.mitre.org
- 项目文档：README.md
