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
const searchQuery = ref('')

const statusOptions = [
  { value: '', label: '全部状态' },
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

// Detail modal
const showDetail = ref(false)
const selectedOrder = ref<Order | null>(null)

async function fetchOrders(page = 1) {
  loading.value = true
  error.value = ''
  
  try {
    const response: PaginatedResponse<Order> = await ordersApi.list({
      page,
      status: statusFilter.value || undefined,
      order_no: searchQuery.value || undefined,
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

async function handleFilterChange() {
  currentPage.value = 1
  await fetchOrders(1)
}

async function viewOrder(order: Order) {
  try {
    selectedOrder.value = await ordersApi.get(order.id)
    showDetail.value = true
  } catch (e: any) {
    alert(e.response?.data?.detail || '加载订单详情失败')
  }
}

async function updateStatus(orderId: string, newStatus: string) {
  try {
    await ordersApi.updateStatus(orderId, newStatus)
    await fetchOrders(currentPage.value)
    if (selectedOrder.value?.id === orderId) {
      selectedOrder.value = await ordersApi.get(orderId)
    }
  } catch (e: any) {
    alert(e.response?.data?.detail || '更新状态失败')
  }
}

function closeDetail() {
  showDetail.value = false
  selectedOrder.value = null
}

function formatPrice(price: number | string) {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return `¥${numPrice.toFixed(2)}`
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function getNextStatus(currentStatus: string): string | null {
  const flow: Record<string, string> = {
    pending: 'confirmed',
    confirmed: 'shipped',
    shipped: 'delivered',
  }
  return flow[currentStatus] || null
}

function getNextStatusLabel(currentStatus: string): string | null {
  const nextStatus = getNextStatus(currentStatus)
  return nextStatus ? statusLabels[nextStatus] : null
}

onMounted(() => fetchOrders())
</script>

<template>
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">订单管理</h1>
        <p class="text-slate-500">管理所有订单</p>
      </div>
      
      <!-- Toolbar -->
      <div class="flex flex-wrap gap-4 mb-6">
        <div class="flex gap-3">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索订单号..."
            class="px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 placeholder-slate-400 focus:border-amber-500 focus:ring-0 transition-all duration-200 min-w-[200px]"
            @keyup.enter="handleFilterChange"
          />
          <button 
            class="px-6 py-3 bg-slate-900 text-white font-medium rounded-xl hover:bg-slate-800 transition-all duration-200"
            @click="handleFilterChange"
          >
            搜索
          </button>
        </div>
        
        <select 
          v-model="statusFilter" 
          @change="handleFilterChange"
          class="px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-700 cursor-pointer focus:border-amber-500 focus:ring-0 transition-all duration-200"
        >
          <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>
      
      <!-- Loading / Error -->
      <div v-if="loading" class="text-center py-16 text-slate-500">加载中...</div>
      <div v-else-if="error" class="text-center py-16 text-red-500">{{ error }}</div>
      
      <!-- Orders Table -->
      <div v-else class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 overflow-hidden">
        <table class="w-full">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-100">
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">订单号</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">经销商</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">金额</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">状态</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">下单时间</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="order in orders" :key="order.id" class="hover:bg-slate-50/50">
              <td class="px-6 py-4">
                <span 
                  class="text-amber-600 font-medium cursor-pointer hover:underline"
                  @click="viewOrder(order)"
                >
                  {{ order.order_no }}
                </span>
              </td>
              <td class="px-6 py-4 text-slate-600">{{ order.dealer_company }}</td>
              <td class="px-6 py-4 font-bold text-orange-500">{{ formatPrice(order.total_amount) }}</td>
              <td class="px-6 py-4">
                <span 
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                  :class="[statusColors[order.status]?.bg, statusColors[order.status]?.text]"
                >
                  {{ statusLabels[order.status] }}
                </span>
              </td>
              <td class="px-6 py-4 text-slate-400 text-sm">{{ formatDate(order.created_at) }}</td>
              <td class="px-6 py-4">
                <div class="flex gap-2">
                  <button 
                    class="px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors duration-200"
                    @click="viewOrder(order)"
                  >
                    查看
                  </button>
                  <button
                    v-if="getNextStatus(order.status)"
                    class="px-3 py-1.5 text-sm font-medium text-emerald-600 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors duration-200"
                    @click="updateStatus(order.id, getNextStatus(order.status)!)"
                  >
                    {{ getNextStatusLabel(order.status) }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 mt-8">
        <button
          :disabled="currentPage === 1"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="fetchOrders(currentPage - 1)"
        >
          上一页
        </button>
        <span class="text-slate-500 text-sm">第 {{ currentPage }} / {{ totalPages }} 页</span>
        <button
          :disabled="currentPage === totalPages"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="fetchOrders(currentPage + 1)"
        >
          下一页
        </button>
      </div>
      
      <!-- Order Detail Modal -->
      <div v-if="showDetail && selectedOrder" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeDetail">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <!-- Modal Header -->
          <div class="flex justify-between items-center px-6 py-5 border-b border-slate-100">
            <h2 class="text-xl font-bold text-slate-900">订单详情</h2>
            <button class="text-slate-400 hover:text-slate-600 text-2xl" @click="closeDetail">×</button>
          </div>
          
          <!-- Modal Body -->
          <div class="p-6">
            <!-- Order Info -->
            <div class="space-y-3 mb-6">
              <div class="flex py-2 border-b border-slate-100">
                <span class="w-24 text-slate-400 text-sm">订单号</span>
                <span class="flex-1 font-medium text-slate-900">{{ selectedOrder.order_no }}</span>
              </div>
              <div class="flex items-center py-2 border-b border-slate-100">
                <span class="w-24 text-slate-400 text-sm">状态</span>
                <span 
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                  :class="[statusColors[selectedOrder.status]?.bg, statusColors[selectedOrder.status]?.text]"
                >
                  {{ statusLabels[selectedOrder.status] }}
                </span>
              </div>
              <div class="flex py-2 border-b border-slate-100">
                <span class="w-24 text-slate-400 text-sm">经销商</span>
                <span class="flex-1 text-slate-900">{{ selectedOrder.dealer_company }}</span>
              </div>
              <div class="flex py-2 border-b border-slate-100">
                <span class="w-24 text-slate-400 text-sm">配送地址</span>
                <span class="flex-1 text-slate-900">{{ selectedOrder.shipping_address }}</span>
              </div>
              <div v-if="selectedOrder.notes" class="flex py-2 border-b border-slate-100">
                <span class="w-24 text-slate-400 text-sm">备注</span>
                <span class="flex-1 text-slate-900">{{ selectedOrder.notes }}</span>
              </div>
              <div class="flex py-2">
                <span class="w-24 text-slate-400 text-sm">下单时间</span>
                <span class="flex-1 text-slate-900">{{ formatDate(selectedOrder.created_at) }}</span>
              </div>
            </div>
            
            <!-- Items -->
            <h3 class="text-lg font-bold text-slate-900 mb-4">商品明细</h3>
            <div class="bg-slate-50 rounded-xl p-4 mb-6">
              <div 
                v-for="item in selectedOrder.items" 
                :key="item.id" 
                class="flex justify-between items-center py-3 border-b border-slate-200 last:border-0"
              >
                <span class="text-slate-700">{{ item.product_name }}</span>
                <div class="flex items-center gap-4 text-sm">
                  <span class="text-slate-400">× {{ item.quantity }}</span>
                  <span class="text-slate-400">{{ formatPrice(item.unit_price) }}</span>
                  <span class="font-medium text-slate-900 min-w-[80px] text-right">{{ formatPrice(item.subtotal) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Total -->
            <div class="flex justify-between items-center p-4 bg-slate-900 rounded-xl text-white mb-6">
              <span>总计</span>
              <span class="text-xl font-bold">{{ formatPrice(selectedOrder.total_amount) }}</span>
            </div>
            
            <!-- Actions -->
            <div v-if="getNextStatus(selectedOrder.status)">
              <button
                class="w-full py-4 bg-emerald-500 text-white font-bold rounded-xl hover:bg-emerald-600 transition-all duration-200"
                @click="updateStatus(selectedOrder.id, getNextStatus(selectedOrder.status)!)"
              >
                标记为: {{ getNextStatusLabel(selectedOrder.status) }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
