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

const statusColors: Record<string, string> = {
  pending: '#f59e0b',
  confirmed: '#3b82f6',
  shipped: '#8b5cf6',
  delivered: '#10b981',
  cancelled: '#ef4444',
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
  <div class="dashboard-page">
    <div class="page-header">
      <h1>管理后台</h1>
      <p>欢迎回来，管理员</p>
    </div>
    
    <div v-if="loading" class="loading">
      加载中...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <template v-else-if="stats">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <div class="stat-info">
            <p class="stat-label">今日订单</p>
            <p class="stat-value">{{ stats.today_orders }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <p class="stat-label">总营收</p>
            <p class="stat-value">{{ formatPrice(stats.total_revenue) }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <p class="stat-label">待处理订单</p>
            <p class="stat-value">{{ stats.status_counts.pending || 0 }}</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <p class="stat-label">已完成订单</p>
            <p class="stat-value">{{ stats.status_counts.delivered || 0 }}</p>
          </div>
        </div>
      </div>
      
      <div class="content-grid">
        <div class="section-card">
          <h2>订单状态分布</h2>
          <div class="status-list">
            <div
              v-for="(count, status) in stats.status_counts"
              :key="status"
              class="status-item"
            >
              <div class="status-bar">
                <span
                  class="status-badge"
                  :style="{ backgroundColor: statusColors[status] + '20', color: statusColors[status] }"
                >
                  {{ statusLabels[status] || status }}
                </span>
                <span class="status-count">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="section-card">
          <div class="section-header">
            <h2>最近订单</h2>
            <router-link to="/admin/orders" class="view-all">查看全部</router-link>
          </div>
          
          <div class="recent-orders">
            <div
              v-for="order in stats.recent_orders"
              :key="order.id"
              class="order-item"
            >
              <div class="order-main">
                <span class="order-no">{{ order.order_no }}</span>
                <span class="order-company">{{ order.dealer_company }}</span>
              </div>
              <div class="order-meta">
                <span class="order-amount">{{ formatPrice(order.total_amount) }}</span>
                <span
                  class="order-status"
                  :style="{ backgroundColor: statusColors[order.status] + '20', color: statusColors[order.status] }"
                >
                  {{ statusLabels[order.status] }}
                </span>
              </div>
              <div class="order-date">{{ formatDate(order.created_at) }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="quick-links">
        <h2>快捷入口</h2>
        <div class="links-grid">
          <router-link to="/admin/products" class="link-card">
            <span class="link-icon">📦</span>
            <span class="link-text">产品管理</span>
          </router-link>
          <router-link to="/admin/orders" class="link-card">
            <span class="link-icon">📋</span>
            <span class="link-text">订单管理</span>
          </router-link>
          <router-link to="/admin/dealers" class="link-card">
            <span class="link-icon">👥</span>
            <span class="link-text">经销商管理</span>
          </router-link>
          <router-link to="/products" class="link-card">
            <span class="link-icon">🛒</span>
            <span class="link-text">产品目录</span>
          </router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.dashboard-page {
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

.loading, .error {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.error {
  color: #dc2626;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 2rem;
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 10px;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a2e;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.section-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.section-card h2 {
  font-size: 1.125rem;
  color: #1a1a2e;
  margin-bottom: 1rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h2 {
  margin-bottom: 0;
}

.view-all {
  font-size: 0.875rem;
  color: #0f3460;
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.status-item {
  display: flex;
  align-items: center;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 8px;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-count {
  font-weight: 600;
  color: #1a1a2e;
}

.recent-orders {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.order-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
}

.order-no {
  font-weight: 500;
  color: #1a1a2e;
  font-size: 0.875rem;
}

.order-company {
  font-size: 0.75rem;
  color: #64748b;
  display: block;
}

.order-amount {
  font-weight: 600;
  color: #dc2626;
  font-size: 0.875rem;
}

.order-status {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 500;
}

.order-date {
  font-size: 0.75rem;
  color: #64748b;
}

.quick-links {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.quick-links h2 {
  font-size: 1.125rem;
  color: #1a1a2e;
  margin-bottom: 1rem;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.link-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.25rem;
  background: #f8fafc;
  border-radius: 12px;
  text-decoration: none;
  transition: background 0.2s, transform 0.2s;
}

.link-card:hover {
  background: #0f3460;
  transform: translateY(-2px);
}

.link-card:hover .link-text {
  color: white;
}

.link-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.link-text {
  font-size: 0.875rem;
  color: #1a1a2e;
  font-weight: 500;
}
</style>
