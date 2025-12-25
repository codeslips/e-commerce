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
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>欣与甜</h1>
        <p>经销商订货平台</p>
      </div>
      
      <form @submit.prevent="handleSubmit" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="请输入用户名"
            required
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="请输入密码"
            required
            :disabled="loading"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div class="demo-section">
        <div class="demo-header">
          <span class="demo-icon">✨</span>
          <span>Demo 账号 (点击自动填充)</span>
        </div>
        <div class="demo-accounts">
          <button
            v-for="account in demoAccounts"
            :key="account.username"
            type="button"
            class="demo-account-card"
            :class="{ 'active': username === account.username }"
            @click="selectDemoAccount(account)"
          >
            <div class="account-badge" :class="account.role">
              {{ account.label }}
            </div>
            <div class="account-info">
              <span class="account-username">{{ account.username }}</span>
              <span class="account-desc">{{ account.description }}</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 1rem;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2.5rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2rem;
  color: #1a1a2e;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.login-header p {
  color: #64748b;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #0f3460;
  box-shadow: 0 0 0 3px rgba(15, 52, 96, 0.1);
}

.form-group input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.error-message {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
}

.login-button {
  padding: 1rem;
  background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(15, 52, 96, 0.3);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.demo-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.demo-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.demo-icon {
  font-size: 1rem;
}

.demo-accounts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.demo-account-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  width: 100%;
}

.demo-account-card:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateX(4px);
}

.demo-account-card.active {
  background: #eff6ff;
  border-color: #3b82f6;
}

.account-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 600;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.account-badge.admin {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
  color: white;
}

.account-badge.dealer {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.account-badge.dealer-pending {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.account-info {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  min-width: 0;
}

.account-username {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.account-desc {
  font-size: 0.75rem;
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
