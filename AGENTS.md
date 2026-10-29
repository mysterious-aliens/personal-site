# 个人主页项目说明

## 项目简介
深色科技风的个人主页，用于展示个人信息、技能栈和项目经历。
首页右侧带一个模拟终端的打字机动画，支持点击「重新执行」重播。
**内容由后端接口实时读取**，管理员登录后台修改后，前台刷新即可生效，无需重新构建。

## 技术栈
- 前端：**Vue 3**（组合式 API）+ **Vite 6** + 原生 CSS
- 后端：**Flask** + SQLite（内容存一张 `content` 表）
- 部署：前端 GitHub Pages（`gh-pages` 分支），后端本地 / 任意 Python 托管平台

## 目录结构
```
├── index.html              # Vite 入口
├── vite.config.js          # base = /personal-site/
├── package.json
├── PRD.md                  # 需求分析
├── TECH_DESIGN.md          # 技术设计
├── AGENTS.md               # 本文件
├── server/
│   ├── app.py              # Flask 后端：读取 / 登录 / 保存 / 恢复默认
│   ├── site.db             # SQLite 数据库（首次启动自动生成）
│   └── README.md           # 后端启动与接口说明
└── src/
    ├── main.js             # 按 hash 挂载 App 或 Admin
    ├── App.vue             # 前台页面（数据来自 /api/content）
    ├── Admin.vue           # 管理端：登录 + 表单编辑
    ├── api.js              # 接口封装
    ├── defaults.js         # 后端不可用时的兜底内容
    └── style.css           # 全局样式
```

## 常用命令
```bash
# 前端
npm install
npm run dev        # http://localhost:5173
npm run build      # 产物在 dist/

# 后端
pip install flask flask-cors
python server/app.py   # http://127.0.0.1:5001
```

管理端入口：`http://localhost:5173/#admin`
默认账号：`admin / chenkun2026`（可通过环境变量 `SITE_ADMIN_USER`、`SITE_ADMIN_PASSWORD` 修改）

## 硬性约定
1. 组件一律用 Vue 单文件组件，**不允许再写纯 HTML 页面**。
2. 前台展示的数据全部来自 `content`，不要在组件里写死文案。
3. 后端接口统一返回 `{ ok, data | error }`，前端只通过 `src/api.js` 调用。
4. 管理员密码用 PBKDF2 存哈希，不存明文；token 用 HMAC 生成，按小时过期。
5. 后端不可用时前端必须能回退到 `defaults.js`，保证静态站点可访问。
6. 构建产物 `dist/` 不提交到 `main`，部署时单独推到 `gh-pages`。

## 部署方式
前端：
```bash
npm run build
# 把 dist/ 推到 gh-pages 分支，Pages 源选 gh-pages
```
后端：需要一台能跑 Python 的机器（本地 / Render / Railway / 云服务器均可），
启动后把前端 `VITE_API_BASE` 指向它的 `/api` 地址再重新构建即可。
