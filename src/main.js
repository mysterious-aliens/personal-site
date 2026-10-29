import { createApp } from 'vue'
import App from './App.vue'
import Admin from './Admin.vue'
import './style.css'

let app = null

function isAdminPage() {
  return window.location.hash.startsWith('#admin') || window.location.pathname.includes('/admin')
}

function render() {
  const isAdmin = isAdminPage()
  const root = document.getElementById('app')
  if (app) app.unmount()
  root.innerHTML = ''
  app = createApp(isAdmin ? Admin : App)
  app.mount(root)
}

window.addEventListener('hashchange', render)
window.addEventListener('popstate', render)
render()
