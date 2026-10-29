<script setup>
import { ref, onMounted } from 'vue'

const terminalLines = ref([])
const running = ref(false)

const commands = [
  {
    cmd: 'whoami',
    output: [{ text: '陈堃 · 大连民族大学 物联网工程' }],
  },
  {
    cmd: 'cat direction.txt',
    output: [
      { text: '大模型与深度学习工程' },
      { text: '→ 从零训练过 63.91M 参数的中文预训练模型', highlight: true },
      { text: '→ 手写过 BPE 分词器，调过 Llama 3.1 的 LoRA', highlight: true },
    ],
  },
  {
    cmd: 'ls skills/',
    output: [{ text: 'Python   PyTorch   Transformers   LoRA   TypeScript   Git' }],
  },
  {
    cmd: 'git log --oneline -1',
    output: [{ text: '一切从“先把最小可用版本跑通”开始。' }],
  },
]

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function runTerminal() {
  if (running.value) return
  running.value = true
  terminalLines.value = []

  for (const item of commands) {
    terminalLines.value.push({ type: 'cmd', text: '' })
    const current = terminalLines.value.length - 1
    for (const ch of item.cmd) {
      terminalLines.value[current].text += ch
      await sleep(50)
    }
    await sleep(300)

    for (const line of item.output) {
      terminalLines.value.push({ type: 'out', ...line })
      await sleep(200)
    }
    await sleep(300)
  }

  running.value = false
}

onMounted(() => {
  runTerminal()

  // 滚动到可视区域时淡入
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('visible')
      })
    },
    { threshold: 0.15 }
  )
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el))
})
</script>

