<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ordersApi } from '@/api'
import type { OrderStats } from '@/api'

const stats = ref<OrderStats | null>(null)
const loading = ref(true)
const error = ref('')

const statusLabels: Record<string, string> = {
  pending: '待确认',
  confirmed: '已确认',
  shipped: '已发货',
  delivered: '已送达',
  cancelled: '已取消',
}

const statusColors: Record<string, { bg: string, text: string }> = {
  pending: { bg: 'bg-amber-100', text: 'text-amber-700' },
  confirmed: { bg: 'bg-blue-100', text: 'text-blue-700' },
  shipped: { bg: 'bg-purple-100', text: 'text-purple-700' },
  delivered: { bg: 'bg-emerald-100', text: 'text-emerald-700' },
  cancelled: { bg: 'bg-red-100', text: 'text-red-700' },
}

async function fetchStats() {
  loading.value = true
  error.value = ''
  
  try {
    stats.value = await ordersApi.getStats()
  } catch (e: any) {
    error.value = e.response?.data?.detail || '加载数据失败'
  } finally {
    loading.value = false
  }
}

function formatPrice(price: number | string) {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return `¥${numPrice.toFixed(2)}`
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(fetchStats)
</script>

<template>
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">管理后台</h1>
        <p class="text-slate-500">欢迎回来，管理员</p>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-flex items-center gap-3 text-slate-500">
          <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>加载中...</span>
        </div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-500 font-medium">{{ error }}</p>
      </div>
      
      <template v-else-if="stats">
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-5 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center text-2xl">
              📦
            </div>
            <div>
              <p class="text-sm text-slate-400 mb-0.5">今日订单</p>
              <p class="text-2xl font-bold text-slate-900">{{ stats.today_orders }}</p>
            </div>
          </div>
          
          <div class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-5 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-emerald-100 to-teal-100 flex items-center justify-center text-2xl">
              💰
            </div>
            <div>
              <p class="text-sm text-slate-400 mb-0.5">总营收</p>
              <p class="text-2xl font-bold text-slate-900">{{ formatPrice(stats.total_revenue) }}</p>
            </div>
          </div>
          
          <div class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-5 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-amber-100 to-yellow-100 flex items-center justify-center text-2xl">
              ⏳
            </div>
            <div>
              <p class="text-sm text-slate-400 mb-0.5">待处理订单</p>
              <p class="text-2xl font-bold text-slate-900">{{ stats.status_counts.pending || 0 }}</p>
            </div>
          </div>
          
          <div class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-5 flex items-center gap-4">
            <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-emerald-100 to-green-100 flex items-center justify-center text-2xl">
              ✅
            </div>
            <div>
              <p class="text-sm text-slate-400 mb-0.5">已完成订单</p>
              <p class="text-2xl font-bold text-slate-900">{{ stats.status_counts.delivered || 0 }}</p>
            </div>
          </div>
        </div>
        
        <!-- Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-8">
          <!-- Status Distribution -->
          <div class="lg:col-span-2 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-6">
            <h2 class="text-lg font-bold text-slate-900 mb-5">订单状态分布</h2>
            <div class="space-y-3">
              <div
                v-for="(count, status) in stats.status_counts"
                :key="status"
                class="flex justify-between items-center p-3 bg-slate-50 rounded-xl"
              >
                <span 
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                  :class="[statusColors[status as string]?.bg, statusColors[status as string]?.text]"
                >
                  {{ statusLabels[status as string] || status }}
                </span>
                <span class="font-bold text-slate-900">{{ count }}</span>
              </div>
            </div>
          </div>
          
          <!-- Recent Orders -->
          <div class="lg:col-span-3 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-6">
            <div class="flex justify-between items-center mb-5">
              <h2 class="text-lg font-bold text-slate-900">最近订单</h2>
              <router-link to="/admin/orders" class="text-sm text-amber-600 font-medium hover:text-amber-700">
                查看全部
              </router-link>
            </div>
            <div class="space-y-3">
              <div
                v-for="order in stats.recent_orders"
                :key="order.id"
                class="p-4 bg-slate-50 rounded-xl"
              >
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <p class="font-semibold text-slate-900 text-sm">{{ order.order_no }}</p>
                    <p class="text-xs text-slate-400">{{ order.dealer_company }}</p>
                  </div>
                  <span 
                    class="px-2.5 py-1 rounded-full text-[10px] font-semibold"
                    :class="[statusColors[order.status]?.bg, statusColors[order.status]?.text]"
                  >
                    {{ statusLabels[order.status] }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-xs text-slate-400">{{ formatDate(order.created_at) }}</span>
                  <span class="font-bold text-orange-500">{{ formatPrice(order.total_amount) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Quick Links -->
        <div class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-6">
          <h2 class="text-lg font-bold text-slate-900 mb-5">快捷入口</h2>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <router-link 
              to="/admin/products" 
              class="group flex flex-col items-center p-5 bg-slate-50 rounded-xl hover:bg-slate-900 transition-all duration-200"
            >
              <span class="text-3xl mb-2">📦</span>
              <span class="text-sm font-medium text-slate-700 group-hover:text-white">产品管理</span>
            </router-link>
            <router-link 
              to="/admin/orders" 
              class="group flex flex-col items-center p-5 bg-slate-50 rounded-xl hover:bg-slate-900 transition-all duration-200"
            >
              <span class="text-3xl mb-2">📋</span>
              <span class="text-sm font-medium text-slate-700 group-hover:text-white">订单管理</span>
            </router-link>
            <router-link 
              to="/admin/dealers" 
              class="group flex flex-col items-center p-5 bg-slate-50 rounded-xl hover:bg-slate-900 transition-all duration-200"
            >
              <span class="text-3xl mb-2">👥</span>
              <span class="text-sm font-medium text-slate-700 group-hover:text-white">经销商管理</span>
            </router-link>
            <router-link 
              to="/products" 
              class="group flex flex-col items-center p-5 bg-slate-50 rounded-xl hover:bg-slate-900 transition-all duration-200"
            >
              <span class="text-3xl mb-2">🛒</span>
              <span class="text-sm font-medium text-slate-700 group-hover:text-white">产品目录</span>
            </router-link>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
