# TaskRun

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用实例和路由注册
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证相关路由（登录接口）
│   │   └── funboost.py      # Funboost路由
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # 用户相关Pydantic模型
│   ├── schemas/
│   │   └── __init__.py      # 数据库schema（预留）
│   ├── crud/
│   │   └── __init__.py      # CRUD操作（预留）
│   ├── database/
│   │   └── __init__.py      # 数据库连接配置（预留）
│   └── dependencies/
│       ├── __init__.py
│       └── auth.py          # 认证依赖（JWT验证）
├── main.py                  # 入口点，导入app.main
├── funboost_cli_user.py
├── funboost_config.py
└── nb_log_config.py
```
生成依赖

```
pip install pipreqs
# 生成仅包含项目实际依赖的requirements.txt（UTF-8编码）
pipreqs ./ --encoding=utf8 --force
```