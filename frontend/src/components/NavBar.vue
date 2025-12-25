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
  <header class="sticky top-0 z-50 w-full backdrop-blur flex-none transition-colors duration-500 bg-white/80 border-b border-slate-900/10">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-3 group cursor-pointer" @click="closeMobileMenu">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center shadow-lg shadow-orange-200/50 group-hover:scale-105 transition-transform duration-200">
            <span class="text-white font-black text-xs">XT</span>
          </div>
          <div class="flex items-baseline gap-1.5">
            <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600">欣与甜</span>
            <span class="text-xs text-slate-400 hidden sm:inline">订货平台</span>
          </div>
        </router-link>

        <!-- Mobile toggle -->
        <button 
          class="md:hidden flex flex-col gap-1 p-2 -mr-2"
          @click="toggleMobileMenu"
        >
          <span class="w-5 h-0.5 bg-slate-700 rounded-full transition-all" :class="{ 'rotate-45 translate-y-1.5': mobileMenuOpen }"></span>
          <span class="w-5 h-0.5 bg-slate-700 rounded-full transition-all" :class="{ 'opacity-0': mobileMenuOpen }"></span>
          <span class="w-5 h-0.5 bg-slate-700 rounded-full transition-all" :class="{ '-rotate-45 -translate-y-1.5': mobileMenuOpen }"></span>
        </button>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center gap-8 text-sm font-medium">
          <router-link 
            to="/products" 
            class="text-slate-600 hover:text-amber-600 transition-colors duration-200"
          >
            产品目录
          </router-link>
          
          <template v-if="isLoggedIn && isDealer">
            <router-link 
              to="/orders" 
              class="text-slate-600 hover:text-amber-600 transition-colors duration-200"
            >
              我的订单
            </router-link>
          </template>
          
          <template v-if="isAdmin">
            <router-link 
              to="/admin" 
              class="text-amber-600 hover:text-amber-700 transition-colors duration-200 font-semibold"
            >
              管理后台
            </router-link>
          </template>
        </nav>

        <!-- Desktop Right Actions -->
        <div class="hidden md:flex items-center gap-4">
          <template v-if="isLoggedIn && isDealer">
            <router-link 
              to="/cart" 
              class="relative p-2 text-slate-600 hover:text-amber-600 transition-colors duration-200"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span 
                v-if="cartCount > 0" 
                class="absolute -top-0.5 -right-0.5 bg-orange-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center"
              >
                {{ cartCount }}
              </span>
            </router-link>
          </template>

          <template v-if="isLoggedIn">
            <router-link 
              to="/profile" 
              class="flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-amber-600 transition-colors duration-200"
            >
              <div class="w-7 h-7 rounded-full bg-slate-100 flex items-center justify-center">
                <svg class="w-4 h-4 text-slate-500" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
              <span class="max-w-[80px] truncate">{{ username }}</span>
            </router-link>
            <button 
              @click="handleLogout"
              class="px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-all duration-200"
            >
              退出
            </button>
          </template>

          <template v-else>
            <router-link 
              to="/login" 
              class="px-5 py-2.5 text-sm font-semibold text-white bg-slate-900 hover:bg-slate-800 rounded-xl shadow-lg shadow-slate-900/10 transition-all duration-200"
            >
              登录
            </router-link>
          </template>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div 
      v-show="mobileMenuOpen"
      class="md:hidden border-t border-slate-100 bg-white"
    >
      <div class="container mx-auto px-4 py-4 space-y-2">
        <router-link 
          to="/products" 
          class="block px-4 py-3 text-slate-600 hover:text-amber-600 hover:bg-slate-50 rounded-xl transition-colors duration-200"
          @click="closeMobileMenu"
        >
          产品目录
        </router-link>

        <template v-if="isLoggedIn && isDealer">
          <router-link 
            to="/orders" 
            class="block px-4 py-3 text-slate-600 hover:text-amber-600 hover:bg-slate-50 rounded-xl transition-colors duration-200"
            @click="closeMobileMenu"
          >
            我的订单
          </router-link>
          <router-link 
            to="/cart" 
            class="flex items-center gap-2 px-4 py-3 text-slate-600 hover:text-amber-600 hover:bg-slate-50 rounded-xl transition-colors duration-200"
            @click="closeMobileMenu"
          >
            <span>购物车</span>
            <span v-if="cartCount > 0" class="bg-orange-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
              {{ cartCount }}
            </span>
          </router-link>
        </template>

        <template v-if="isAdmin">
          <router-link 
            to="/admin" 
            class="block px-4 py-3 text-amber-600 font-semibold hover:bg-amber-50 rounded-xl transition-colors duration-200"
            @click="closeMobileMenu"
          >
            管理后台
          </router-link>
        </template>

        <div class="pt-2 border-t border-slate-100">
          <template v-if="isLoggedIn">
            <router-link 
              to="/profile" 
              class="block px-4 py-3 text-slate-600 hover:text-amber-600 hover:bg-slate-50 rounded-xl transition-colors duration-200"
              @click="closeMobileMenu"
            >
              个人中心 ({{ username }})
            </router-link>
            <button 
              @click="handleLogout"
              class="w-full text-left px-4 py-3 text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-xl transition-colors duration-200"
            >
              退出登录
            </button>
          </template>

          <template v-else>
            <router-link 
              to="/login" 
              class="block px-4 py-3 text-center font-semibold text-white bg-slate-900 hover:bg-slate-800 rounded-xl transition-colors duration-200"
              @click="closeMobileMenu"
            >
              登录
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>
