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

const statusColors: Record<string, { bg: string, text: string }> = {
  pending: { bg: 'bg-amber-100', text: 'text-amber-700' },
  approved: { bg: 'bg-emerald-100', text: 'text-emerald-700' },
  suspended: { bg: 'bg-red-100', text: 'text-red-700' },
}
</script>

<template>
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-2xl">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">个人中心</h1>
        <p class="text-slate-500">查看和管理您的账户信息</p>
      </div>
      
      <div class="space-y-6">
        <!-- Account Info Card -->
        <div class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-6">
          <h2 class="text-lg font-bold text-slate-900 mb-5">账户信息</h2>
          
          <div class="space-y-4">
            <div class="flex py-3 border-b border-slate-100 last:border-0">
              <span class="w-24 text-slate-400 text-sm">用户名</span>
              <span class="flex-1 text-slate-900 font-medium">{{ authStore.user?.username }}</span>
            </div>
            <div class="flex py-3 border-b border-slate-100 last:border-0">
              <span class="w-24 text-slate-400 text-sm">邮箱</span>
              <span class="flex-1 text-slate-900">{{ authStore.user?.email }}</span>
            </div>
            <div class="flex py-3">
              <span class="w-24 text-slate-400 text-sm">角色</span>
              <span class="flex-1 text-slate-900">{{ authStore.user?.role === 'admin' ? '管理员' : '经销商' }}</span>
            </div>
          </div>
        </div>
        
        <!-- Dealer Info Card -->
        <div v-if="dealer" class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-6">
          <div class="flex justify-between items-center mb-5">
            <h2 class="text-lg font-bold text-slate-900">企业信息</h2>
            <span 
              class="px-3 py-1.5 rounded-full text-xs font-semibold"
              :class="[statusColors[dealer.status]?.bg, statusColors[dealer.status]?.text]"
            >
              {{ statusLabels[dealer.status] }}
            </span>
          </div>
          
          <!-- View Mode -->
          <div v-if="!editing" class="space-y-4">
            <div class="flex py-3 border-b border-slate-100">
              <span class="w-24 text-slate-400 text-sm">公司名称</span>
              <span class="flex-1 text-slate-900 font-medium">{{ dealer.company_name }}</span>
            </div>
            <div class="flex py-3 border-b border-slate-100">
              <span class="w-24 text-slate-400 text-sm">联系人</span>
              <span class="flex-1 text-slate-900">{{ dealer.contact_name }}</span>
            </div>
            <div class="flex py-3 border-b border-slate-100">
              <span class="w-24 text-slate-400 text-sm">联系电话</span>
              <span class="flex-1 text-slate-900">{{ dealer.phone }}</span>
            </div>
            <div class="flex py-3">
              <span class="w-24 text-slate-400 text-sm">地址</span>
              <span class="flex-1 text-slate-900">{{ dealer.address || '-' }}</span>
            </div>
            
            <button 
              class="mt-6 px-6 py-3 bg-slate-900 text-white font-semibold rounded-xl hover:bg-slate-800 transition-all duration-200"
              @click="startEdit"
            >
              编辑信息
            </button>
          </div>
          
          <!-- Edit Mode -->
          <form v-else @submit.prevent="saveProfile" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">公司名称</label>
              <input 
                v-model="formData.company_name" 
                required
                class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 focus:border-amber-500 focus:ring-0 transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">联系人</label>
              <input 
                v-model="formData.contact_name" 
                required
                class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 focus:border-amber-500 focus:ring-0 transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">联系电话</label>
              <input 
                v-model="formData.phone" 
                required
                class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 focus:border-amber-500 focus:ring-0 transition-all duration-200"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">地址</label>
              <textarea 
                v-model="formData.address" 
                rows="2"
                class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 focus:border-amber-500 focus:ring-0 transition-all duration-200 resize-none"
              ></textarea>
            </div>
            
            <!-- Error Message -->
            <div v-if="error" class="p-4 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
              {{ error }}
            </div>
            
            <!-- Actions -->
            <div class="flex gap-4 pt-2">
              <button 
                type="button" 
                class="flex-1 py-3 bg-slate-100 text-slate-600 font-semibold rounded-xl hover:bg-slate-200 transition-all duration-200 disabled:opacity-60"
                @click="cancelEdit"
                :disabled="saving"
              >
                取消
              </button>
              <button 
                type="submit" 
                class="flex-1 py-3 bg-slate-900 text-white font-semibold rounded-xl hover:bg-slate-800 transition-all duration-200 disabled:opacity-60"
                :disabled="saving"
              >
                {{ saving ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
          
          <!-- Success Message -->
          <div v-if="success" class="mt-4 p-4 bg-emerald-50 border border-emerald-100 text-emerald-700 rounded-xl text-sm font-medium">
            {{ success }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
