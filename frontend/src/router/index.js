import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: () => import('../views/ChangePassword.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/student',
    name: 'StudentDashboard',
    component: () => import('../views/StudentDashboard.vue'),
    meta: { requiresAuth: true, roles: ['student'] },
  },
  {
    path: '/student/holland',
    name: 'HollandAssessment',
    component: () => import('../views/HollandAssessment.vue'),
    meta: { requiresAuth: true, roles: ['student'] },
  },
  {
    path: '/student/gallup',
    name: 'GallupAssessment',
    component: () => import('../views/GallupAssessment.vue'),
    meta: { requiresAuth: true, roles: ['student'] },
  },
  {
    path: '/student/report',
    name: 'StudentReport',
    component: () => import('../views/StudentReport.vue'),
    meta: { requiresAuth: true, roles: ['student'] },
  },
  {
    path: '/student/career',
    name: 'CareerPlanning',
    component: () => import('../views/CareerPlanning.vue'),
    meta: { requiresAuth: true, roles: ['student'] },
  },
  {
    path: '/teacher',
    name: 'TeacherDashboard',
    component: () => import('../views/TeacherDashboard.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'] },
  },
  {
    path: '/teacher/report/:studentId',
    name: 'TeacherReport',
    component: () => import('../views/TeacherReport.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'] },
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, roles: ['admin'] },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next('/login')
    return
  }

  if (to.meta.roles && auth.user && !to.meta.roles.includes(auth.user.role)) {
    next(auth.homePath)
    return
  }

  if (
    auth.isLoggedIn &&
    auth.mustChangePassword &&
    to.name !== 'ChangePassword' &&
    to.path !== '/login'
  ) {
    next('/change-password')
    return
  }

  next()
})

export default router
