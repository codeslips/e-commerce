import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue'),
    meta: { guest: true },
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('@/views/Products.vue'),
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('@/views/Cart.vue'),
    meta: { requiresAuth: true, requiresDealer: true },
  },
  {
    path: '/orders',
    name: 'orders',
    component: () => import('@/views/Orders.vue'),
    meta: { requiresAuth: true, requiresDealer: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  // Admin routes
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/products',
    name: 'admin-products',
    component: () => import('@/views/admin/Products.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/orders',
    name: 'admin-orders',
    component: () => import('@/views/admin/Orders.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/dealers',
    name: 'admin-dealers',
    component: () => import('@/views/admin/Dealers.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guards
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  
  // Wait for auth to initialize
  if (!authStore.initialized) {
    await authStore.fetchCurrentUser()
  }
  
  // Guest only pages (login)
  if (to.meta.guest && authStore.isAuthenticated) {
    return next(authStore.isAdmin ? '/admin' : '/products')
  }
  
  // Auth required
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }
  
  // Admin required
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next('/')
  }
  
  // Dealer required (for orders, cart)
  if (to.meta.requiresDealer && !authStore.isDealer && !authStore.isAdmin) {
    return next('/login')
  }
  
  next()
})

export default router
