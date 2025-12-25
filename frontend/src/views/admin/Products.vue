<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { productsApi } from '@/api'
import type { Product, PaginatedResponse } from '@/api'

const products = ref<Product[]>([])
const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const searchQuery = ref('')

// Modal state
const showModal = ref(false)
const editingProduct = ref<Product | null>(null)
const saving = ref(false)
const modalError = ref('')

const formData = ref({
  name: '',
  category: '',
  price: 0,
  unit: '袋',
  min_order_quantity: 1,
  description: '',
  stock: 0,
  is_active: true,
})

async function fetchProducts(page = 1) {
  loading.value = true
  error.value = ''
  
  try {
    const response: PaginatedResponse<Product> = await productsApi.list({
      page,
      search: searchQuery.value || undefined,
    })
    products.value = response.items
    currentPage.value = response.page
    totalPages.value = response.pages
  } catch (e: any) {
    error.value = e.response?.data?.detail || '加载产品失败'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingProduct.value = null
  formData.value = {
    name: '',
    category: '',
    price: 0,
    unit: '袋',
    min_order_quantity: 1,
    description: '',
    stock: 0,
    is_active: true,
  }
  modalError.value = ''
  showModal.value = true
}

function openEditModal(product: Product) {
  editingProduct.value = product
  formData.value = {
    name: product.name,
    category: product.category,
    price: product.price,
    unit: product.unit,
    min_order_quantity: product.min_order_quantity,
    description: product.description || '',
    stock: product.stock,
    is_active: product.is_active,
  }
  modalError.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingProduct.value = null
  modalError.value = ''
}

async function saveProduct() {
  saving.value = true
  modalError.value = ''
  
  try {
    if (editingProduct.value) {
      await productsApi.update(editingProduct.value.id, formData.value)
    } else {
      await productsApi.create(formData.value)
    }
    closeModal()
    await fetchProducts(currentPage.value)
  } catch (e: any) {
    modalError.value = e.response?.data?.detail || '保存失败'
  } finally {
    saving.value = false
  }
}

async function deleteProduct(product: Product) {
  if (!confirm(`确定要删除产品 "${product.name}" 吗？`)) return
  
  try {
    await productsApi.delete(product.id)
    await fetchProducts(currentPage.value)
  } catch (e: any) {
    alert(e.response?.data?.detail || '删除失败')
  }
}

async function handleSearch() {
  currentPage.value = 1
  await fetchProducts(1)
}

function formatPrice(price: number | string) {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return `¥${numPrice.toFixed(2)}`
}

onMounted(() => fetchProducts())
</script>

<template>
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Page Header -->
      <div class="flex justify-between items-start mb-8">
        <div>
          <h1 class="text-3xl font-bold text-slate-900 mb-2">产品管理</h1>
          <p class="text-slate-500">管理所有产品</p>
        </div>
        <button 
          class="px-6 py-3 bg-slate-900 text-white font-semibold rounded-xl hover:bg-slate-800 transition-all duration-200 shadow-lg shadow-slate-900/10"
          @click="openCreateModal"
        >
          + 添加产品
        </button>
      </div>
      
      <!-- Search -->
      <div class="mb-6">
        <div class="flex gap-3 max-w-md">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索产品..."
            class="flex-1 px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 placeholder-slate-400 focus:border-amber-500 focus:ring-0 transition-all duration-200"
            @keyup.enter="handleSearch"
          />
          <button 
            class="px-6 py-3 bg-slate-900 text-white font-medium rounded-xl hover:bg-slate-800 transition-all duration-200"
            @click="handleSearch"
          >
            搜索
          </button>
        </div>
      </div>
      
      <!-- Loading / Error -->
      <div v-if="loading" class="text-center py-16 text-slate-500">加载中...</div>
      <div v-else-if="error" class="text-center py-16 text-red-500">{{ error }}</div>
      
      <!-- Products Table -->
      <div v-else class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 overflow-hidden">
        <table class="w-full">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-100">
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">产品名称</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">分类</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">价格</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">库存</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">状态</th>
              <th class="px-6 py-4 text-left text-sm font-semibold text-slate-600">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="product in products" :key="product.id" class="hover:bg-slate-50/50">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg overflow-hidden bg-slate-100 flex-shrink-0">
                    <img
                      v-if="product.image_url"
                      :src="product.image_url"
                      :alt="product.name"
                      class="w-full h-full object-cover"
                    />
                    <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-400 to-orange-500 text-white font-bold text-sm">
                      {{ product.name.charAt(0) }}
                    </div>
                  </div>
                  <span class="font-medium text-slate-900">{{ product.name }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-slate-600">{{ product.category }}</td>
              <td class="px-6 py-4 text-slate-900 font-medium">{{ formatPrice(product.price) }} / {{ product.unit }}</td>
              <td class="px-6 py-4">
                <span :class="product.stock < 100 ? 'text-red-500 font-semibold' : 'text-slate-600'">
                  {{ product.stock }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span 
                  class="px-3 py-1 rounded-full text-xs font-semibold"
                  :class="product.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'"
                >
                  {{ product.is_active ? '上架' : '下架' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex gap-2">
                  <button 
                    class="px-3 py-1.5 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors duration-200"
                    @click="openEditModal(product)"
                  >
                    编辑
                  </button>
                  <button 
                    class="px-3 py-1.5 text-sm font-medium text-red-500 border border-red-200 rounded-lg hover:bg-red-500 hover:text-white hover:border-red-500 transition-all duration-200"
                    @click="deleteProduct(product)"
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
          @click="fetchProducts(currentPage - 1)"
        >
          上一页
        </button>
        <span class="text-slate-500 text-sm">第 {{ currentPage }} / {{ totalPages }} 页</span>
        <button
          :disabled="currentPage === totalPages"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="fetchProducts(currentPage + 1)"
        >
          下一页
        </button>
      </div>
      
      <!-- Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="closeModal">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
          <!-- Modal Header -->
          <div class="flex justify-between items-center px-6 py-5 border-b border-slate-100">
            <h2 class="text-xl font-bold text-slate-900">{{ editingProduct ? '编辑产品' : '添加产品' }}</h2>
            <button class="text-slate-400 hover:text-slate-600 text-2xl" @click="closeModal">×</button>
          </div>
          
          <!-- Modal Form -->
          <form @submit.prevent="saveProduct" class="p-6 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">产品名称 *</label>
                <input v-model="formData.name" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">分类 *</label>
                <input v-model="formData.category" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">价格 *</label>
                <input v-model.number="formData.price" type="number" step="0.01" min="0" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">单位 *</label>
                <input v-model="formData.unit" required class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">最低起订量</label>
                <input v-model.number="formData.min_order_quantity" type="number" min="1" class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">库存</label>
                <input v-model.number="formData.stock" type="number" min="0" class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200" />
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">描述</label>
              <textarea v-model="formData.description" rows="3" class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:border-amber-500 focus:ring-0 transition-all duration-200 resize-none"></textarea>
            </div>
            
            <div class="flex items-center gap-2">
              <input type="checkbox" v-model="formData.is_active" id="is_active" class="w-4 h-4 text-amber-500 border-slate-300 rounded focus:ring-amber-500" />
              <label for="is_active" class="text-sm font-medium text-slate-700 cursor-pointer">上架销售</label>
            </div>
            
            <div v-if="modalError" class="p-4 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
              {{ modalError }}
            </div>
            
            <div class="flex gap-4 pt-2">
              <button type="button" class="flex-1 py-3 bg-slate-100 text-slate-600 font-semibold rounded-xl hover:bg-slate-200 transition-all duration-200" @click="closeModal">
                取消
              </button>
              <button type="submit" class="flex-1 py-3 bg-slate-900 text-white font-semibold rounded-xl hover:bg-slate-800 transition-all duration-200 disabled:opacity-60" :disabled="saving">
                {{ saving ? '保存中...' : '保存' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
