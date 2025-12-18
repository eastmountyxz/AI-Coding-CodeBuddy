# 图书管理系统

这是一个使用 Django 3.2 开发的图书管理系统示例网站。

## 项目结构

```
library_site/
├── manage.py                    # Django 管理脚本
├── library_site/                # 项目配置目录
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # 项目设置文件
│   ├── urls.py                 # 主 URL 配置
│   └── wsgi.py
├── library/                     # 应用目录
│   ├── __init__.py
│   ├── admin.py                # 管理后台配置
│   ├── apps.py                 # 应用配置
│   ├── models.py               # 数据模型（保留接口）
│   ├── views.py                # 视图函数
│   ├── urls.py                 # 应用 URL 配置
│   ├── tests.py                # 测试文件
│   ├── migrations/             # 数据库迁移文件
│   │   └── __init__.py
│   ├── templates/              # 模板目录
│   │   └── library/
│   │       ├── base.html       # 基础模板
│   │       ├── login.html      # 登录页面
│   │       └── home.html       # 主页面
│   └── static/                 # 静态文件目录
│       └── library/
│           ├── css/            # CSS 文件
│           └── images/         # 图片文件
│               ├── book1.jpg
│               ├── book2.jpg
│               ├── book3.jpg
│               ├── book4.jpg
│               ├── book5.jpg
│               └── book6.jpg
└── db.sqlite3                  # SQLite 数据库文件
```

## 功能说明

1. **登录系统**
   - 用户名和密码表单
   - 硬编码账户验证（admin/123456）
   - 登录成功后跳转主界面
   - 登录失败给出错误提示

2. **图书展示**
   - 主界面展示图书列表
   - 每本书包含：书名、作者、分类、简介
   - 图书封面图片展示（使用占位图片）
   - 响应式卡片布局

3. **系统设计**
   - 使用 base.html 作为母板模板
   - 统一的页头、导航和页脚
   - 使用 Bootstrap 5 美化界面
   - 保留 SQLite 默认配置但暂不编写实际数据库操作

## 使用方法

1. **安装依赖**
   ```
   pip install django==3.2.25
   ```

2. **数据库迁移**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **启动开发服务器**
   ```
   python manage.py runserver
   ```

4. **访问网站**
   - 打开浏览器访问 http://127.0.0.1:8000/
   - 使用测试账户登录：用户名 admin，密码 123456

## 技术特点

1. **视图传值**
   - 在 views.py 中定义硬编码的图书数据
   - 通过 context 字典传递数据到模板
   - 在模板中使用循环展示图书信息

2. **静态文件处理**
   - 配置了静态文件目录
   - 图书封面图片路径通过 static 标签引用
   - 图片加载失败时自动使用备用图片

3. **会话管理**
   - 使用 Django 的 session 实现登录状态保持
   - 登出时清除会话数据

4. **响应式设计**
   - 使用 Bootstrap 5 实现响应式布局
   - 适配不同屏幕尺寸的设备

## 注意事项

- 本示例保留了 SQLite 配置，但未实际使用数据库
- 图书数据为硬编码，存储在 views.py 中的 BOOKS_DATA 列表
- 图片文件为空占位文件，模板中设置了图片加载失败时的备用方案