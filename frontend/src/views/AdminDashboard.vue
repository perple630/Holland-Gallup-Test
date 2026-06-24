<template>
  <div class="container">
    <h1>系统管理</h1>
    <p class="subtitle">平台概览与用户账号管理</p>

    <div class="stats-grid" v-if="stats">
      <div class="stat-card" v-for="item in statItems" :key="item.label">
        <div class="stat-value">{{ item.value }}</div>
        <div class="stat-label">{{ item.label }}</div>
      </div>
    </div>

    <div class="card">
      <div class="toolbar">
        <select v-model="roleFilter" @change="loadUsers">
          <option value="">全部角色</option>
          <option value="student">学生</option>
          <option value="teacher">教师</option>
          <option value="admin">管理员</option>
        </select>
        <button @click="showCreate = true">新建用户</button>
        <button class="btn-secondary" @click="$router.push('/teacher')">学生测评管理</button>
      </div>

      <table class="user-table">
        <thead>
          <tr>
            <th>用户名</th>
            <th>姓名</th>
            <th>角色</th>
            <th>学校/年级</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.username }}</td>
            <td>{{ u.display_name || '—' }}</td>
            <td>{{ roleLabel(u.role) }}</td>
            <td>{{ u.school || '—' }} {{ u.grade || '' }}</td>
            <td>
              <span :class="u.is_active ? 'tag ok' : 'tag off'">{{ u.is_active ? '正常' : '停用' }}</span>
            </td>
            <td class="actions">
              <button class="btn-sm" @click="resetPwd(u)">重置密码</button>
              <button class="btn-sm btn-secondary" @click="toggleActive(u)">
                {{ u.is_active ? '停用' : '启用' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showCreate" class="modal-mask" @click.self="showCreate = false">
      <div class="modal card">
        <h3>新建用户</h3>
        <div class="form-group">
          <label>用户名</label>
          <input v-model="createForm.username" />
        </div>
        <div class="form-group">
          <label>初始密码</label>
          <input v-model="createForm.password" type="password" placeholder="留空则自动生成" />
        </div>
        <div class="form-group">
          <label>姓名</label>
          <input v-model="createForm.display_name" />
        </div>
        <div class="form-group">
          <label>角色</label>
          <select v-model="createForm.role">
            <option value="student">学生</option>
            <option value="teacher">教师</option>
            <option value="admin">管理员</option>
          </select>
        </div>
        <div class="modal-actions">
          <button @click="handleCreate">创建</button>
          <button class="btn-secondary" @click="showCreate = false">取消</button>
        </div>
        <p v-if="createMsg" class="success">{{ createMsg }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  getAdminStats,
  getAdminUsers,
  createAdminUser,
  updateAdminUser,
  resetAdminUserPassword,
} from '../api'

const stats = ref(null)
const users = ref([])
const roleFilter = ref('')
const showCreate = ref(false)
const createMsg = ref('')
const createForm = ref({
  username: '',
  password: '',
  display_name: '',
  role: 'teacher',
})

const statItems = computed(() => {
  if (!stats.value) return []
  const s = stats.value
  return [
    { label: '总用户', value: s.total_users },
    { label: '学生', value: s.students },
    { label: '教师', value: s.teachers },
    { label: '管理员', value: s.admins },
    { label: '双测评完成', value: s.completed_assessments },
  ]
})

function roleLabel(role) {
  return { student: '学生', teacher: '教师', admin: '管理员' }[role] || role
}

async function loadStats() {
  stats.value = await getAdminStats()
}

async function loadUsers() {
  users.value = await getAdminUsers(roleFilter.value || undefined)
}

onMounted(async () => {
  await Promise.all([loadStats(), loadUsers()])
})

async function handleCreate() {
  createMsg.value = ''
  const payload = { ...createForm.value }
  if (!payload.password) delete payload.password
  const res = await createAdminUser(payload)
  let msg = `已创建用户 ${res.username}`
  if (!createForm.value.password) {
    const pwdRes = await resetAdminUserPassword(res.id)
    msg += `，初始密码：${pwdRes.new_password}`
  }
  createMsg.value = msg
  await loadUsers()
  await loadStats()
}

async function resetPwd(user) {
  const custom = prompt(`为 ${user.username} 设置新密码（留空则自动生成）`, '')
  if (custom === null) return
  const res = await resetAdminUserPassword(user.id, custom || null)
  alert(`密码已重置\n用户名：${res.username}\n新密码：${res.new_password}`)
}

async function toggleActive(user) {
  await updateAdminUser(user.id, { is_active: !user.is_active })
  await loadUsers()
}
</script>

<style scoped>
.subtitle { color: #666; }
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}
.stat-card {
  background: #fff;
  border-radius: 10px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stat-value { font-size: 28px; font-weight: 700; color: #2563eb; }
.stat-label { font-size: 13px; color: #6b7280; margin-top: 4px; }
.toolbar { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; align-items: center; }
.user-table { width: 100%; border-collapse: collapse; }
.user-table th, .user-table td { padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: left; }
.tag { padding: 2px 8px; border-radius: 12px; font-size: 12px; }
.tag.ok { background: #dcfce7; color: #166534; }
.tag.off { background: #fee2e2; color: #991b1b; }
.actions { display: flex; gap: 6px; flex-wrap: wrap; }
.btn-sm { padding: 4px 10px; font-size: 12px; }
.btn-secondary { background: #6b7280; }
.modal-mask {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal { width: 100%; max-width: 420px; }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; margin-bottom: 4px; font-size: 14px; }
.form-group input, .form-group select {
  width: 100%; padding: 8px 10px; border: 1px solid #d1d5db; border-radius: 6px;
}
.modal-actions { display: flex; gap: 8px; margin-top: 12px; }
.success { color: #16a34a; font-size: 13px; margin-top: 8px; }
</style>
