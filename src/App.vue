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
      { text: '从零训练过 63.91M 参数的中文预训练模型', highlight: true },
      { text: '手写过 BPE 分词器，调过 Llama 3.1 的 LoRA', highlight: true },
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
      await sleep(45)
    }
    await sleep(260)

    for (const line of item.output) {
      terminalLines.value.push({ type: 'out', ...line })
      await sleep(170)
    }
    await sleep(260)
  }

  running.value = false
}

onMounted(() => {
  runTerminal()

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('visible')
      })
    },
    { threshold: 0.12 }
  )
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el))
})
</script>

<template>
  <!-- 导航 -->
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

  <!-- 首屏 -->
  <section id="home" class="hero">
    <div class="hero-glow"></div>
    <div class="container hero-grid">
      <div class="hero-copy">
        <div class="status-badge">
          <span class="status-dot"></span>
          辽宁 · 大连　正在学习大模型
        </div>

        <h1 class="title">
          你好，我是<br />
          <span class="gradient-text">陈堃</span>
        </h1>

        <p class="subtitle">物联网工程在读 · 大模型与深度学习方向</p>
        <p class="description">
          <span class="prompt">$</span> 从零训练 63.91M 参数中文模型，手写 BPE 分词器
        </p>

        <div class="buttons">
          <a href="#projects" class="btn-primary">看看我的项目</a>
          <a href="#contact" class="btn-secondary">联系我</a>
        </div>

        <div class="stats">
          <div class="stat-item">
            <div class="stat-num">04</div>
            <div class="stat-label">实训项目</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-num">63.91M</div>
            <div class="stat-label">模型参数</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-num">1.24GB</div>
            <div class="stat-label">训练语料</div>
          </div>
        </div>
      </div>

      <div class="hero-terminal">
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
                <span v-if="line.highlight" class="arrow">↳</span>{{ line.text }}
              </div>
            </template>
            <span class="cursor"></span>
          </div>
          <div class="terminal-footer">
            <span class="exit">exit 0</span>
            <button class="rerun-btn" @click="runTerminal">↻ 重新执行</button>
          </div>
        </div>
      </div>
    </div>

    <div class="scroll-hint"><span>↓</span></div>
  </section>

  <!-- 关于 -->
  <section id="about" class="section reveal">
    <div class="container">
      <div class="section-head">
        <span class="section-label">01 / ABOUT</span>
        <h2 class="section-title">关于我</h2>
      </div>

      <div class="about-card">
        <div class="avatar">
          <span>陈</span>
        </div>
        <div class="about-text">
          <p>我是陈堃，大连民族大学物联网工程专业大三学生，方向是大模型与深度学习工程。</p>
          <p>喜欢从零开始造轮子，从分词器到预训练模型都自己动手实现过一遍，喜欢把原理搞懂再写代码。</p>
          <p>目前在做课程设计项目，学习 Web 开发、Git 部署、AI 辅助开发等技术。</p>
          <div class="about-meta">
            <span class="meta-item">📍 辽宁 · 大连</span>
            <span class="meta-item">🎓 大连民族大学</span>
            <span class="meta-item">💡 大模型工程</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 技能 -->
  <section id="skills" class="section reveal">
    <div class="container">
      <div class="section-head">
        <span class="section-label">02 / SKILLS</span>
        <h2 class="section-title">技能栈</h2>
      </div>

      <div class="skills-grid">
        <div class="skill-category">
          <div class="skill-icon">💻</div>
          <h3>编程语言</h3>
          <p class="skill-desc">日常写代码的主力语言</p>
          <div class="skill-tags">
            <span class="tag">Python</span>
            <span class="tag">C语言</span>
            <span class="tag">Java</span>
            <span class="tag">JavaScript</span>
          </div>
        </div>

        <div class="skill-category">
          <div class="skill-icon">🧠</div>
          <h3>AI / 深度学习</h3>
          <p class="skill-desc">从训练到微调的完整链路</p>
          <div class="skill-tags">
            <span class="tag">PyTorch</span>
            <span class="tag">Transformers</span>
            <span class="tag">LoRA</span>
            <span class="tag">BPE 分词器</span>
          </div>
        </div>

        <div class="skill-category">
          <div class="skill-icon">🛠️</div>
          <h3>开发工具</h3>
          <p class="skill-desc">版本管理与 AI 辅助开发</p>
          <div class="skill-tags">
            <span class="tag">Git</span>
            <span class="tag">GitHub</span>
            <span class="tag">VS Code</span>
            <span class="tag">Cursor</span>
          </div>
        </div>

        <div class="skill-category">
          <div class="skill-icon">✨</div>
          <h3>其他</h3>
          <p class="skill-desc">课程里接触过的技术</p>
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
      <div class="section-head">
        <span class="section-label">03 / PROJECTS</span>
        <h2 class="section-title">实训项目</h2>
      </div>

      <div class="projects-grid">
        <article class="project-card">
          <span class="project-index">01</span>
          <h3>MiniMind 大模型预训练</h3>
          <p>从零实现 63.91M 参数的中文预训练模型，包括 BPE 分词器、Transformer 架构与训练流程。</p>
          <div class="project-tags">
            <span class="tag">PyTorch</span>
            <span class="tag">Transformer</span>
          </div>
        </article>

        <article class="project-card">
          <span class="project-index">02</span>
          <h3>SFT 微调作业</h3>
          <p>在魔搭云端进行全量 SFT 与 LoRA 微调，理解聊天模板与 loss 遮盖机制。</p>
          <div class="project-tags">
            <span class="tag">LoRA</span>
            <span class="tag">Transformers</span>
          </div>
        </article>

        <article class="project-card">
          <span class="project-index">03</span>
          <h3>电商图片下载插件</h3>
          <p>Chrome 扩展插件，使用 Cursor 辅助开发，GitHub Pages 部署。</p>
          <div class="project-tags">
            <span class="tag">JavaScript</span>
            <span class="tag">Chrome 扩展</span>
          </div>
        </article>

        <article class="project-card">
          <span class="project-index">04</span>
          <h3>个人主页网站</h3>
          <p>深色科技风个人主页，Vue 3 + Vite 构建，带终端打字机动画，GitHub Pages 部署。</p>
          <div class="project-tags">
            <span class="tag">Vue 3</span>
            <span class="tag">Vite</span>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- 博客 -->
  <section id="blog" class="section reveal">
    <div class="container">
      <div class="section-head">
        <span class="section-label">04 / NOTES</span>
        <h2 class="section-title">博客</h2>
      </div>

      <div class="timeline">
        <div class="timeline-item">
          <span class="timeline-dot"></span>
          <div class="timeline-body">
            <span class="timeline-date">2026 · 10</span>
            <h3>从零实现一个 BPE 分词器</h3>
            <p>记录手写 BPE 分词器的过程，理解合并规则与词表构建。</p>
          </div>
        </div>
        <div class="timeline-item">
          <span class="timeline-dot"></span>
          <div class="timeline-body">
            <span class="timeline-date">2026 · 10</span>
            <h3>大模型预训练流程记录</h3>
            <p>从数据准备、训练脚本到 loss 曲线的完整流程。</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 联系 -->
  <section id="contact" class="section reveal">
    <div class="container">
      <div class="section-head">
        <span class="section-label">05 / CONTACT</span>
        <h2 class="section-title">联系我</h2>
      </div>

      <div class="contact-card">
        <div>
          <h3>有想法？欢迎聊聊</h3>
          <p>课程作业、项目合作或者单纯交流技术，都可以找我。</p>
        </div>
        <div class="contact-actions">
          <a class="btn-primary" href="mailto:3465473990@qq.com">发邮件</a>
          <a class="btn-secondary" href="https://github.com/mysterious-aliens" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>

      <div class="contact-lines">
        <span>邮箱 3465473990@qq.com</span>
        <span>GitHub github.com/mysterious-aliens</span>
      </div>
    </div>
  </section>

  <footer class="footer">
    <span>© 2026 陈堃</span>
    <span class="footer-dot">·</span>
    <span>Built with Vue 3 + Vite</span>
  </footer>
</template>
