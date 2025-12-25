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

const statusColors: Record<string, { bg: string, text: string }> = {
  pending: { bg: 'bg-amber-100', text: 'text-amber-700' },
  approved: { bg: 'bg-emerald-100', text: 'text-emerald-700' },
  suspended: { bg: 'bg-red-100', text: 'text-red-700' },
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
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Page Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 mb-2">经销商管理</h1>
          <p class="text-slate-500">管理所有经销商账户</p>
        </div>
        <button 
          class="px-6 py-3 bg-slate-900 text-white font-semibold rounded-xl hover:bg-slate-800 transition-all duration-200 shadow-lg shadow-slate-900/10"
          @click="openCreateModal"
        >
          + 添加经销商
        </button>
      </div>
      
      <!-- Toolbar -->
      <div class="flex flex-wrap gap-4 mb-6">
        <div class="flex gap-3">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索公司名称、联系人..."
            class="px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 placeholder-slate-400 focus:border-amber-500 focus:ring-0 transition-all duration-200 min-w-[250px]"
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
      
      <!-- Dealers Table -->
      <div v-else class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 overflow-hidden overflow-x-auto">
        <table class="w-full min-w-[800px]">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-100">
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">公司名称</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">联系人</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">联系电话</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">账号</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">状态</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">注册时间</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600 whitespace-nowrap">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="dealer in dealers" :key="dealer.id" class="hover:bg-slate-50/50">
              <td class="px-6 py-4 font-medium text-slate-900">{{ dealer.company_name }}</td>
              <td class="px-6 py-4 text-slate-600">{{ dealer.contact_name }}</td>
              <td class="px-6 py-4 text-slate-600">{{ dealer.phone }}</td>
              <td class="px-6 py-4 text-slate-600">{{ dealer.user.username }}</td>
              <td class="px-6 py-4">
                <span 
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                  :class="[statusColors[dealer.status]?.bg, statusColors[dealer.status]?.text]"
                >
                  {{ statusLabels[dealer.status] }}
                </span>
              </td>
              <td class="px-6 py-4 text-slate-400 text-sm">{{ formatDate(dealer.created_at) }}</td>
              <td class="px-6 py-4">
                <div class="flex gap-2 flex-wrap">
                  <button
                    v-if="dealer.status === 'pending'"
                    class="px-3 py-1.5 text-sm font-medium text-emerald-600 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-colors duration-200 whitespace-nowrap"
                    @click="updateStatus(dealer, 'approved')"
                  >
                    通过
                  </button>
                  <button
                    v-if="dealer.status === 'approved'"
                    class="px-3 py-1.5 text-sm font-medium text-amber-600 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors duration-200 whitespace-nowrap"
                    @click="updateStatus(dealer, 'suspended')"
                  >
                    停用
                  </button>
                  <button
                    v-if="dealer.status === 'suspended'"
                    class="px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors duration-200 whitespace-nowrap"
                    @click="updateStatus(dealer, 'approved')"
                  >
                    激活
                  </button>
                  <button 
                    class="px-3 py-1.5 text-sm font-medium text-red-500 border border-red-200 rounded-lg hover:bg-red-500 hover:text-white hover:border-red-500 transition-all duration-200 whitespace-nowrap"
                    @click="deleteDealer(dealer)"
                  >
                    删除
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
          @click="fetchDealers(currentPage - 1)"
        >
          上一页
        </button>
        <span class="text-slate-500 text-sm">第 {{ currentPage }} / {{ totalPages }} 页</span>
        <button
          :disabled="currentPage === totalPages"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="fetchDealers(currentPage + 1)"
        >
          下一页
        </button>
      </div>
      
      <!-- Create Dealer Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeModal">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <!-- Modal Header -->
          <div class="flex justify-between items-center px-6 py-5 border-b border-slate-100">
            <h2 class="text-xl font-bold text-slate-900">添加经销商</h2>
            <button class="text-slate-400 hover:text-slate-600 text-2xl" @click="closeModal">×</button>
          </div>
          
          <!-- Modal Form -->
          <form @submit.prevent="createDealer" class="p-6">
            <h3 class="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">账户信息</h3>
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">用户名 *</label>
                <input v-model="formData.username" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">邮箱 *</label>
                <input v-model="formData.email" type="email" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">密码 *</label>
                <input v-model="formData.password" type="password" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">状态</label>
                <select v-model="formData.status" class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200">
                  <option value="pending">待审核</option>
                  <option value="approved">已通过</option>
                </select>
              </div>
            </div>
            
            <h3 class="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">企业信息</h3>
            <div class="space-y-4 mb-6">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">公司名称 *</label>
                  <input v-model="formData.company_name" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-slate-700 mb-2">联系人 *</label>
                  <input v-model="formData.contact_name" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">联系电话 *</label>
                <input v-model="formData.phone" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">地址</label>
                <textarea v-model="formData.address" rows="2" class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200 resize-none"></textarea>
              </div>
            </div>
            
            <div v-if="modalError" class="p-4 mb-4 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
              {{ modalError }}
            </div>
            
            <div class="flex gap-4">
              <button type="button" class="flex-1 py-3 bg-slate-100 text-slate-600 font-semibold rounded-xl hover:bg-slate-200 transition-all duration-200" @click="closeModal">
                取消
              </button>
              <button type="submit" class="flex-1 py-3 bg-slate-900 text-white font-semibold rounded-xl hover:bg-slate-800 transition-all duration-200 disabled:opacity-60" :disabled="saving">
                {{ saving ? '创建中...' : '创建' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
