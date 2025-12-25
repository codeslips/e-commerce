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

const statusColors: Record<string, string> = {
  pending: '#f59e0b',
  confirmed: '#3b82f6',
  shipped: '#8b5cf6',
  delivered: '#10b981',
  cancelled: '#ef4444',
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
  <div class="orders-page">
    <div class="page-header">
      <h1>我的订单</h1>
      <p>查看和管理您的订单</p>
    </div>
    
    <div class="filters">
      <select v-model="statusFilter" @change="handleStatusChange">
        <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
    </div>
    
    <div v-if="loading" class="loading">
      加载中...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else-if="orders.length === 0" class="empty">
      <div class="empty-icon">📦</div>
      <p>暂无订单</p>
      <router-link to="/products" class="browse-btn">去选购</router-link>
    </div>
    
    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <div class="order-no">
            <span class="label">订单号</span>
            <span class="value">{{ order.order_no }}</span>
          </div>
          <div
            class="order-status"
            :style="{ backgroundColor: statusColors[order.status] + '20', color: statusColors[order.status] }"
          >
            {{ statusLabels[order.status] }}
          </div>
        </div>
        
        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <span class="item-name">{{ item.product_name }}</span>
            <span class="item-qty">× {{ item.quantity }}</span>
            <span class="item-price">{{ formatPrice(item.subtotal) }}</span>
          </div>
        </div>
        
        <div class="order-footer">
          <div class="order-info">
            <p class="order-date">{{ formatDate(order.created_at) }}</p>
            <p class="order-address">配送至: {{ order.shipping_address }}</p>
          </div>
          <div class="order-total">
            <span class="label">合计</span>
            <span class="amount">{{ formatPrice(order.total_amount) }}</span>
          </div>
        </div>
        
        <div v-if="order.status === 'pending'" class="order-actions">
          <button class="cancel-btn" @click="cancelOrder(order.id)">
            取消订单
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="totalPages > 1" class="pagination">
      <button
        :disabled="currentPage === 1"
        @click="fetchOrders(currentPage - 1)"
      >
        上一页
      </button>
      <span class="page-info">
        第 {{ currentPage }} / {{ totalPages }} 页
      </span>
      <button
        :disabled="currentPage === totalPages"
        @click="fetchOrders(currentPage + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<style scoped>
.orders-page {
  padding: 1rem 0;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.75rem;
  color: #1a1a2e;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #64748b;
}

.filters {
  margin-bottom: 1.5rem;
}

.filters select {
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  min-width: 150px;
  cursor: pointer;
}

.filters select:focus {
  outline: none;
  border-color: #0f3460;
}

.loading, .error, .empty {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.error {
  color: #dc2626;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.browse-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  background: #0f3460;
  color: white;
  text-decoration: none;
  border-radius: 8px;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.order-no .label {
  font-size: 0.75rem;
  color: #64748b;
  margin-right: 0.5rem;
}

.order-no .value {
  font-weight: 600;
  color: #1a1a2e;
}

.order-status {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.order-items {
  margin-bottom: 1rem;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  font-size: 0.95rem;
}

.item-name {
  flex: 1;
  color: #374151;
}

.item-qty {
  color: #64748b;
  margin: 0 1rem;
}

.item-price {
  font-weight: 500;
  color: #1a1a2e;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.order-date {
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.order-address {
  font-size: 0.8rem;
  color: #64748b;
}

.order-total {
  text-align: right;
}

.order-total .label {
  font-size: 0.75rem;
  color: #64748b;
}

.order-total .amount {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  color: #dc2626;
}

.order-actions {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
}

.cancel-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #dc2626;
  color: #dc2626;
  background: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.cancel-btn:hover {
  background: #dc2626;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  border: 2px solid #0f3460;
  border-radius: 8px;
  background: white;
  color: #0f3460;
  cursor: pointer;
}

.pagination button:hover:not(:disabled) {
  background: #0f3460;
  color: white;
}

.pagination button:disabled {
  border-color: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
}

.page-info {
  color: #64748b;
  font-size: 0.875rem;
}
</style>
