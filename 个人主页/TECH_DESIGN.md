# 个人主页 技术设计文档

## 一、技术栈选型

### 1.1 选型结论
| 层 | 选型 | 理由 |
|----|------|------|
| 前端 | 原生 HTML + CSS + JavaScript | 纯静态页面，不需要框架 |
| 样式 | CSS3 + Flexbox | 简单布局，不需要预处理器 |
| 动画 | CSS Animation + JS | 终端打字机动画效果 |
| 部署 | GitHub Pages | 免费静态托管 |

---

## 二、页面结构

### 2.1 整体布局
```
┌─────────────────────────────────────────┐
│  Logo          首页 关于 技能 项目 联系  │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐    ┌─────────────────┐ │
│  │  个人简介    │    │   终端窗口       │ │
│  │  你好，我是  │    │   whoami...     │ │
│  │  陈堃        │    │   cat direction │ │
│  │  专业介绍    │    │   ls skills/    │ │
│  │  技能列表    │    │   git log       │ │
│  │  按钮        │    │                 │ │
│  └─────────────┘    └─────────────────┘ │
│                                         │
│  4个项目  63.91M参数  1.24GB语料        │
└─────────────────────────────────────────┘
```

### 2.2 模块划分
1. **导航栏模块**：顶部导航，支持切换页面
2. **个人简介模块**：左侧展示姓名、专业、方向
3. **终端动画模块**：右侧终端窗口，自动播放命令动画
4. **统计数据模块**：底部展示项目数、模型参数、语料大小

---

## 三、核心技术实现

### 3.1 星空背景
用 CSS 渐变 + 多个 radial-gradient 做点状星空效果，不需要图片。

```css
body {
  background: #0a0a1a;
  background-image: 
    radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
    radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
    radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px);
  background-size: 550px 550px, 350px 350px, 250px 250px;
}
```

### 3.2 终端打字机动画
用 JS 控制逐字输出命令和结果，模拟真实终端效果。

```javascript
const commands = [
  { cmd: 'whoami', output: '陈堃 · 大连民族大学 物联网工程' },
  { cmd: 'cat direction.txt', output: '大模型与深度学习工程' },
  { cmd: 'ls skills/', output: 'Python PyTorch Transformers LoRA TypeScript Git' },
  { cmd: 'git log --oneline -1', output: '一切从"先把最小可用版本跑通"开始。' }
];
```

### 3.3 响应式布局
用 Flexbox 布局，手机端自动上下排列。

---

## 四、目录结构

```
个人主页/
├── index.html          # 主页面
├── style.css           # 样式文件
├── app.js              # 主逻辑
├── PRD.md              # 需求文档
├── TECH_DESIGN.md      # 技术设计文档
└── AGENTS.md           # 项目说明
```
