<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dealersApi } from '@/api'
import type { Dealer, PaginatedResponse } from '@/api'

const dealers = ref<Dealer[]>([])
const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const statusFilter = ref('')
const searchQuery = ref('')

const statusOptions = [
  { value: '', label: '全部状态' },
  { value: 'pending', label: '待审核' },
  { value: 'approved', label: '已通过' },
  { value: 'suspended', label: '已停用' },
]

const statusLabels: Record<string, string> = {
  pending: '待审核',
  approved: '已通过',
  suspended: '已停用',
}

const statusColors: Record<string, string> = {
  pending: '#f59e0b',
  approved: '#10b981',
  suspended: '#ef4444',
}

// Modal for creating dealer
const showModal = ref(false)
const saving = ref(false)
const modalError = ref('')

const formData = ref({
  username: '',
  email: '',
  password: '',
  company_name: '',
  contact_name: '',
  phone: '',
  address: '',
  status: 'pending',
})

async function fetchDealers(page = 1) {
  loading.value = true
  error.value = ''
  
  try {
    const response: PaginatedResponse<Dealer> = await dealersApi.list({
      page,
      status: statusFilter.value || undefined,
      search: searchQuery.value || undefined,
    })
    dealers.value = response.items
    currentPage.value = response.page
    totalPages.value = response.pages
  } catch (e: any) {
    error.value = e.response?.data?.detail || '加载经销商失败'
  } finally {
    loading.value = false
  }
}

async function handleFilterChange() {
  currentPage.value = 1
  await fetchDealers(1)
}

function openCreateModal() {
  formData.value = {
    username: '',
    email: '',
    password: '',
    company_name: '',
    contact_name: '',
    phone: '',
    address: '',
    status: 'pending',
  }
  modalError.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  modalError.value = ''
}

async function createDealer() {
  saving.value = true
  modalError.value = ''
  
  try {
    await dealersApi.create(formData.value)
    closeModal()
    await fetchDealers(1)
  } catch (e: any) {
    modalError.value = e.response?.data?.detail || '创建失败'
  } finally {
    saving.value = false
  }
}

async function updateStatus(dealer: Dealer, newStatus: string) {
  const statusText = statusLabels[newStatus]
  if (!confirm(`确定要将 "${dealer.company_name}" 的状态改为 "${statusText}" 吗？`)) return
  
  try {
    await dealersApi.updateStatus(dealer.id, newStatus)
    await fetchDealers(currentPage.value)
  } catch (e: any) {
    alert(e.response?.data?.detail || '更新状态失败')
  }
}

