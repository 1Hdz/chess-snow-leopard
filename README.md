# chess-snow-leopard

基于 **Django 5.2** 的个人学习项目，从零搭建，用于系统练习 Django 后端开发的基础流程：URL 路由、视图函数、请求对象、模板语法、静态资源、ORM 增删改查、表单提交与第三方 API 调用。

> 本仓库最初创建自 GitHub 的 "Introduction to GitHub" 练习（原 README 为 `Exercise: Introduction to GitHub`），随后作为 Django 学习代码上传，仓库名沿用至今。

---

## 一、技术栈

| 分类 | 技术 | 用途 |
| --- | --- | --- |
| 后端框架 | Django 5.2.17 | Web 应用框架 |
| 数据库 | MySQL（5.7+ / 8.x） | 业务数据存储，库名 `mysite2` |
| 数据库驱动 | PyMySQL 1.2.3 | 通过 `install_as_MySQLdb()` 连接 MySQL |
| HTTP 客户端 | requests 2.34.x | 调用 open-meteo 天气接口 |
| 前端框架 | Bootstrap 3.4.1 | 页面样式（本地静态资源） |
| 前端脚本 | jQuery 3.6.0 | JS 库（本地静态资源） |

---

## 二、功能模块

### 1. 基础演示

- **首页 `/index/`**：最简单的视图，返回 `"Hello, world."`
- **request 对象 `/something/`**：演示如何获取请求方式（`GET`/`POST`）、URL 查询参数（`request.GET`）、请求体（`request.POST`），以及三种响应方式（`HttpResponse` / `render` / `redirect`）

### 2. 模板与静态资源

- **模板语法 `/tpl/`**：演示 Django 模板的变量输出（`{{ }}`）、列表/字典取值、`for` 循环渲染
- **用户列表页 `/user/list/`**：演示本地静态资源的引入方式（`{% static %}`），包含 Bootstrap CSS、jQuery 与本地图片

### 3. 登录功能

- **用户登录 `/login/`**：`GET` 请求展示登录表单，`POST` 请求校验用户名密码；账号 `root`、密码 `123` 校验通过后重定向，否则回显错误提示（模板上下文传递）

### 4. 天气接口调用

