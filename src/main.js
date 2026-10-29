import { createApp } from 'vue'
import App from './App.vue'
import Admin from './Admin.vue'
import './style.css'

let app = null

function render() {
  const isAdmin = window.location.hash.startsWith('#admin')
  const root = document.getElementById('app')
  if (app) app.unmount()
  root.innerHTML = ''
  app = createApp(isAdmin ? Admin : App)
  app.mount(root)
}

window.addEventListener('hashchange', render)
render()
