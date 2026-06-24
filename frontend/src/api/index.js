import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

export default api

export async function login(credentials) {
  const res = await api.post('/auth/login', credentials)
  return res.data
}

export async function register(data) {
  const res = await api.post('/auth/register', data)
  return res.data
}

export async function getMe() {
  const res = await api.get('/auth/me')
  return res.data
}

export async function updateProfile(data) {
  const res = await api.patch('/auth/profile', data)
  return res.data
}

export async function changePassword(data) {
  const res = await api.post('/auth/change-password', data)
  return res.data
}

export async function getProgress() {
  const res = await api.get('/assessments/progress')
  return res.data
}

export async function getQuestions(type) {
  const res = await api.get('/assessments/questions', { params: { assessment_type: type } })
  return res.data
}

export async function submitHolland(answers) {
  const res = await api.post('/assessments/holland', { answers })
  return res.data
}

export async function submitGallup(answers) {
  const res = await api.post('/assessments/gallup', { answers })
  return res.data
}

export async function getStudentReport() {
  const res = await api.get('/reports/student')
  return res.data
}

export async function getTeacherStudents() {
  const res = await api.get('/teacher/students')
  return res.data
}

export async function createStudent(data) {
  const res = await api.post('/teacher/students', data)
  return res.data
}

export async function updateStudent(id, data) {
  const res = await api.patch(`/teacher/students/${id}`, data)
  return res.data
}

export async function resetStudentPassword(id, newPassword) {
  const res = await api.post(`/teacher/students/${id}/reset-password`, {
    new_password: newPassword || null,
  })
  return res.data
}

export async function deactivateStudent(id) {
  const res = await api.post(`/teacher/students/${id}/deactivate`)
  return res.data
}

export async function activateStudent(id) {
  const res = await api.post(`/teacher/students/${id}/activate`)
  return res.data
}

export async function getProfessionalReport(studentId) {
  const res = await api.get(`/reports/professional/${studentId}`)
  return res.data
}

export async function getStudentReportById(studentId) {
  const res = await api.get(`/reports/student/${studentId}`)
  return res.data
}

export async function getAdminStats() {
  const res = await api.get('/admin/stats')
  return res.data
}

export async function getAdminUsers(role) {
  const res = await api.get('/admin/users', { params: role ? { role } : {} })
  return res.data
}

export async function createAdminUser(data) {
  const res = await api.post('/admin/users', data)
  return res.data
}

export async function updateAdminUser(id, data) {
  const res = await api.patch(`/admin/users/${id}`, data)
  return res.data
}

export async function resetAdminUserPassword(id, newPassword) {
  const res = await api.post(`/admin/users/${id}/reset-password`, {
    new_password: newPassword || null,
  })
  return res.data
}
