# 京迹 - 北京历史文化景点推荐系统

## 项目简介
京迹（RecoTravel）是一个基于Django开发的北京历史文化景点推荐系统，旨在为用户提供个性化的旅游路线规划和景点推荐服务。

## 功能特点
1. 用户系统
   - 用户注册（用户名仅限英文且不超过6个字符，支持邮箱注册）
   - 用户登录、注销，安全管理
   - 登录后显示用户信息，下拉菜单支持退出

2. 博客与互动
   - 支持发帖，帖子可上传封面图片，内容支持富文本
   - 作者可删除自己的帖子
   - 支持对帖子评论，评论仅限本人删除

3. 图片上传与展示
   - 发帖时必须上传封面图片，所有图片在博客和详情页美观展示

4. AI 北京旅游助手
   - 集成大模型接口，智能解答北京旅游相关问题
   - 提供路线、景点、美食、交通、历史文化等建议

5. 景点智能推荐
   - 用户输入关键词，AI推荐最匹配的北京景点
   - 支持个性化推荐

6. 旅游路线规划
   - 用户选择感兴趣景点，系统自动生成最优旅游路线
   - 结合高德地图API获取真实路线信息

7. 响应式美观前端界面
   - 采用Bootstrap和自定义样式，适配PC和移动端，界面现代美观

8. 安全与体验优化
   - 表单校验、权限控制、错误提示、操作反馈等细节完善，提升整体用户体验

## 技术栈
- 后端：Django
- 数据库：SQLite
- 前端：HTML, CSS, JavaScript, Bootstrap
- 其他：jQuery, Font Awesome

## 安装说明
1. 克隆项目
```bash
git clone https://github.com/chenjiawei30/RecoTravel.git
cd RecoTravel
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库（SQLite）并修改 settings.py 中的数据库连接信息
```bash
cp .env.example .env
# 编辑 .env 文件，设置 OPENAI_API_KEY=你的API密钥
```

5. 运行数据库迁移
```bash
python manage.py migrate
```

6. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

7. 运行开发服务器
```bash
python manage.py runserver
```

## 使用说明
1. 用户注册
   - 填写用户名、邮箱和密码
   - 点击注册按钮完成注册

2. 用户登录
   - 输入用户名和密码
   - 点击登录按钮完成登录

3. 景点推荐
   - 在首页浏览推荐景点
   - 点击景点查看详细信息
   - 选择感兴趣的景点进行路线规划

4. 路线规划
   - 选择想要游览的景点
   - 系统自动生成推荐路线
   - 查看路线详情和景点信息

## 项目结构
```
RecoTravel/
├── mydjango/          # Django项目配置
├── templates/         # HTML模板
├── static/            # 静态文件
├── staticfiles/       # 收集的静态文件
├── manage.py          # Django管理脚本
└── requirements.txt   # 项目依赖
```

北京市旅游路线推荐系统项目

* **编程语言**：Python
* **网站框架**：Django
* **旅游路线来源**：高德地图API


## 一、项目背景

随着旅游行业的迅猛发展以及城市化进程的加快，北京作为中国的首都和世界著名的旅游城市，每年吸引大量国内外游客。北京拥有丰富的旅游资源，包括文化古迹、现代景观与自然风光。

然而，随着旅游信息的不断增加，游客在选择景点和规划旅游路线时常常面临如下问题：

* 信息过载
* 个性化推荐不足
* 旅游体验优化困难

本项目旨在利用Web技术和AI大模型，设计一个高效且个性化的北京旅游推荐系统。


## 二、项目目标

本系统基于 Django 框架和 SQLite 数据库，结合大模型API，实现以下核心功能：

* 用户注册、登录、注销，权限管理
* 博客发帖、图片上传、评论互动
* AI助手智能问答与景点推荐
* 旅游路线智能规划
* 响应式美观前端界面


## 三、项目环境

| 项目组件  | 配置说明                       |
| ----- | -------------------------- |
| 操作系统  | Ubuntu 22.04               |
| 网站框架  | Django 2.1.2               |
| 数据库     | SQLite                        |
| 编程语言  | Python 3.10                 |
| 依赖库   | requests、django、pillow等 |


## 四、系统架构设计

### 1. 数据准备与预处理

* **数据来源**：部分景点数据爬取自公开旅游平台，部分由管理员手动整理
* **数据格式**：JSON格式，包含景点名称、地址、图片等信息
* **数据文件**：
  * `static/spots.json`  # 景点信息数据

### 2. Django Web 系统功能

* 用户注册、登录、注销，权限管理
* 博客发帖、图片上传、评论互动
* AI助手智能问答与景点推荐
* 旅游路线智能规划
* 前端页面美观、响应式


## 五、目录结构

```
RecoTravel/
├── mydjango/
│   ├── settings.py
│   ├── urls.py
│   ├── view.py
│   └── sam/
├── templates/
├── static/
├── manage.py
└── db.sqlite3
```


## 六、实验总结

### 系统优势

* Django 提供稳定、易用的 Web 展示框架
* SQLite 数据库高效存储用户、帖子、评论等信息
* 集成大模型API，智能推荐与问答体验佳
* 前端界面美观，用户体验良好

### 当前问题

* 推荐效果受限于大模型API的准确性和数据覆盖度
* 需持续优化前端交互和界面细节

### 优化方向

* 增强AI推荐的个性化和多样性
* 丰富景点数据和用户行为数据
* 打造更直观友好的前端展示界面

## 项目功能

- **用户注册、登录、注销**：支持用户名和邮箱注册，注册时用户名仅限英文且不超过6个字符，保障账户安全。
- **个人信息与权限管理**：登录后可查看个人信息，支持下拉菜单显示用户状态，未登录用户部分功能受限。
- **博客发帖与管理**：用户可发布新帖子，支持上传封面图片，帖子内容支持富文本，作者可删除自己的帖子。
- **评论互动**：支持对每个帖子进行评论，评论可删除，仅限评论作者本人操作，提升社区互动体验。
- **图片上传与展示**：发帖时必须上传封面图片，所有图片均可在博客和详情页美观展示。
- **AI 北京旅游助手**：集成大模型接口，智能解答北京旅游相关问题，提供路线、景点、美食、交通等建议。
- **景点智能推荐**：根据用户输入关键词，AI推荐最匹配的北京景点，支持个性化推荐。
- **旅游路线规划**：用户可选择感兴趣的景点，系统自动生成最优旅游路线，结合高德地图API获取真实路线信息。
- **响应式美观前端界面**：采用Bootstrap和自定义样式，适配PC和移动端，界面现代美观。
- **安全与体验优化**：表单校验、权限控制、错误提示、操作反馈等细节完善，提升整体用户体验。
