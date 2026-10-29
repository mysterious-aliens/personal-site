# 个人主页项目说明

## 项目简介
深色科技风的个人主页，用于展示个人信息、技能栈和项目经历。
首页右侧带一个模拟终端的打字机动画，支持点击「重新执行」重播。

## 技术栈
- **Vue 3**（组合式 API，`<script setup>`）
- **Vite 6**（开发服务器 + 构建）
- 原生 CSS（`src/style.css`，未引入 UI 框架）
- 部署：GitHub Pages（`gh-pages` 分支）

## 目录结构
```
personal-site-vue/
├── index.html          # Vite 入口，只保留 #app 挂载点
├── vite.config.js      # base 设为 /personal-site/，适配 GitHub Pages 子路径
├── package.json
├── PRD.md              # 需求分析
├── TECH_DESIGN.md      # 技术设计
├── AGENTS.md           # 本文件
└── src/
    ├── main.js         # createApp + 挂载
    ├── App.vue         # 页面全部区块（导航/首页/关于/技能/项目/博客/联系）
    └── style.css       # 全局样式
```

## 常用命令
```bash
npm install      # 安装依赖
npm run dev      # 本地开发，默认 http://localhost:5173
npm run build    # 构建，产物在 dist/
npm run preview  # 预览构建产物
```

## 硬性约定
1. 组件一律用 Vue 单文件组件（`.vue`），**不允许再写纯 HTML 页面**。
2. 样式集中在 `src/style.css`，类名沿用现有的 `navbar` / `section` / `terminal` 等，不要随意改名。
3. 终端动画逻辑只能放在 `App.vue` 的 `<script setup>` 里，不要用 `document.getElementById` 直接操作 DOM。
4. 构建产物 `dist/` 不提交到 `main` 分支，部署时单独推到 `gh-pages`。
5. 新增区块时，导航栏的锚点（`#id`）要和区块 `id` 保持一致。

## 部署方式
```bash
npm run build
# 把 dist/ 推到 gh-pages 分支
```
GitHub 仓库 Settings → Pages → Source 选 `gh-pages` 分支 → 访问
`https://mysterious-aliens.github.io/personal-site/`
