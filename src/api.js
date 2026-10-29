// 后端接口封装
// 本地开发默认连 127.0.0.1:5000；部署时可以通过 VITE_API_BASE 指定线上地址
export const API_BASE =
  import.meta.env.VITE_API_BASE || 'http://127.0.0.1:5001/api'

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok || data.ok === false) {
    throw new Error(data.error || `请求失败（${res.status}）`)
  }
  return data
}

export async function fetchContent() {
  const data = await request('/content')
  return data.data
}

export async function login(username, password) {
  const data = await request('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
  return data.token
}

export async function saveContent(token, content) {
  return request('/content', {
    method: 'PUT',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(content),
  })
}

export async function resetContent(token) {
  return request('/content/reset', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })
}
