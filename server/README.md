# 个人主页后端

Flask + SQLite，提供内容读取与管理端保存。

## 启动

```bash
pip install flask flask-cors
python server/app.py
```

默认监听 `http://127.0.0.1:5001`，首次启动会自动建表并写入默认内容。

管理账号：`admin / chenkun2026`
可通过环境变量覆盖：

```bash
set SITE_ADMIN_USER=admin
set SITE_ADMIN_PASSWORD=你的密码
set SITE_SECRET=随机字符串
```

## 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/health` | 健康检查 |
| GET | `/api/content` | 读取整站内容（公开） |
| POST | `/api/login` | 登录，返回 token |
| PUT | `/api/content` | 保存内容（需 `Authorization: Bearer <token>`） |
| POST | `/api/content/reset` | 恢复默认内容（需 token） |

登录示例：

```bash
curl -X POST http://127.0.0.1:5001/api/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"chenkun2026\"}"
```

## 数据

内容存 `server/site.db` 的 `content` 表，字段：

- `id`：固定 1
- `data`：整站 JSON 字符串
- `updated_at`：最后修改时间戳

## 前端对接

前端通过 `src/api.js` 调用，默认地址 `http://127.0.0.1:5001/api`。
部署到别的机器时，构建前设置：

```bash
set VITE_API_BASE=https://你的后端域名/api
npm run build
```

后端不可用时，前端自动回退到 `src/defaults.js` 的静态内容。
