<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ordersApi } from '@/api'
import type { Order, PaginatedResponse } from '@/api'

const orders = ref<Order[]>([])
const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const statusFilter = ref('')

const statusOptions = [
  { value: '', label: '全部' },
  { value: 'pending', label: '待确认' },
  { value: 'confirmed', label: '已确认' },
  { value: 'shipped', label: '已发货' },
  { value: 'delivered', label: '已送达' },
  { value: 'cancelled', label: '已取消' },
]

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

async function fetchOrders(page = 1) {
  loading.value = true
  error.value = ''
  
  try {
    const response: PaginatedResponse<Order> = await ordersApi.list({
      page,
      status: statusFilter.value || undefined,
    })
    orders.value = response.items
    currentPage.value = response.page
    totalPages.value = response.pages
  } catch (e: any) {
    error.value = e.response?.data?.detail || '加载订单失败'
  } finally {
    loading.value = false
  }
}

async function handleStatusChange() {
  currentPage.value = 1
  await fetchOrders(1)
}

async function cancelOrder(orderId: string) {
  if (!confirm('确定要取消这个订单吗？')) return
  
  try {
    await ordersApi.cancel(orderId)
    await fetchOrders(currentPage.value)
  } catch (e: any) {
    alert(e.response?.data?.detail || '取消订单失败')
  }
}

function formatPrice(price: number | string) {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return `¥${numPrice.toFixed(2)}`
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => fetchOrders())
</script>

<template>
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-4xl">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">我的订单</h1>
        <p class="text-slate-500">查看和管理您的订单</p>
      </div>
      
      <!-- Filters -->
      <div class="mb-6">
        <select 
          v-model="statusFilter" 
          @change="handleStatusChange"
          class="px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-700 font-medium min-w-[150px] cursor-pointer focus:border-amber-500 focus:ring-0 transition-all duration-200"
        >
          <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
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
      
      <!-- Empty State -->
      <div v-else-if="orders.length === 0" class="text-center py-16 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100">
        <div class="text-6xl mb-4">📦</div>
        <p class="text-slate-500 font-medium mb-6">暂无订单</p>
        <router-link 
          to="/products" 
          class="inline-block px-8 py-3 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 transition-all duration-200"
        >
          去选购
        </router-link>
      </div>
      
      <!-- Orders List -->
      <div v-else class="space-y-4">
        <div 
          v-for="order in orders" 
          :key="order.id" 
          class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 overflow-hidden"
        >
          <!-- Order Header -->
          <div class="flex justify-between items-center px-6 py-4 border-b border-slate-100 bg-slate-50/50">
            <div>
              <span class="text-xs text-slate-400 font-medium">订单号</span>
              <p class="font-semibold text-slate-900">{{ order.order_no }}</p>
            </div>
            <span 
              class="px-3 py-1.5 rounded-full text-xs font-semibold"
              :class="[statusColors[order.status]?.bg, statusColors[order.status]?.text]"
            >
              {{ statusLabels[order.status] }}
            </span>
          </div>
          
          <!-- Order Items -->
          <div class="px-6 py-4 divide-y divide-slate-100">
            <div 
              v-for="item in order.items" 
              :key="item.id" 
              class="flex justify-between items-center py-3 first:pt-0 last:pb-0"
            >
              <span class="text-slate-700">{{ item.product_name }}</span>
              <div class="flex items-center gap-4">
                <span class="text-slate-400">× {{ item.quantity }}</span>
                <span class="font-medium text-slate-900 min-w-[80px] text-right">{{ formatPrice(item.subtotal) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Order Footer -->
          <div class="flex justify-between items-end px-6 py-4 border-t border-slate-100 bg-slate-50/30">
            <div>
              <p class="text-xs text-slate-400 mb-1">{{ formatDate(order.created_at) }}</p>
              <p class="text-sm text-slate-500">配送至: {{ order.shipping_address }}</p>
            </div>
            <div class="text-right">
              <span class="text-xs text-slate-400">合计</span>
              <p class="text-xl font-bold text-orange-500">{{ formatPrice(order.total_amount) }}</p>
            </div>
          </div>
          
          <!-- Order Actions -->
          <div v-if="order.status === 'pending'" class="px-6 py-4 border-t border-slate-100 flex justify-end">
            <button 
              class="px-4 py-2 border-2 border-red-200 text-red-500 font-medium rounded-xl hover:bg-red-500 hover:text-white hover:border-red-500 transition-all duration-200"
              @click="cancelOrder(order.id)"
            >
              取消订单
            </button>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 mt-10">
        <button
          :disabled="currentPage === 1"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="fetchOrders(currentPage - 1)"
        >
          上一页
        </button>
        <span class="text-slate-500 text-sm">
          第 {{ currentPage }} / {{ totalPages }} 页
        </span>
        <button
          :disabled="currentPage === totalPages"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="fetchOrders(currentPage + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>
