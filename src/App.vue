<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { DEFAULT_CONTENT } from './defaults'
import { fetchContent } from './api'

const content = ref(DEFAULT_CONTENT)
const apiConnected = ref(false)
const terminalLines = ref([])
const running = ref(false)

const commands = [
  { cmd: 'whoami', output: [{ text: '陈堃 · 大连民族大学 物联网工程' }] },
  {
    cmd: 'cat direction.txt',
    output: [
      { text: '大模型与深度学习工程' },
      { text: '从零训练过 63.91M 参数的中文预训练模型', highlight: true },
      { text: '手写过 BPE 分词器，调过 Llama 3.1 的 LoRA', highlight: true },
    ],
  },
  { cmd: 'ls skills/', output: [{ text: 'Python   PyTorch   Transformers   LoRA   TypeScript   Git' }] },
  { cmd: 'git log --oneline -1', output: [{ text: '一切从“先把最小可用版本跑通”开始。' }] },
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

function observeReveals() {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('visible')
      })
    },
    { threshold: 0.12 }
  )
  document.querySelectorAll('.reveal:not(.visible)').forEach((el) => io.observe(el))
}

async function loadContent() {
  try {
    const data = await fetchContent()
    content.value = { ...DEFAULT_CONTENT, ...data }
    apiConnected.value = true
  } catch (err) {
    // 后端没启动时用默认内容，保证静态页面仍可访问
    console.info('后端未连接，使用默认内容：', err.message)
  }
}

onMounted(async () => {
  runTerminal()
  await loadContent()
  await nextTick()
  observeReveals()
})
</script>

<template>
  <!-- 导航 -->
  <nav class="navbar">
    <div class="nav-left">
      <div class="logo">
        <span class="logo-icon">{{ content.name.slice(0, 1) }}</span>
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
          {{ content.badge }}
        </div>

        <h1 class="title">
          你好，我是<br />
          <span class="gradient-text">{{ content.name }}</span>
        </h1>

        <p class="subtitle">{{ content.role }}</p>
        <p class="description">
          <span class="prompt">$</span> {{ content.tagline }}
        </p>

        <div class="buttons">
          <a href="#projects" class="btn-primary">看看我的项目</a>
          <a href="#contact" class="btn-secondary">联系我</a>
        </div>

        <div class="stats">
          <template v-for="(item, i) in content.stats" :key="i">
            <div class="stat-item">
              <div class="stat-num">{{ item.num }}</div>
              <div class="stat-label">{{ item.label }}</div>
            </div>
            <div v-if="i < content.stats.length - 1" class="stat-divider"></div>
          </template>
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
        <div class="avatar"><span>{{ content.name.slice(0, 1) }}</span></div>
        <div class="about-text">
          <p v-for="(line, i) in content.about" :key="i">{{ line }}</p>
          <div class="about-meta">
            <span v-for="(m, i) in content.meta" :key="i" class="meta-item">{{ m }}</span>
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
        <div v-for="(skill, i) in content.skills" :key="i" class="skill-category">
          <div class="skill-icon">{{ skill.icon }}</div>
          <h3>{{ skill.title }}</h3>
          <p class="skill-desc">{{ skill.desc }}</p>
          <div class="skill-tags">
            <span v-for="(tag, j) in skill.tags" :key="j" class="tag">{{ tag }}</span>
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
        <article v-for="(p, i) in content.projects" :key="i" class="project-card">
          <span class="project-index">{{ String(i + 1).padStart(2, '0') }}</span>
          <h3>{{ p.title }}</h3>
          <p>{{ p.desc }}</p>
          <div class="project-tags">
            <span v-for="(tag, j) in p.tags" :key="j" class="tag">{{ tag }}</span>
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
        <div v-for="(item, i) in content.blog" :key="i" class="timeline-item">
          <span class="timeline-dot"></span>
          <div class="timeline-body">
            <span class="timeline-date">{{ item.date }}</span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.desc }}</p>
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
          <a class="btn-primary" :href="`mailto:${content.contact.email}`">发邮件</a>
          <a class="btn-secondary" :href="`https://${content.contact.github}`" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>

      <div class="contact-lines">
        <span>邮箱 {{ content.contact.email }}</span>
        <span>GitHub {{ content.contact.github }}</span>
      </div>
    </div>
  </section>

  <footer class="footer">
    <span>© 2026 {{ content.name }}</span>
    <span class="footer-dot">·</span>
    <span>Built with Vue 3 + Vite + Flask</span>
    <span class="footer-dot">·</span>
    <a v-if="apiConnected" class="footer-link" href="#admin">管理入口</a>
  </footer>
</template>
