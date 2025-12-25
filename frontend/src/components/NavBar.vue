<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore, useCartStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const mobileMenuOpen = ref(false)

const isLoggedIn = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => authStore.isAdmin)
const isDealer = computed(() => authStore.isDealer)
const username = computed(() => authStore.user?.username)
const cartCount = computed(() => cartStore.totalItems)

async function handleLogout() {
  await authStore.logout()
  router.push('/')
  mobileMenuOpen.value = false
}

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}
</script>

<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-brand" @click="closeMobileMenu">
        <span class="brand-text">欣与甜</span>
        <span class="brand-sub">订货平台</span>
      </router-link>
      
      <button class="mobile-toggle" @click="toggleMobileMenu">
        <span></span>
        <span></span>
        <span></span>
      </button>
      
      <div class="navbar-menu" :class="{ open: mobileMenuOpen }">
        <div class="navbar-start">
          <router-link to="/products" class="nav-link" @click="closeMobileMenu">
            产品目录
          </router-link>
          
          <template v-if="isLoggedIn && isDealer">
            <router-link to="/orders" class="nav-link" @click="closeMobileMenu">
              我的订单
            </router-link>
          </template>
          
          <template v-if="isAdmin">
            <router-link to="/admin" class="nav-link admin-link" @click="closeMobileMenu">
              管理后台
            </router-link>
          </template>
        </div>
        
        <div class="navbar-end">
          <template v-if="isLoggedIn && isDealer">
            <router-link to="/cart" class="nav-link cart-link" @click="closeMobileMenu">
              <span class="cart-icon">🛒</span>
              <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
            </router-link>
          </template>
          
          <template v-if="isLoggedIn">
            <router-link to="/profile" class="nav-link user-link" @click="closeMobileMenu">
              <span class="user-icon">👤</span>
              <span class="username">{{ username }}</span>
            </router-link>
            <button class="logout-btn" @click="handleLogout">
              退出
            </button>
          </template>
          
          <template v-else>
            <router-link to="/login" class="nav-link login-link" @click="closeMobileMenu">
              登录
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: #1a1a2e;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.navbar-brand {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  text-decoration: none;
}

.brand-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fbbf24;
}

.brand-sub {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
}

.mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
  background: none;
  border: none;
  cursor: pointer;
}

.mobile-toggle span {
  width: 20px;
  height: 2px;
  background: white;
  border-radius: 1px;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  justify-content: space-between;
  margin-left: 2rem;
}

.navbar-start,
.navbar-end {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.admin-link {
  color: #fbbf24;
}

.cart-link {
  position: relative;
  font-size: 1.25rem;
}

.cart-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #dc2626;
  color: white;
  font-size: 0.65rem;
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  font-weight: 600;
}

.user-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-icon {
  font-size: 1.1rem;
}

.username {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.login-link {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.login-link:hover {
  background: rgba(251, 191, 36, 0.3);
}

.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

@media (max-width: 768px) {
  .mobile-toggle {
    display: flex;
  }
  
  .navbar-menu {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    background: #1a1a2e;
    flex-direction: column;
    padding: 1rem;
    gap: 0.5rem;
    margin-left: 0;
    display: none;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .navbar-menu.open {
    display: flex;
  }
  
  .navbar-start,
  .navbar-end {
    flex-direction: column;
    width: 100%;
    gap: 0.25rem;
  }
  
  .nav-link {
    width: 100%;
    padding: 0.75rem;
  }
  
  .logout-btn {
    width: 100%;
    margin-top: 0.5rem;
  }
}
</style>

