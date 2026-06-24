<template>
  <div class="container">
    <h1>职业规划</h1>
    <p class="subtitle">基于你的测评结果，探索适合的发展方向（功能拓展中）</p>

    <div class="card">
      <h3>即将上线</h3>
      <ul>
        <li>结合 Holland 三码与 Gallup 优势领域的职业路径建议</li>
        <li>专业与院校方向参考</li>
        <li>阶段性目标与行动清单</li>
        <li>与导师/咨询师的沟通记录</li>
      </ul>
      <p class="hint">你可在「个人资料」中填写职业规划意向，数据将保留供后续模块使用。</p>
      <button @click="$router.push('/profile')">完善个人资料</button>
      <button class="btn-secondary" @click="$router.push('/student')">返回仪表盘</button>
    </div>
  </div>
</template>

<style scoped>
.subtitle { color: #666; }
ul { line-height: 1.8; color: #4b5563; }
.hint { color: #6b7280; font-size: 14px; margin: 16px 0; }
.btn-secondary { background: #6b7280; margin-left: 8px; }
</style>
