import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { getMe } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isStaff = computed(() => isTeacher.value || isAdmin.value)
  const mustChangePassword = computed(() => !!user.value?.must_change_password)
  const profileComplete = computed(() => !!user.value?.profile_complete)

  const homePath = computed(() => {
    if (isAdmin.value) return '/admin'
    if (isTeacher.value) return '/teacher'
    return '/student'
  })

  function persist() {
    localStorage.setItem('token', token.value)
    localStorage.setItem('user', JSON.stringify(user.value))
    api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  function setAuth(authData) {
    token.value = authData.access_token
    user.value = {
      id: authData.user_id,
      username: authData.username,
      role: authData.role,
      display_name: authData.display_name,
      profile_complete: authData.profile_complete,
      must_change_password: authData.must_change_password,
    }
    persist()
  }

  function setUser(userData) {
    user.value = { ...user.value, ...userData }
    persist()
  }

  async function refreshUser() {
    if (!token.value) return null
    const me = await getMe()
    user.value = {
      id: me.id,
      username: me.username,
      role: me.role,
      display_name: me.display_name,
      email: me.email,
      grade: me.grade,
      class_name: me.class_name,
      school: me.school,
      phone: me.phone,
      career_note: me.career_note,
      profile_complete: me.profile_complete,
      must_change_password: me.must_change_password,
      is_active: me.is_active,
    }
    persist()
    return user.value
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete api.defaults.headers.common['Authorization']
  }

  function init() {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }
  }

  return {
    token,
    user,
    isLoggedIn,
    isTeacher,
    isStudent,
    isAdmin,
    isStaff,
    mustChangePassword,
    profileComplete,
    homePath,
    setAuth,
    setUser,
    refreshUser,
    logout,
    init,
  }
})
