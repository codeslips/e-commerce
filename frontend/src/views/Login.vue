<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

interface DemoAccount {
  username: string
  password: string
  role: string
  label: string
  description: string
}

const demoAccounts: DemoAccount[] = [
  {
    username: 'admin',
    password: 'admin123',
    role: 'admin',
    label: '管理员',
    description: '管理后台完整权限'
  },
  {
    username: 'dealer001',
    password: 'dealer123',
    role: 'dealer',
    label: '经销商(已审核)',
    description: '广州好味道食品店'
  },
  {
    username: 'dealer004',
    password: 'dealer123',
    role: 'dealer-pending',
    label: '经销商(待审核)',
    description: '东莞小食铺'
  }
]

function selectDemoAccount(account: DemoAccount) {
  username.value = account.username
  password.value = account.password
}

async function handleSubmit() {
  error.value = ''
  loading.value = true
  
  try {
    await authStore.login({ username: username.value, password: password.value })
    
    // Redirect based on role
    if (authStore.isAdmin) {
      router.push('/admin')
    } else {
      router.push('/products')
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-4">
    <div class="w-full max-w-md">
      <div class="bg-white/95 backdrop-blur rounded-2xl shadow-2xl shadow-slate-900/50 p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 mb-4 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 shadow-lg shadow-orange-200/50">
            <span class="text-white font-black text-xl">XT</span>
          </div>
          <h1 class="text-2xl font-bold text-slate-900 mb-1">欣与甜</h1>
          <p class="text-slate-500 text-sm">经销商订货平台</p>
        </div>
        
        <!-- Login Form -->
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div>
            <label for="username" class="block text-sm font-medium text-slate-700 mb-2">用户名</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="请输入用户名"
              required
              :disabled="loading"
              class="block w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 bg-slate-50 text-slate-900 placeholder-slate-400 focus:border-amber-500 focus:ring-0 focus:bg-white transition-all duration-200 disabled:bg-slate-100 disabled:cursor-not-allowed"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-slate-700 mb-2">密码</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="请输入密码"
              required
              :disabled="loading"
              class="block w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 bg-slate-50 text-slate-900 placeholder-slate-400 focus:border-amber-500 focus:ring-0 focus:bg-white transition-all duration-200 disabled:bg-slate-100 disabled:cursor-not-allowed"
            />
          </div>
          
          <div v-if="error" class="p-4 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
            {{ error }}
          </div>
          
          <button 
            type="submit" 
            class="w-full py-4 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 active:scale-[0.98] transition-all duration-200 shadow-lg shadow-slate-900/20 disabled:opacity-60 disabled:cursor-not-allowed"
            :disabled="loading"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        
        <!-- Demo Accounts -->
        <div class="mt-8 pt-6 border-t border-slate-100">
          <div class="flex items-center gap-2 mb-4 text-slate-500 text-sm font-medium">
            <span class="text-amber-500">✨</span>
            <span>Demo 账号 (点击自动填充)</span>
          </div>
          <div class="space-y-2">
            <button
              v-for="account in demoAccounts"
              :key="account.username"
              type="button"
              class="w-full flex items-center gap-3 p-3.5 bg-slate-50 border-2 border-slate-100 rounded-xl cursor-pointer transition-all duration-200 hover:bg-slate-100 hover:border-slate-200 hover:translate-x-1 text-left"
              :class="{ 'bg-amber-50 border-amber-200': username === account.username }"
              @click="selectDemoAccount(account)"
            >
              <span 
                class="px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider text-white"
                :class="{
                  'bg-gradient-to-r from-purple-500 to-purple-600': account.role === 'admin',
                  'bg-gradient-to-r from-emerald-500 to-emerald-600': account.role === 'dealer',
                  'bg-gradient-to-r from-amber-500 to-amber-600': account.role === 'dealer-pending'
                }"
              >
                {{ account.label }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-slate-800">{{ account.username }}</p>
                <p class="text-xs text-slate-500 truncate">{{ account.description }}</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
