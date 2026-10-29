// 站点默认内容：后端不可用时作为兜底，保证 GitHub Pages 也能正常展示
export const DEFAULT_CONTENT = {
  name: '陈堃',
  role: '物联网工程在读 · 大模型与深度学习方向',
  tagline: '从零训练 63.91M 参数中文模型，手写 BPE 分词器',
  badge: '辽宁 · 大连　正在学习大模型',
  stats: [
    { num: '04', label: '实训项目' },
    { num: '63.91M', label: '模型参数' },
    { num: '1.24GB', label: '训练语料' },
  ],
  about: [
    '我是陈堃，大连民族大学物联网工程专业大三学生，方向是大模型与深度学习工程。',
    '喜欢从零开始造轮子，从分词器到预训练模型都自己动手实现过一遍，喜欢把原理搞懂再写代码。',
    '目前在做课程设计项目，学习 Web 开发、Git 部署、AI 辅助开发等技术。',
  ],
  meta: ['📍 辽宁 · 大连', '🎓 大连民族大学', '💡 大模型工程'],
  skills: [
    { icon: '💻', title: '编程语言', desc: '日常写代码的主力语言', tags: ['Python', 'C语言', 'Java', 'JavaScript'] },
    { icon: '🧠', title: 'AI / 深度学习', desc: '从训练到微调的完整链路', tags: ['PyTorch', 'Transformers', 'LoRA', 'BPE 分词器'] },
    { icon: '🛠️', title: '开发工具', desc: '版本管理与 AI 辅助开发', tags: ['Git', 'GitHub', 'VS Code', 'Cursor'] },
    { icon: '✨', title: '其他', desc: '课程里接触过的技术', tags: ['HTML/CSS', 'MySQL', '51单片机', 'Proteus'] },
  ],
  projects: [
    { title: 'MiniMind 大模型预训练', desc: '从零实现 63.91M 参数的中文预训练模型，包括 BPE 分词器、Transformer 架构与训练流程。', tags: ['PyTorch', 'Transformer'] },
    { title: 'SFT 微调作业', desc: '在魔搭云端进行全量 SFT 与 LoRA 微调，理解聊天模板与 loss 遮盖机制。', tags: ['LoRA', 'Transformers'] },
    { title: '电商图片下载插件', desc: 'Chrome 扩展插件，使用 Cursor 辅助开发，GitHub Pages 部署。', tags: ['JavaScript', 'Chrome 扩展'] },
    { title: '个人主页网站', desc: '深色科技风个人主页，Vue 3 + Vite 构建，带终端打字机动画，后端可实时修改内容。', tags: ['Vue 3', 'Vite'] },
  ],
  blog: [
    { date: '2026 · 10', title: '从零实现一个 BPE 分词器', desc: '记录手写 BPE 分词器的过程，理解合并规则与词表构建。' },
    { date: '2026 · 10', title: '大模型预训练流程记录', desc: '从数据准备、训练脚本到 loss 曲线的完整流程。' },
  ],
  contact: { email: '3465473990@qq.com', github: 'github.com/mysterious-aliens' },
}
