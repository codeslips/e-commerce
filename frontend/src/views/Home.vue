<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores'

const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => authStore.isAdmin)
const username = computed(() => authStore.user?.username)
const companyName = computed(() => authStore.user?.dealer?.company_name)
</script>

<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative overflow-hidden pt-16 pb-20 lg:pt-24 lg:pb-28">
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-gradient-to-b from-amber-50/50 to-transparent -z-10"></div>
      
      <div class="container mx-auto px-4 relative">
        <!-- Logo & Title -->
        <div class="max-w-3xl mx-auto text-center mb-12">
          <div class="inline-flex items-center justify-center p-1.5 mb-6 rounded-2xl bg-amber-100/50 text-amber-700 text-sm font-bold tracking-wide uppercase">
            <span class="px-3 py-1 bg-white rounded-xl shadow-sm">Serendipity</span>
            <span class="px-3">经销商订货平台</span>
          </div>
          <h1 class="text-4xl md:text-6xl font-black text-slate-900 mb-6 tracking-tight">
            欢迎来到<span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 to-orange-600">欣与甜</span>
          </h1>
          <p class="text-lg text-slate-600 max-w-xl mx-auto">
            优质食品，专业配送，为您的事业保驾护航。
          </p>
          
          <div v-if="isLoggedIn" class="mt-8 inline-flex items-center gap-3 px-6 py-4 bg-white/80 backdrop-blur rounded-2xl shadow-lg shadow-slate-200/60 border border-slate-100">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
            </div>
            <div class="text-left">
              <p v-if="isAdmin" class="text-sm text-slate-500">您好，管理员</p>
              <p v-else class="text-sm text-slate-500">欢迎回来</p>
              <p class="font-semibold text-slate-900">{{ companyName || username }}</p>
            </div>
          </div>
        </div>

        <!-- CTA Buttons -->
        <div class="flex flex-wrap justify-center gap-4 mt-8">
          <template v-if="!isLoggedIn">
            <router-link 
              to="/login" 
              class="px-8 py-4 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 active:scale-95 transition-all duration-200 shadow-lg shadow-slate-900/20"
            >
              登录
            </router-link>
            <router-link 
              to="/products" 
              class="px-8 py-4 bg-white text-slate-700 font-bold rounded-xl border-2 border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all duration-200"
            >
              浏览产品
            </router-link>
          </template>
          <template v-else-if="isAdmin">
            <router-link 
              to="/admin" 
              class="px-8 py-4 bg-gradient-to-r from-amber-400 to-orange-500 text-slate-900 font-bold rounded-xl hover:from-amber-500 hover:to-orange-600 active:scale-95 transition-all duration-200 shadow-lg shadow-orange-200/50"
            >
              进入管理后台
            </router-link>
            <router-link 
              to="/products" 
              class="px-8 py-4 bg-white text-slate-700 font-bold rounded-xl border-2 border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all duration-200"
            >
              浏览产品
            </router-link>
          </template>
          <template v-else>
            <router-link 
              to="/products" 
              class="px-8 py-4 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 active:scale-95 transition-all duration-200 shadow-lg shadow-slate-900/20"
            >
              开始选购
            </router-link>
            <router-link 
              to="/orders" 
              class="px-8 py-4 bg-white text-slate-700 font-bold rounded-xl border-2 border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all duration-200"
            >
              查看订单
            </router-link>
          </template>
        </div>
      </div>
    </section>
    
    <!-- Features Section -->
    <section class="py-16 bg-slate-50/50 border-t border-slate-100">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-center gap-4 mb-10">
            <div class="h-px flex-1 bg-slate-200"></div>
            <h2 class="text-sm font-bold text-slate-400 uppercase tracking-[0.2em]">为什么选择我们</h2>
            <div class="h-px flex-1 bg-slate-200"></div>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="group p-6 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 hover:shadow-xl hover:shadow-slate-200/50 hover:-translate-y-1 transition-all duration-300">
              <div class="w-14 h-14 mb-4 rounded-xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center text-3xl">
                🍞
              </div>
              <h3 class="text-lg font-bold text-slate-900 mb-2">优质产品</h3>
              <p class="text-sm text-slate-500 leading-relaxed">精选优质原料，严格品质把控，为您提供放心的食品</p>
            </div>
            
            <div class="group p-6 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 hover:shadow-xl hover:shadow-slate-200/50 hover:-translate-y-1 transition-all duration-300">
              <div class="w-14 h-14 mb-4 rounded-xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center text-3xl">
                🚚
              </div>
              <h3 class="text-lg font-bold text-slate-900 mb-2">快速配送</h3>
              <p class="text-sm text-slate-500 leading-relaxed">专业物流团队，确保产品新鲜送达</p>
            </div>
            
            <div class="group p-6 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 hover:shadow-xl hover:shadow-slate-200/50 hover:-translate-y-1 transition-all duration-300">
              <div class="w-14 h-14 mb-4 rounded-xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center text-3xl">
                💰
              </div>
              <h3 class="text-lg font-bold text-slate-900 mb-2">优惠价格</h3>
              <p class="text-sm text-slate-500 leading-relaxed">经销商专享批发价格，合作共赢</p>
            </div>
            
            <div class="group p-6 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 hover:shadow-xl hover:shadow-slate-200/50 hover:-translate-y-1 transition-all duration-300">
              <div class="w-14 h-14 mb-4 rounded-xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center text-3xl">
                📱
              </div>
              <h3 class="text-lg font-bold text-slate-900 mb-2">便捷订货</h3>
              <p class="text-sm text-slate-500 leading-relaxed">在线下单，随时查询订单状态</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
