// 终端动画效果

const commands = [
  {
    cmd: 'whoami',
    output: [
      '陈堃 · 大连民族大学 物联网工程'
    ]
  },
  {
    cmd: 'cat direction.txt',
    output: [
      '大模型与深度学习工程',
      { text: '→ 从零训练过 63.91M 参数的中文预训练模型', highlight: true },
      { text: '→ 手写过 BPE 分词器，调过 Llama 3.1 的 LoRA', highlight: true }
    ]
  },
  {
    cmd: 'ls skills/',
    output: [
      'Python   PyTorch   Transformers   LoRA   TypeScript   Git'
    ]
  },
  {
    cmd: 'git log --oneline -1',
    output: [
      '一切从"先把最小可用版本跑通"开始。'
    ]
  }
];

const terminal = document.getElementById('terminal');
const rerunBtn = document.getElementById('rerunBtn');

// 打字机效果
async function typeText(element, text, speed = 30) {
  for (let i = 0; i < text.length; i++) {
    element.textContent += text[i];
    await sleep(speed);
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 执行动画
async function runTerminal() {
  terminal.innerHTML = '';
  
  for (const cmd of commands) {
    // 输出命令行
    const cmdLine = document.createElement('div');
    cmdLine.className = 'cmd-line';
    
    const cmdEl = document.createElement('span');
    cmdEl.className = 'cmd';
    cmdLine.appendChild(cmdEl);
    
    terminal.appendChild(cmdLine);
    await typeText(cmdEl, cmd.cmd, 50);
    await sleep(300);
    
    // 输出结果
    for (const line of cmd.output) {
      const outputEl = document.createElement('div');
      outputEl.className = 'output';
      
      if (typeof line === 'object' && line.highlight) {
        outputEl.classList.add('highlight');
        outputEl.innerHTML = '<span class="arrow">→</span>' + line.text;
      } else {
        outputEl.textContent = typeof line === 'string' ? line : line.text;
      }
      
      terminal.appendChild(outputEl);
      await sleep(200);
    }
    
    await sleep(300);
  }
}

// 重新执行按钮
rerunBtn.addEventListener('click', runTerminal);

// 启动
runTerminal();
