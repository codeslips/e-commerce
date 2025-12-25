<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores'
import { dealersApi } from '@/api'

const authStore = useAuthStore()

const editing = ref(false)
const saving = ref(false)
const error = ref('')
const success = ref('')

const formData = ref({
  company_name: '',
  contact_name: '',
  phone: '',
  address: '',
})

const dealer = computed(() => authStore.user?.dealer)

function startEdit() {
  if (!dealer.value) return
  formData.value = {
    company_name: dealer.value.company_name,
    contact_name: dealer.value.contact_name,
    phone: dealer.value.phone,
    address: dealer.value.address || '',
  }
  editing.value = true
}

function cancelEdit() {
  editing.value = false
  error.value = ''
}

async function saveProfile() {
  if (!dealer.value) return
  
  saving.value = true
  error.value = ''
  success.value = ''
  
  try {
    await dealersApi.update(dealer.value.id, formData.value)
    editing.value = false
    success.value = '保存成功'
    await authStore.fetchCurrentUser()
    setTimeout(() => success.value = '', 3000)
  } catch (e: any) {
    error.value = e.response?.data?.detail || '保存失败'
  } finally {
    saving.value = false
  }
}

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
</script>

<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>个人中心</h1>
      <p>查看和管理您的账户信息</p>
    </div>
    
    <div class="profile-cards">
      <div class="profile-card account-card">
        <h2>账户信息</h2>
        <div class="info-row">
          <span class="label">用户名</span>
          <span class="value">{{ authStore.user?.username }}</span>
        </div>
        <div class="info-row">
          <span class="label">邮箱</span>
          <span class="value">{{ authStore.user?.email }}</span>
        </div>
        <div class="info-row">
          <span class="label">角色</span>
          <span class="value">{{ authStore.user?.role === 'admin' ? '管理员' : '经销商' }}</span>
        </div>
      </div>
      
      <div v-if="dealer" class="profile-card dealer-card">
        <div class="card-header">
          <h2>企业信息</h2>
          <div
            class="status-badge"
            :style="{ backgroundColor: statusColors[dealer.status] + '20', color: statusColors[dealer.status] }"
          >
            {{ statusLabels[dealer.status] }}
          </div>
        </div>
        
        <div v-if="!editing">
          <div class="info-row">
            <span class="label">公司名称</span>
            <span class="value">{{ dealer.company_name }}</span>
          </div>
          <div class="info-row">
            <span class="label">联系人</span>
            <span class="value">{{ dealer.contact_name }}</span>
          </div>
          <div class="info-row">
            <span class="label">联系电话</span>
            <span class="value">{{ dealer.phone }}</span>
          </div>
          <div class="info-row">
            <span class="label">地址</span>
            <span class="value">{{ dealer.address || '-' }}</span>
          </div>
          
          <button class="edit-btn" @click="startEdit">
            编辑信息
          </button>
        </div>
        
        <form v-else @submit.prevent="saveProfile" class="edit-form">
          <div class="form-group">
            <label>公司名称</label>
            <input v-model="formData.company_name" required />
          </div>
          <div class="form-group">
            <label>联系人</label>
            <input v-model="formData.contact_name" required />
          </div>
          <div class="form-group">
            <label>联系电话</label>
            <input v-model="formData.phone" required />
          </div>
          <div class="form-group">
            <label>地址</label>
            <textarea v-model="formData.address" rows="2"></textarea>
          </div>
          
          <div v-if="error" class="error-message">{{ error }}</div>
          
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="cancelEdit" :disabled="saving">
              取消
            </button>
            <button type="submit" class="save-btn" :disabled="saving">
              {{ saving ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
        
        <div v-if="success" class="success-message">{{ success }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
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

.profile-cards {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 600px;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.profile-card h2 {
  font-size: 1.125rem;
  color: #1a1a2e;
  margin-bottom: 1.25rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.card-header h2 {
  margin-bottom: 0;
}

.status-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.info-row {
  display: flex;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f3f4f6;
}

.info-row:last-of-type {
  border-bottom: none;
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

.edit-btn {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: #0f3460;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.edit-btn:hover {
  background: #1a1a2e;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  color: #374151;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0f3460;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.cancel-btn {
  flex: 1;
  padding: 0.75rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.cancel-btn:hover:not(:disabled) {
  background: #e5e7eb;
}

.save-btn {
  flex: 1;
  padding: 0.75rem;
  background: #0f3460;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.save-btn:hover:not(:disabled) {
  background: #1a1a2e;
}

.save-btn:disabled,
.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
}

.success-message {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  margin-top: 1rem;
}
</style>

