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

const statusColors: Record<string, string> = {
  pending: '#f59e0b',
  confirmed: '#3b82f6',
  shipped: '#8b5cf6',
  delivered: '#10b981',
  cancelled: '#ef4444',
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

function formatPrice(price: number) {
  return `¥${price.toFixed(2)}`
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
  <div class="admin-orders">
    <div class="page-header">
      <h1>订单管理</h1>
      <p>管理所有订单</p>
    </div>
    
    <div class="toolbar">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索订单号..."
          @keyup.enter="handleFilterChange"
        />
        <button @click="handleFilterChange">搜索</button>
      </div>
      
      <select v-model="statusFilter" @change="handleFilterChange">
        <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="orders-table">
      <table>
        <thead>
          <tr>
            <th>订单号</th>
            <th>经销商</th>
            <th>金额</th>
            <th>状态</th>
            <th>下单时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td>
              <span class="order-no" @click="viewOrder(order)">
                {{ order.order_no }}
              </span>
            </td>
            <td>{{ order.dealer_company }}</td>
            <td class="amount">{{ formatPrice(order.total_amount) }}</td>
            <td>
              <span
                class="status-badge"
                :style="{ backgroundColor: statusColors[order.status] + '20', color: statusColors[order.status] }"
              >
                {{ statusLabels[order.status] }}
              </span>
            </td>
            <td class="date">{{ formatDate(order.created_at) }}</td>
            <td>
              <div class="actions">
                <button class="view-btn" @click="viewOrder(order)">
                  查看
                </button>
                <button
                  v-if="getNextStatus(order.status)"
                  class="status-btn"
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
    
    <div v-if="totalPages > 1" class="pagination">
      <button
        :disabled="currentPage === 1"
        @click="fetchOrders(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button
        :disabled="currentPage === totalPages"
        @click="fetchOrders(currentPage + 1)"
      >
        下一页
      </button>
    </div>
    
    <!-- Order Detail Modal -->
    <div v-if="showDetail && selectedOrder" class="modal-overlay" @click.self="closeDetail">
      <div class="modal">
        <div class="modal-header">
          <h2>订单详情</h2>
          <button class="close-btn" @click="closeDetail">×</button>
        </div>
        
        <div class="modal-body">
          <div class="order-info">
            <div class="info-row">
              <span class="label">订单号</span>
              <span class="value">{{ selectedOrder.order_no }}</span>
            </div>
            <div class="info-row">
              <span class="label">状态</span>
              <span
                class="status-badge"
                :style="{ backgroundColor: statusColors[selectedOrder.status] + '20', color: statusColors[selectedOrder.status] }"
              >
                {{ statusLabels[selectedOrder.status] }}
              </span>
            </div>
            <div class="info-row">
              <span class="label">经销商</span>
              <span class="value">{{ selectedOrder.dealer_company }}</span>
            </div>
            <div class="info-row">
              <span class="label">配送地址</span>
              <span class="value">{{ selectedOrder.shipping_address }}</span>
            </div>
            <div v-if="selectedOrder.notes" class="info-row">
              <span class="label">备注</span>
              <span class="value">{{ selectedOrder.notes }}</span>
            </div>
            <div class="info-row">
              <span class="label">下单时间</span>
              <span class="value">{{ formatDate(selectedOrder.created_at) }}</span>
            </div>
          </div>
          
          <h3>商品明细</h3>
          <div class="items-list">
            <div v-for="item in selectedOrder.items" :key="item.id" class="item-row">
              <span class="item-name">{{ item.product_name }}</span>
              <span class="item-qty">× {{ item.quantity }}</span>
              <span class="item-price">{{ formatPrice(item.unit_price) }}</span>
              <span class="item-subtotal">{{ formatPrice(item.subtotal) }}</span>
            </div>
          </div>
          
          <div class="order-total">
            <span>总计</span>
            <span class="total-amount">{{ formatPrice(selectedOrder.total_amount) }}</span>
          </div>
          
          <div v-if="getNextStatus(selectedOrder.status)" class="modal-actions">
            <button
              class="action-btn"
              @click="updateStatus(selectedOrder.id, getNextStatus(selectedOrder.status)!)"
            >
              标记为: {{ getNextStatusLabel(selectedOrder.status) }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-orders {
  padding: 1rem 0;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  font-size: 1.75rem;
  color: #1a1a2e;
  margin-bottom: 0.25rem;
}

.page-header p {
  color: #64748b;
}

.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.search-box input {
  padding: 0.625rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  min-width: 200px;
}

.search-box input:focus {
  outline: none;
  border-color: #0f3460;
}

.search-box button {
  padding: 0.625rem 1rem;
  background: #0f3460;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.toolbar select {
  padding: 0.625rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.error {
  color: #dc2626;
}

.orders-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #f3f4f6;
}

th {
  background: #f8fafc;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.order-no {
  color: #0f3460;
  font-weight: 500;
  cursor: pointer;
}

.order-no:hover {
  text-decoration: underline;
}

.amount {
  font-weight: 600;
  color: #dc2626;
}

.date {
  color: #64748b;
  font-size: 0.875rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.view-btn, .status-btn {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
}

.view-btn {
  background: #e0f2fe;
  color: #0369a1;
  border: none;
}

.view-btn:hover {
  background: #bae6fd;
}

.status-btn {
  background: #dcfce7;
  color: #16a34a;
  border: none;
}

.status-btn:hover {
  background: #bbf7d0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
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

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  font-size: 1.25rem;
  color: #1a1a2e;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.order-info {
  margin-bottom: 1.5rem;
}

.info-row {
  display: flex;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.info-row .label {
  width: 100px;
  color: #64748b;
  font-size: 0.875rem;
}

.info-row .value {
  flex: 1;
  color: #1a1a2e;
}

.modal-body h3 {
  font-size: 1rem;
  color: #1a1a2e;
  margin-bottom: 1rem;
}

.items-list {
  background: #f8fafc;
  border-radius: 8px;
  padding: 0.5rem;
}

.item-row {
  display: grid;
  grid-template-columns: 1fr auto auto auto;
  gap: 1rem;
  padding: 0.75rem;
  border-bottom: 1px solid #e5e7eb;
}

.item-row:last-child {
  border-bottom: none;
}

.item-name {
  color: #374151;
}

.item-qty {
  color: #64748b;
}

.item-price {
  color: #64748b;
}

.item-subtotal {
  font-weight: 500;
  color: #1a1a2e;
}

.order-total {
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  margin-top: 1rem;
  background: #1a1a2e;
  border-radius: 8px;
  color: white;
}

.total-amount {
  font-size: 1.25rem;
  font-weight: 700;
}

.modal-actions {
  margin-top: 1.5rem;
}

.action-btn {
  width: 100%;
  padding: 0.875rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1rem;
}

.action-btn:hover {
  background: #059669;
}
</style>

