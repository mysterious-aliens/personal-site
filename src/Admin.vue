<script setup>
import { ref, computed, onMounted } from 'vue'
import { DEFAULT_CONTENT } from './defaults'
import { fetchContent, login, saveContent, resetContent } from './api'

const token = ref(localStorage.getItem('site_token') || '')
const loggedIn = computed(() => !!token.value)

const username = ref('admin')
const password = ref('')
const error = ref('')
const notice = ref('')
const saving = ref(false)
const loading = ref(false)

const form = ref({
  name: '',
  role: '',
  tagline: '',
  badge: '',
  stats: '',
  about: '',
  meta: '',
  skills: '',
  projects: '',
  blog: '',
  email: '',
  github: '',
})

function fillForm(data) {
  form.value = {
    name: data.name || '',
    role: data.role || '',
    tagline: data.tagline || '',
    badge: data.badge || '',
    stats: (data.stats || []).map((s) => `${s.num}|${s.label}`).join('\n'),
    about: (data.about || []).join('\n'),
    meta: (data.meta || []).join('、'),
    skills: (data.skills || [])
      .map((s) => `${s.icon}|${s.title}|${s.desc}|${(s.tags || []).join(',')}`)
      .join('\n'),
    projects: (data.projects || [])
      .map((p) => `${p.title}|${p.desc}|${(p.tags || []).join(',')}`)
      .join('\n'),
    blog: (data.blog || []).map((b) => `${b.date}|${b.title}|${b.desc}`).join('\n'),
    email: data.contact?.email || '',
    github: data.contact?.github || '',
  }
}

function splitLines(text) {
  return text
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
}

function splitTags(text) {
  return (text || '')
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean)
}

function buildData() {
  return {
    name: form.value.name.trim(),
    role: form.value.role.trim(),
    tagline: form.value.tagline.trim(),
    badge: form.value.badge.trim(),
    stats: splitLines(form.value.stats).map((line) => {
      const [num, label] = line.split('|')
      return { num: (num || '').trim(), label: (label || '').trim() }
    }),
    about: splitLines(form.value.about),
    meta: form.value.meta
      .split(/[、,，]/)
      .map((m) => m.trim())
      .filter(Boolean),
    skills: splitLines(form.value.skills).map((line) => {
      const [icon, title, desc, tags] = line.split('|')
      return {
        icon: (icon || '✨').trim(),
        title: (title || '').trim(),
        desc: (desc || '').trim(),
        tags: splitTags(tags),
      }
    }),
    projects: splitLines(form.value.projects).map((line) => {
      const [title, desc, tags] = line.split('|')
      return { title: (title || '').trim(), desc: (desc || '').trim(), tags: splitTags(tags) }
    }),
    blog: splitLines(form.value.blog).map((line) => {
      const [date, title, desc] = line.split('|')
      return { date: (date || '').trim(), title: (title || '').trim(), desc: (desc || '').trim() }
    }),
    contact: { email: form.value.email.trim(), github: form.value.github.trim() },
  }
}

async function load() {
  loading.value = true
  try {
    const data = await fetchContent()
    fillForm(data)
  } catch (err) {
    error.value = err.message
    fillForm(DEFAULT_CONTENT)
  } finally {
    loading.value = false
  }
}

async function doLogin() {
  error.value = ''
  notice.value = ''
  try {
    token.value = await login(username.value.trim(), password.value)
    localStorage.setItem('site_token', token.value)
    password.value = ''
    await load()
  } catch (err) {
    error.value = err.message
  }
}

function logout() {
  token.value = ''
  localStorage.removeItem('site_token')
}

async function doSave() {
  error.value = ''
  notice.value = ''
  saving.value = true
  try {
    await saveContent(token.value, buildData())
    notice.value = '保存成功，前台刷新即可看到最新内容'
    setTimeout(() => (notice.value = ''), 4000)
  } catch (err) {
    error.value = err.message
    if (err.message.includes('登录')) logout()
  } finally {
    saving.value = false
  }
}

async function doReset() {
  if (!confirm('确定恢复默认内容吗？')) return
  try {
    await resetContent(token.value)
    await load()
    notice.value = '已恢复默认内容'
  } catch (err) {
    error.value = err.message
  }
}

onMounted(() => {
  if (token.value) load()
})
</script>

<template>
  <div class="admin">
    <header class="admin-header">
      <a class="admin-brand" href="./">
        <span class="logo-icon">C</span>
        <span>个人主页 · 内容管理</span>
      </a>
      <div class="admin-header-actions">
        <a class="btn-secondary" href="./">查看前台</a>
        <button v-if="loggedIn" class="btn-secondary" @click="logout">退出登录</button>
      </div>
    </header>

    <main class="admin-main">
      <div v-if="!loggedIn" class="admin-login">
        <h1>管理员登录</h1>
        <p class="admin-hint">默认账号 admin / chenkun2026（可在后端环境变量里改）</p>
        <label>
          用户名
          <input v-model="username" type="text" autocomplete="username" />
        </label>
        <label>
          密码
          <input v-model="password" type="password" autocomplete="current-password" @keyup.enter="doLogin" />
        </label>
        <button class="btn-primary" @click="doLogin">登录</button>
        <p v-if="error" class="admin-error">{{ error }}</p>
      </div>

      <div v-else class="admin-editor">
        <div class="admin-editor-head">
          <h1>编辑站点内容</h1>
          <div class="admin-editor-actions">
            <button class="btn-secondary" @click="doReset">恢复默认</button>
            <button class="btn-primary" :disabled="saving" @click="doSave">
              {{ saving ? '保存中…' : '保存并生效' }}
            </button>
          </div>
        </div>

        <p v-if="notice" class="admin-notice">{{ notice }}</p>
        <p v-if="error" class="admin-error">{{ error }}</p>

        <div class="admin-grid">
          <label class="admin-field">
            姓名
            <input v-model="form.name" type="text" />
          </label>
          <label class="admin-field">
            方向 / 身份
            <input v-model="form.role" type="text" />
          </label>
          <label class="admin-field admin-field-wide">
            一句话介绍
            <input v-model="form.tagline" type="text" />
          </label>
          <label class="admin-field admin-field-wide">
            顶部状态标签
            <input v-model="form.badge" type="text" />
          </label>

          <label class="admin-field admin-field-wide">
            数据指标（每行一个：数值|说明）
            <textarea v-model="form.stats" rows="3"></textarea>
          </label>

          <label class="admin-field admin-field-wide">
            关于我（每行一段）
            <textarea v-model="form.about" rows="4"></textarea>
          </label>

          <label class="admin-field admin-field-wide">
            个人标签（用顿号或逗号分隔）
            <input v-model="form.meta" type="text" />
          </label>

          <label class="admin-field admin-field-wide">
            技能（每行一个：图标|标题|说明|标签1,标签2）
            <textarea v-model="form.skills" rows="5"></textarea>
          </label>

          <label class="admin-field admin-field-wide">
            项目（每行一个：标题|描述|标签1,标签2）
            <textarea v-model="form.projects" rows="6"></textarea>
          </label>

          <label class="admin-field admin-field-wide">
            博客（每行一个：日期|标题|描述）
            <textarea v-model="form.blog" rows="4"></textarea>
          </label>

          <label class="admin-field">
            邮箱
            <input v-model="form.email" type="text" />
          </label>
          <label class="admin-field">
            GitHub
            <input v-model="form.github" type="text" />
          </label>
        </div>

        <p class="admin-tip">
          保存后打开前台页面即可看到最新内容；前台内容由后端接口实时读取，不重新构建。
        </p>
      </div>
    </main>
  </div>
</template>
