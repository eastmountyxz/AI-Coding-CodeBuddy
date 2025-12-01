# 新媒体营销与热榜系统

## 项目简介

这是一个功能完整的新媒体营销与热榜系统，实现了内容聚合与数据采集功能。系统包括数据采集、数据存储和前端展示三个核心模块。

## 功能特点

### 1. 数据采集模块（高优先级）
- ✅ 多平台内容采集（微博、知乎、抖音）
- ✅ 数据清洗（去重、关键信息提取）
- ✅ 反爬虫策略（User-Agent轮换、请求延时）
- ✅ 爬虫代码模板

### 2. 数据存储模块（高优先级）
- ✅ JSON结构化存储
- ✅ 完整的增删查改（CRUD）操作
- ✅ 数据统计功能
- ✅ 批量操作支持

### 3. 前端展示模块（中优先级）
- ✅ 响应式界面设计（Bootstrap）
- ✅ 数据列表展示
- ✅ 平台筛选功能
- ✅ 关键词搜索功能
- ✅ 数据刷新功能
- ✅ Vue.js数据绑定
- ✅ Axios异步请求

## 技术栈

### 前端
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5.3
- Vue.js 3
- Axios

### 后端
- Python 3.8+
- Flask（Web框架）
- Requests（HTTP请求）
- BeautifulSoup4（HTML解析）

### 数据存储
- JSON文件存储

## 项目结构

```
├── index.html          # 前端主页面
├── app.js              # Vue.js应用逻辑
├── style.css           # 样式文件
├── api.py              # Flask API接口
├── crawler.py          # 数据采集模块
├── data_storage.py     # 数据存储模块
├── data.json           # 数据文件（自动生成）
├── requirements.txt    # Python依赖
└── README.md           # 项目文档
```

## 安装与运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端API服务

```bash
python api.py
```

API服务将在 `http://localhost:5000` 启动

### 3. 打开前端页面

直接在浏览器中打开 `index.html` 文件，或使用本地服务器：

```bash
# 使用Python内置服务器
python -m http.server 8080
```

然后访问 `http://localhost:8080`

## 使用说明

### 数据采集
1. 点击"开始采集数据"按钮
2. 系统将自动从多个平台采集热榜数据
3. 采集完成后数据会自动保存到 `data.json`

### 数据筛选
- 使用"平台筛选"下拉菜单选择特定平台
- 在"关键词搜索"框输入关键词并点击搜索

### 数据管理
- 点击"刷新"按钮重新加载数据
- 点击数据行的"删除"按钮删除单条数据

## API接口文档

### 获取所有数据
```
GET /api/data
参数：
  - platform: 平台筛选（可选）
  - keyword: 关键词搜索（可选）
```

### 获取单条数据
```
GET /api/data/<item_id>
```

### 添加数据
```
POST /api/data
Body: JSON格式数据
```

### 更新数据
```
PUT /api/data/<item_id>
Body: JSON格式数据
```

### 删除数据
```
DELETE /api/data/<item_id>
```

### 触发数据采集
```
POST /api/crawl
Body: { "platform": "平台名称" } (可选)
```

### 获取统计信息
```
GET /api/statistics
```

## 反爬虫策略

系统实现了以下反爬虫策略：

1. **User-Agent轮换**：使用多个真实浏览器的User-Agent
2. **请求延时**：在请求之间添加随机延时（1-3秒）
3. **完善请求头**：设置完整的HTTP请求头
4. **数据去重**：使用哈希算法检测重复内容
5. **异常处理**：完善的错误捕获机制

## 注意事项

1. 爬虫使用需遵守目标网站的 `robots.txt` 和服务条款
2. 建议合理设置采集频率，避免对目标网站造成压力
3. 部分平台可能需要登录或API密钥才能访问
4. 示例代码仅供学习参考，实际使用需根据具体情况调整

## 开发辅助功能

本项目支持CodeBuddy的以下辅助功能：

- ✅ 代码自动补全
- ✅ 代码生成
- ✅ 错误提示
- ✅ 语法高亮
- ✅ 智能提示

## 许可证

MIT License
