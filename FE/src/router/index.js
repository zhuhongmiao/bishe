import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user.js'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('../views/home.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', component: () => import('../views/home/welcome.vue') },
        { path: 'profile', component: () => import('../views/home/profile.vue') },
        { path: 'search', component: () => import('../views/home/search.vue') },
        { path: 'analysis', component: () => import('../views/home/analysis.vue') },
        { path: 'price-prediction', component: () => import('../views/home/pricePrediction.vue') },
        { path: 'ai-chat', component: () => import('../views/home/aiChat.vue') },
      ],
    },
    {
      path: '/admin',
      component: () => import('../views/admin/layout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: '', component: () => import('../views/admin/dashboard.vue') },
        { path: 'users', component: () => import('../views/admin/users.vue') },
        { path: 'fabrics', component: () => import('../views/admin/fabrics.vue') },
      ],
    },
    {
      path: '/fabric/:id',
      component: () => import('../views/home/fabricDetail.vue'),
      meta: { requiresAuth: true },
    },
    { path: '/login', component: () => import('../views/login.vue') },
    { path: '/admin/login', component: () => import('../views/admin/login.vue') },
    { path: '/register', component: () => import('../views/register.vue') },
  ],
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isLogin) {
    if (to.path.startsWith('/admin')) {
      next('/admin/login')
      return
    }
    next('/login')
    return
  }

  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/')
    return
  }

  next()
})

export default router
