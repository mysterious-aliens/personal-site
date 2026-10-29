# 技术设计文档 · 个人主页

## 1. 背景与目标
把已有的纯 HTML 个人主页重构成工程化前端项目，满足课程要求：
- 不能是纯 HTML/CSS/JS 静态页
- 需要组件化、构建流程和可维护的目录结构
- 仍然部署在 GitHub Pages，保持原域名可访问

## 2. 技术选型

| 维度 | 选择 | 理由 |
|---|---|---|
| 框架 | Vue 3（组合式 API） | 上手快、单文件组件结构清晰；与课程里另一个 AI 聊天系统保持一致 |
| 构建工具 | Vite 6 | 冷启动快、配置少，`base` 一行就能适配 GitHub Pages 子路径 |
| 样式 | 原生 CSS | 页面规模小，引入 Tailwind/Element Plus 反而增加体积 |
| 状态管理 | 不需要 | 页面无跨组件状态，`ref` 足够 |
| 路由 | 不需要 | 单页锚点滚动，用 `<a href="#id">` 即可 |
| 部署 | GitHub Pages（gh-pages 分支） | 免费、和现有仓库绑定 |

## 3. 结构设计

```
index.html            # 只留 <div id="app">，由 Vite 注入 bundle
src/main.js           # createApp(App).mount('#app')
src/App.vue           # 页面结构 + 终端动画逻辑
src/style.css         # 全局样式（原 style.css 迁移而来）
```

### 3.1 App.vue
一个组件承载全部区块（导航、首页、关于、技能、项目、博客、联系），
因为区块之间没有复用和独立状态，拆成 7 个组件收益不大。
如果后续要加路由，再按区块拆分。

### 3.2 终端动画
原实现用 `document.getElementById` + 手动 `createElement`。
重构后改为数据驱动：

- `terminalLines: ref([])` 保存当前已输出的行
- `runTerminal()` 按命令逐字符 `push`，用 `await sleep()` 控制节奏
- 模板用 `v-for` 渲染，`highlight` 行加 `arrow` 前缀
- `running` 标志防止重复点击叠加动画

好处：不再直接操作 DOM，逻辑和视图解耦，动画状态可测试。

## 4. 构建与部署

`vite.config.js` 里设置 `base: '/personal-site/'`，
因为 GitHub Pages 项目站点地址是 `https://<user>.github.io/personal-site/`，
资源路径必须带这个前缀，否则 JS/CSS 会 404。

部署流程：
1. `npm run build` 生成 `dist/`
2. 把 `dist/` 内容推到 `gh-pages` 分支
3. 仓库 Settings → Pages → Source 选择 `gh-pages` 分支
4. 访问 `https://mysterious-aliens.github.io/personal-site/`

## 5. 风险与取舍
- **哈希路由 vs 锚点**：单页锚点足够，不引入 vue-router，减少依赖。
- **样式迁移**：原 `style.css` 直接复用，避免视觉回归；类名保持不变。
- **部署分支**：`main` 只放源码，`gh-pages` 只放构建产物，避免仓库里混入 `dist`。
