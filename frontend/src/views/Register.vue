<template>
  <div class="container login-container">
    <div class="card login-card">
      <h1>学生注册</h1>
      <p class="subtitle">创建账号后即可参加 Holland 与 Gallup 测评</p>

      <form @submit.prevent="handleRegister">
        <div class="form-row">
          <div class="form-group">
            <label>用户名 *</label>
            <input v-model="form.username" required placeholder="登录用户名" />
          </div>
          <div class="form-group">
            <label>姓名</label>
            <input v-model="form.display_name" placeholder="真实姓名或昵称" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>密码 *</label>
            <input v-model="form.password" type="password" required placeholder="至少8位，含大小写/数字/符号" />
          </div>
          <div class="form-group">
            <label>确认密码 *</label>
            <input v-model="confirmPassword" type="password" required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>学校</label>
            <input v-model="form.school" placeholder="就读学校" />
          </div>
          <div class="form-group">
            <label>年级</label>
            <input v-model="form.grade" placeholder="如：高二 / 大三" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>班级</label>
            <input v-model="form.class_name" placeholder="可选" />
          </div>
          <div class="form-group">
            <label>手机 / 邮箱</label>
            <input v-model="form.phone" placeholder="联系方式（可选）" />
          </div>
        </div>

        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? '注册中...' : '注册并登录' }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
      <div class="links">
        <router-link to="/login">已有账号？去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { register, login } from '../api'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const error = ref('')
const confirmPassword = ref('')

const form = ref({
  username: '',
  password: '',
  display_name: '',
  school: '',
  grade: '',
  class_name: '',
  phone: '',
})

async function handleRegister() {
  error.value = ''
  if (form.value.password !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  try {
    await register(form.value)
    const res = await login({
      username: form.value.username,
      password: form.value.password,
    })
    auth.setAuth(res)
    router.push('/profile')
  } catch (err) {
    error.value = err.response?.data?.detail || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 24px 0;
}

.login-card {
  width: 100%;
  max-width: 640px;
}

.subtitle {
  color: #666;
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  margin-bottom: 12px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #4b5563;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.login-btn {
  width: 100%;
  margin-top: 8px;
  padding: 12px;
}

.error {
  color: #dc2626;
  margin-top: 12px;
}

.links {
  margin-top: 16px;
}

.links a {
  color: #2563eb;
  text-decoration: none;
}
</style>