async function deleteDealer(dealer: Dealer) {
  if (!confirm(`确定要删除经销商 "${dealer.company_name}" 吗？此操作不可恢复。`)) return
  
  try {
    await dealersApi.delete(dealer.id)
    await fetchDealers(currentPage.value)
  } catch (e: any) {
    alert(e.response?.data?.detail || '删除失败')
  }
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

onMounted(() => fetchDealers())
</script>

<template>
  <div class="admin-dealers">
    <div class="page-header">
      <div>
        <h1>经销商管理</h1>
        <p>管理所有经销商账户</p>
      </div>
      <button class="add-btn" @click="openCreateModal">
        + 添加经销商
      </button>
    </div>
    
    <div class="toolbar">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索公司名称、联系人..."
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
    
    <div v-else class="dealers-table">
      <table>
        <thead>
          <tr>
            <th>公司名称</th>
            <th>联系人</th>
            <th>联系电话</th>
            <th>账号</th>
            <th>状态</th>
            <th>注册时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dealer in dealers" :key="dealer.id">
            <td>{{ dealer.company_name }}</td>
            <td>{{ dealer.contact_name }}</td>
            <td>{{ dealer.phone }}</td>
            <td>{{ dealer.user.username }}</td>
            <td>
              <span
                class="status-badge"
                :style="{ backgroundColor: statusColors[dealer.status] + '20', color: statusColors[dealer.status] }"
              >
                {{ statusLabels[dealer.status] }}
              </span>
            </td>
            <td class="date">{{ formatDate(dealer.created_at) }}</td>
            <td>
              <div class="actions">
                <button
                  v-if="dealer.status === 'pending'"
                  class="approve-btn"
                  @click="updateStatus(dealer, 'approved')"
                >
                  通过
                </button>
                <button
                  v-if="dealer.status === 'approved'"
                  class="suspend-btn"
                  @click="updateStatus(dealer, 'suspended')"
                >
                  停用
                </button>
                <button
                  v-if="dealer.status === 'suspended'"
                  class="activate-btn"
                  @click="updateStatus(dealer, 'approved')"
                >
                  激活
                </button>
                <button class="delete-btn" @click="deleteDealer(dealer)">
                  删除
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
        @click="fetchDealers(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button
        :disabled="currentPage === totalPages"
        @click="fetchDealers(currentPage + 1)"
      >
        下一页
      </button>
    </div>
    
    <!-- Create Dealer Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>添加经销商</h2>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        
        <form @submit.prevent="createDealer" class="modal-form">
          <h3>账户信息</h3>
          <div class="form-row">
            <div class="form-group">
              <label>用户名 *</label>
              <input v-model="formData.username" required />
            </div>
            <div class="form-group">
              <label>邮箱 *</label>
              <input v-model="formData.email" type="email" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>密码 *</label>
              <input v-model="formData.password" type="password" required />
            </div>
            <div class="form-group">
              <label>状态</label>
              <select v-model="formData.status">
                <option value="pending">待审核</option>
                <option value="approved">已通过</option>
              </select>
            </div>
          </div>
          
          <h3>企业信息</h3>
          <div class="form-row">
            <div class="form-group">
              <label>公司名称 *</label>
              <input v-model="formData.company_name" required />
            </div>
            <div class="form-group">
              <label>联系人 *</label>
              <input v-model="formData.contact_name" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>联系电话 *</label>
              <input v-model="formData.phone" required />
            </div>
          </div>
          
          <div class="form-group">
            <label>地址</label>
            <textarea v-model="formData.address" rows="2"></textarea>
          </div>
          
          <div v-if="modalError" class="error-message">{{ modalError }}</div>
          
          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="closeModal">取消</button>
            <button type="submit" class="save-btn" :disabled="saving">
              {{ saving ? '创建中...' : '创建' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dealers {
  padding: 1rem 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.add-btn {
  padding: 0.75rem 1.5rem;
  background: #0f3460;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.add-btn:hover {
  background: #1a1a2e;
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
  min-width: 250px;
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

.dealers-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
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
  white-space: nowrap;
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
  flex-wrap: wrap;
}

.approve-btn, .suspend-btn, .activate-btn, .delete-btn {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  white-space: nowrap;
}

.approve-btn {
  background: #dcfce7;
  color: #16a34a;
  border: none;
}

.approve-btn:hover {
  background: #bbf7d0;
}

.activate-btn {
  background: #dbeafe;
  color: #2563eb;
  border: none;
}

.activate-btn:hover {
  background: #bfdbfe;
}

.suspend-btn {
  background: #fef3c7;
  color: #d97706;
  border: none;
}

.suspend-btn:hover {
  background: #fde68a;
}

.delete-btn {
  background: none;
  border: 1px solid #dc2626;
  color: #dc2626;
}

.delete-btn:hover {
  background: #dc2626;
  color: white;
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
  max-width: 550px;
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

.modal-form {
  padding: 1.5rem;
}

.modal-form h3 {
  font-size: 0.95rem;
  color: #64748b;
  margin-bottom: 1rem;
  margin-top: 1rem;
}

.modal-form h3:first-of-type {
  margin-top: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0f3460;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.modal-actions button {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
  border: none;
}

.save-btn {
  background: #0f3460;
  color: white;
  border: none;
}

.save-btn:hover:not(:disabled) {
  background: #1a1a2e;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

