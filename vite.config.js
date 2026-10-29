import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// GitHub Pages 项目站点地址是 https://<user>.github.io/personal-site/
// 所以资源路径要带上 /personal-site/ 前缀
export default defineConfig({
  plugins: [vue()],
  base: '/personal-site/',
})
