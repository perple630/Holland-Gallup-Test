<template>
  <div class="container login-container">
    <div class="card login-card">
      <h1>RIASEC × CliftonStrengths</h1>
      <p class="subtitle">双维度职业兴趣与优势测评平台</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="username" type="text" placeholder="请输入用户名" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" required autocomplete="current-password" />
        </div>
        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>

      <div class="links">
        <router-link to="/register">学生注册</router-link>
      </div>

      <div class="demo-hint">
        <p>首次使用请注册；教师/管理员账号由系统分配。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { login } from '../api'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    const res = await login({
      username: username.value,
      password: password.value,
    })
    auth.setAuth(res)
    if (res.must_change_password) {
      router.push('/change-password')
    } else if (res.role === 'admin') {
      router.push('/admin')
    } else if (res.role === 'teacher') {
      router.push('/teacher')
    } else {
      router.push('/student')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码'
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
}

.login-card {
  width: 100%;
  max-width: 420px;
  text-align: center;
}

.subtitle {
  color: #666;
  margin-bottom: 24px;
}

.form-group {
  text-align: left;
  margin-bottom: 16px;
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
  font-size: 16px;
}

.error {
  color: #dc2626;
  margin-top: 12px;
  font-size: 14px;
}

.links {
  margin-top: 16px;
  font-size: 14px;
}

.links a {
  color: #2563eb;
  text-decoration: none;
}

.demo-hint {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
  font-size: 13px;
  color: #6b7280;
}
</style>
