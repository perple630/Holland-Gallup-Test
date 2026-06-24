<template>
  <div class="container">
    <h1>个人资料</h1>
    <p class="subtitle">完善资料有助于生成更贴合的测评解读（学校、年级为必填项）</p>

    <div class="card" style="max-width: 640px;">
      <form @submit.prevent="handleSave">
        <div class="form-row">
          <div class="form-group">
            <label>用户名</label>
            <input :value="auth.user?.username" disabled />
          </div>
          <div class="form-group">
            <label>姓名 *</label>
            <input v-model="form.display_name" required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>学校 *</label>
            <input v-model="form.school" required />
          </div>
          <div class="form-group">
            <label>年级 *</label>
            <input v-model="form.grade" required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>班级</label>
            <input v-model="form.class_name" />
          </div>
          <div class="form-group">
            <label>手机</label>
            <input v-model="form.phone" />
          </div>
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="form.email" type="email" />
        </div>
        <div class="form-group" v-if="auth.isStudent">
          <label>职业规划意向（拓展）</label>
          <textarea v-model="form.career_note" rows="4" placeholder="可填写感兴趣的方向、困惑或目标，供后续职业规划模块使用"></textarea>
        </div>

        <div class="actions">
          <button type="submit" :disabled="loading">{{ loading ? '保存中...' : '保存资料' }}</button>
          <button type="button" class="btn-secondary" @click="$router.push('/change-password')">修改密码</button>
        </div>
        <p v-if="message" :class="messageOk ? 'success' : 'error'">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { updateProfile } from '../api'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const message = ref('')
const messageOk = ref(false)

const form = ref({
  display_name: '',
  school: '',
  grade: '',
  class_name: '',
  phone: '',
  email: '',
  career_note: '',
})

onMounted(async () => {
  try {
    await auth.refreshUser()
    const u = auth.user || {}
    form.value = {
      display_name: u.display_name || '',
      school: u.school || '',
      grade: u.grade || '',
      class_name: u.class_name || '',
      phone: u.phone || '',
      email: u.email || '',
      career_note: u.career_note || '',
    }
  } catch (e) {
    message.value = '加载资料失败'
  }
})

async function handleSave() {
  loading.value = true
  message.value = ''
  try {
    await updateProfile(form.value)
    await auth.refreshUser()
    messageOk.value = true
    message.value = '资料已保存'
    if (auth.isStudent && auth.profileComplete) {
      setTimeout(() => router.push('/student'), 600)
    }
  } catch (err) {
    messageOk.value = false
    message.value = err.response?.data?.detail || '保存失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.subtitle { color: #666; margin-bottom: 20px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
@media (max-width: 640px) { .form-row { grid-template-columns: 1fr; } }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 14px; color: #4b5563; }
.form-group input, .form-group textarea {
  width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px;
}
.actions { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
.btn-secondary { background: #6b7280; }
.error { color: #dc2626; margin-top: 12px; }
.success { color: #16a34a; margin-top: 12px; }
</style>