- **成都实时天气 `/weather/`**：通过 `requests` 请求 [open-meteo](https://open-meteo.com/) 免费 API（经纬度 30.67, 104.07），获取当前温度、海拔、时区等信息并在页面渲染

### 5. ORM 与用户信息管理（核心案例）

基于 `UserInfo` 模型的完整增删改查：

- **ORM 演示 `/orm/`**：批量更新（`objects.all().update()`）、条件更新（`objects.filter().update()`）
- **信息列表 `/info/list/`**：`objects.all()` 读取全部记录并渲染到表格，带删除操作入口
- **添加用户 `/info/add/`**：表单提交（含 CSRF 防护），`objects.create()` 写入数据库后重定向回列表页
- **删除用户 `/info/delete/`**：按 `nid`（GET 参数）执行 `objects.filter(id=nid).delete()` 后重定向

---

## 三、路由一览

| 路由 | 方法 | 功能 | 对应视图 |
| --- | --- | --- | --- |
| `/index/` | GET | 首页（Hello, world） | `views.index` |
| `/user/list/` | GET | 用户列表页（静态资源演示） | `views.user_list` |
| `/user/add/` | GET | 添加用户页 | `views.user_add` |
| `/tpl/` | GET | 模板语法演示 | `views.tpl` |
| `/weather/` | GET | 成都实时天气 | `views.weather` |
| `/something/` | GET | request 对象演示 | `views.something` |
| `/login/` | GET/POST | 用户登录 | `views.login` |
| `/orm/` | GET | ORM 更新演示 | `views.orm` |
| `/info/list/` | GET | 用户信息列表 | `views.info_list` |
| `/info/add/` | GET/POST | 添加用户 | `views.info_add` |
| `/info/delete/` | GET | 删除用户 | `views.info_delete` |

---

## 四、数据模型

当前模型定义于 `app01/models.py`：

```python
class UserInfo(models.Model):
    name = models.CharField(max_length=32)      # 姓名
    password = models.CharField(max_length=64)  # 密码
    age = models.IntegerField(default=2)        # 年龄

class Department(models.Model):
    title = models.CharField(max_length=16)     # 部门名称
```

### 迁移历史（migrations）

| 迁移文件 | 说明 |
| --- | --- |
| `0001_initial` | 创建 `User` 表（name / password(66) / age） |
| `0002_department_role...` | 新增 `Department`、`Role` 表；`age` 加默认值 2，`password` 改为 64 |
| `0003_delete_role` | 删除 `Role` 表 |
| `0004_rename_user_userinfo` | `User` 重命名为 `UserInfo` |
| `0005_rename_userinfo_user` | `UserInfo` 重命名回 `User` |
| `0006_rename_user_userinfo` | `User` 最终重命名为 `UserInfo`（当前状态） |

当前库中实际表：`app01_userinfo`、`app01_department`。

---

## 五、项目结构

```
mysite/
├── manage.py                  # Django 管理入口（迁移 / 启动 / 创建应用等）
├── mysite/                    # 项目配置目录
│   ├── settings.py            # 全局配置（数据库、应用注册、模板、静态文件）
│   ├── urls.py                # 全局 URL 路由
│   ├── __init__.py            # 引入 PyMySQL 并安装为 MySQLdb
│   ├── asgi.py                # ASGI 服务器入口
│   ├── wsgi.py                # WSGI 服务器入口
│   └── db.sqlite3             # 占位文件（已切换 MySQL，未实际使用）
└── app01/                     # 业务应用
    ├── views.py               # 全部视图函数
    ├── models.py              # 数据模型
    ├── admin.py               # 后台管理注册（当前未使用）
    ├── apps.py                # 应用配置类 App01Config
    ├── tests.py               # 测试文件
    ├── migrations/            # 数据库迁移文件（0001 ~ 0006）
    ├── templates/             # HTML 模板
    │   ├── index 相关：user_list.html / user_add.html
    │   ├── 演示类：tpl.html / weather.html / login.html
    │   └── 管理类：info_list.html / info_add.html
    └── static/                # 静态资源
        ├── css/               # 自定义样式目录
        ├── js/                # jquery-3.6.0.min.js
        ├── img/               # 1.png（页面示例图）
        └── plugins/
            └── bootstrap-3.4.1/   # Bootstrap 3.4.1 全套资源
```

---

## 六、环境准备

### 1. 环境要求

- Python 3.10+（项目在 Python 3.10 环境开发，Django 5.2 要求 Python 3.10 及以上）
- 本地 MySQL 服务（或可访问的远程 MySQL）

### 2. 安装依赖

```bash
pip install django==5.2.17 pymysql requests
```

> 建议使用虚拟环境（`python -m venv venv` 后激活），避免污染全局环境。

### 3. 配置数据库

项目默认连接 MySQL，配置位于 `mysite/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite2',        # 数据库名
        'USER': 'root',           # 用户名
        'PASSWORD': '123456',     # 密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

先登录 MySQL 创建数据库：

```sql
CREATE DATABASE mysite2 DEFAULT CHARACTER SET utf8mb4;
```

> 如当前环境无 MySQL，可恢复 `settings.py` 中被注释的 SQLite 配置：
>
> ```python
> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.sqlite3',
>         'NAME': BASE_DIR / 'db.sqlite3',
>     }
> }
> ```

### 4. 执行迁移

```bash
python manage.py migrate
```

### 5. 启动服务

```bash
python manage.py runserver
```

浏览器访问 <http://127.0.0.1:8000/index/>。

---

## 七、功能体验指引

| 页面 | 访问地址 | 操作说明 |
| --- | --- | --- |
| 首页 | <http://127.0.0.1:8000/index/> | 直接返回文本 |
| 用户列表 | <http://127.0.0.1:8000/user/list/> | 查看静态资源加载效果 |
| 模板演示 | <http://127.0.0.1:8000/tpl/> | 查看变量 / 循环渲染结果 |
| 天气 | <http://127.0.0.1:8000/weather/> | 需能访问外网 |
| 登录 | <http://127.0.0.1:8000/login/> | 账号 `root` / 密码 `123` |
| 信息管理 | <http://127.0.0.1:8000/info/list/> | 列表 → 添加 → 删除，完整 CRUD 流程 |

---

## 八、常见问题排查

| 现象 | 原因与解决 |
| --- | --- |
| `ModuleNotFoundError: No module named 'pymysql'` | 未安装依赖，执行 `pip install pymysql` |
| `django.db.utils.OperationalError: (1045...)` | MySQL 账号密码错误，检查 `settings.py` 中 `USER` / `PASSWORD` |
| `(2003...) Can't connect to MySQL server` | MySQL 服务未启动，或 `HOST` / `PORT` 配置错误 |
| `(1049...) Unknown database 'mysite2'` | 数据库未创建，先执行 `CREATE DATABASE mysite2 ...` |
| `ModuleNotFoundError: No module named 'requests'` | 未安装依赖，执行 `pip install requests`（仅 `/weather/` 页面需要） |
| `Error: That port is already in use` | 8000 端口被占用，换端口启动：`python manage.py runserver 8001` |
| 迁移报字段错误 | 模型与迁移历史不一致时，可核对 `app01/migrations` 下 0001~0006 顺序 |

---

## 九、开发记录

项目 Git 提交脉络（节选）：

```
f060d2c 删除旧的测试txt文件
e53ebaf Merge branch 'main' of https://github.com/1Hdz/chess-snow-leopard
9bd2185 上传Django项目mysite+app01
b6c332e yici
aa4d362 Merge branch 'main' of github.com:1Hdz/chess-snow-leopard
7a49a92 first commit
a90a6d9 add file 2.txt
38f39b4 first commit
2c84c0d Initial commit
```

远程仓库：`https://github.com/1Hdz/chess-snow-leopard.git`（remote 别名 `gittest`）

---

## 十、备注

- 静态资源已全部本地化（Bootstrap 3.4.1、jQuery 3.6.0），页面样式无需联网。
- `/weather/` 页面依赖外网访问 open-meteo API；若请求失败页面会提示"数据加载失败"。
- `SECRET_KEY` 为开发环境默认值，**部署生产环境前必须更换**，并设置 `DEBUG = False`、`ALLOWED_HOSTS`。
- `db.sqlite3` 为占位文件（0 字节），已加入 `.gitignore`，不影响使用。
- `.gitignore` 已忽略：`__pycache__/`、`*.pyc`、`.idea/`、`.vscode/`、`venv/`、`*.log` 及练习文件夹。