<template>
  <!-- 导航栏 -->
  <nav class="navbar">
    <div class="nav-left">
      <div class="logo">
        <span class="logo-icon">C</span>
        <span class="logo-text">chenkun</span>
      </div>
    </div>
    <div class="nav-right">
      <a href="#home" class="nav-link active">首页</a>
      <a href="#about" class="nav-link">关于</a>
      <a href="#skills" class="nav-link">技能</a>
      <a href="#projects" class="nav-link">项目</a>
      <a href="#blog" class="nav-link">博客</a>
      <a href="#contact" class="nav-link">联系</a>
    </div>
  </nav>

  <!-- 首页 -->
  <section id="home" class="main section">
    <div class="container">
      <div class="left-section">
        <div class="status-badge">
          <span class="status-dot"></span>
          辽宁·大连 · 正在学习大模型
        </div>

        <h1 class="title">
          你好，我是 <span class="gradient-text">陈堃</span>
        </h1>

        <p class="subtitle">物联网工程在读 · 大模型方向</p>

        <p class="description">$ 从零训练了 63.91M 参数的中文模型，手写过 BPE 分词器</p>

        <div class="buttons">
          <a href="#projects" class="btn-primary">看看我的项目</a>
          <a href="#contact" class="btn-secondary">联系我</a>
        </div>

        <div class="stats">
          <div class="stat-item">
            <div class="stat-num">4</div>
            <div class="stat-label">实训项目</div>
          </div>
          <div class="stat-item">
            <div class="stat-num">63.91M</div>
            <div class="stat-label">模型参数</div>
          </div>
          <div class="stat-item">
            <div class="stat-num">1.24 GB</div>
            <div class="stat-label">训练语料</div>
          </div>
        </div>

        <div class="scroll-hint"><span>↓</span> 向下滚动了解更多</div>
      </div>

      <div class="right-section">
        <div class="terminal">
          <div class="terminal-header">
            <div class="terminal-dots">
              <span class="dot red"></span>
              <span class="dot yellow"></span>
              <span class="dot green"></span>
            </div>
            <div class="terminal-title">zsh — profile — 80×24</div>
          </div>
          <div class="terminal-body">
            <template v-for="(line, i) in terminalLines" :key="i">
              <div v-if="line.type === 'cmd'" class="cmd-line">
                <span class="cmd">{{ line.text }}</span>
              </div>
              <div v-else :class="['output', line.highlight ? 'highlight' : '']">
                <span v-if="line.highlight" class="arrow">→</span>{{ line.text }}
              </div>
            </template>
            <span class="cursor"></span>
          </div>
          <div class="terminal-footer">
            <span>执行完成 · exit 0</span>
            <button class="rerun-btn" @click="runTerminal">↻ 重新执行</button>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 关于 -->
  <section id="about" class="section reveal">
    <div class="container">
      <h2 class="section-title">关于我</h2>
      <div class="about-content">
        <p>我是陈堃，大连民族大学物联网工程专业大三学生，方向是大模型与深度学习工程。</p>
        <p>喜欢从零开始造轮子，从分词器到预训练模型，都自己动手实现过一遍，喜欢把原理搞懂再写代码。</p>
        <p>目前在做课程设计项目，学习 Web 开发、Git 部署、AI 辅助开发等技术。</p>
      </div>
    </div>
  </section>

  <!-- 技能 -->
  <section id="skills" class="section reveal">
    <div class="container">
      <h2 class="section-title">技能栈</h2>
      <div class="skills-grid">
        <div class="skill-category">
          <h3>编程语言</h3>
          <div class="skill-tags">
            <span class="tag">Python</span>
            <span class="tag">C语言</span>
            <span class="tag">Java</span>
            <span class="tag">JavaScript</span>
          </div>
        </div>
        <div class="skill-category">
          <h3>AI / 深度学习</h3>
          <div class="skill-tags">
            <span class="tag">PyTorch</span>
            <span class="tag">Transformers</span>
            <span class="tag">LoRA</span>
            <span class="tag">BPE分词器</span>
          </div>
        </div>
        <div class="skill-category">
          <h3>开发工具</h3>
          <div class="skill-tags">
            <span class="tag">Git</span>
            <span class="tag">GitHub</span>
            <span class="tag">VS Code</span>
            <span class="tag">Cursor</span>
          </div>
        </div>
        <div class="skill-category">
          <h3>其他</h3>
          <div class="skill-tags">
            <span class="tag">HTML/CSS</span>
            <span class="tag">MySQL</span>
            <span class="tag">51单片机</span>
            <span class="tag">Proteus</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 项目 -->
  <section id="projects" class="section reveal">
    <div class="container">
      <h2 class="section-title">实训项目</h2>
      <div class="projects-grid">
        <div class="project-card">
          <h3>MiniMind 大模型预训练</h3>
          <p>从零实现 63.91M 参数的中文预训练模型，包括 BPE 分词器、Transformer 架构、预训练流程。</p>
          <div class="project-tags">
            <span class="tag">PyTorch</span>
            <span class="tag">Transformer</span>
          </div>
        </div>
        <div class="project-card">
          <h3>SFT 微调作业</h3>
          <p>在魔搭云端进行 SFT 微调，使用 LoRA 技术微调大模型。</p>
          <div class="project-tags">
            <span class="tag">LoRA</span>
            <span class="tag">Transformers</span>
          </div>
        </div>
        <div class="project-card">
          <h3>电商图片下载插件</h3>
          <p>Chrome 扩展插件，使用 Cursor 开发，GitHub Pages 部署。</p>
          <div class="project-tags">
            <span class="tag">JavaScript</span>
            <span class="tag">Chrome扩展</span>
          </div>
        </div>
        <div class="project-card">
          <h3>个人主页网站</h3>
          <p>深色科技风个人主页，Vue 3 + Vite 构建，带终端打字机动画，GitHub Pages 部署。</p>
          <div class="project-tags">
            <span class="tag">Vue 3</span>
            <span class="tag">Vite</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 博客 -->
  <section id="blog" class="section reveal">
    <div class="container">
      <h2 class="section-title">博客</h2>
      <div class="blog-list">
        <div class="blog-item">
          <h3>从零实现一个 BPE 分词器</h3>
          <p>记录手写 BPE 分词器的过程，理解分词原理。</p>
        </div>
        <div class="blog-item">
          <h3>大模型预训练流程记录</h3>
          <p>从数据准备到模型训练的完整流程。</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 联系 -->
  <section id="contact" class="section reveal">
    <div class="container">
      <h2 class="section-title">联系我</h2>
      <div class="contact-content">
        <p>邮箱：3465473990@qq.com</p>
        <p>GitHub：github.com/mysterious-aliens</p>
        <p>欢迎交流学习！</p>
      </div>
    </div>
  </section>
</template>
