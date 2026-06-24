<template>
  <div class="container">
    <h1>修改密码</h1>
    <p class="subtitle" v-if="auth.mustChangePassword">首次登录或密码已重置，请先修改密码。</p>

    <div class="card" style="max-width: 480px;">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>原密码</label>
          <input v-model="oldPassword" type="password" required />
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input v-model="newPassword" type="password" required placeholder="至少8位，含大小写/数字/符号" />
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input v-model="confirmPassword" type="password" required />
        </div>
        <button type="submit" :disabled="loading">{{ loading ? '提交中...' : '确认修改' }}</button>
        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="success" class="success">{{ success }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { changePassword } from '../api'

const router = useRouter()
const auth = useAuthStore()
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleSubmit() {
  error.value = ''
  success.value = ''
  if (newPassword.value !== confirmPassword.value) {
    error.value = '两次输入的新密码不一致'
    return
  }
  loading.value = true
  try {
    await changePassword({ old_password: oldPassword.value, new_password: newPassword.value })
    await auth.refreshUser()
    success.value = '密码修改成功'
    setTimeout(() => router.push(auth.homePath), 800)
  } catch (err) {
    error.value = err.response?.data?.detail || '修改失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.subtitle { color: #666; margin-bottom: 20px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 14px; }
.form-group input { width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; }
.error { color: #dc2626; margin-top: 12px; }
.success { color: #16a34a; margin-top: 12px; }
</style>
