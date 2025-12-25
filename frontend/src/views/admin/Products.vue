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

function formatPrice(price: number) {
  return `¥${price.toFixed(2)}`
}

onMounted(() => fetchProducts())
</script>

<template>
  <div class="admin-products">
    <div class="page-header">
      <div>
        <h1>产品管理</h1>
        <p>管理所有产品</p>
      </div>
      <button class="add-btn" @click="openCreateModal">
        + 添加产品
      </button>
    </div>
    
    <div class="toolbar">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索产品..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">搜索</button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="products-table">
      <table>
        <thead>
          <tr>
            <th>产品名称</th>
            <th>分类</th>
            <th>价格</th>
            <th>库存</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>
              <div class="product-cell">
                <img
                  v-if="product.image_url"
                  :src="product.image_url"
                  :alt="product.name"
                  class="product-thumb"
                />
                <div v-else class="product-thumb placeholder">
                  {{ product.name.charAt(0) }}
                </div>
                <span>{{ product.name }}</span>
              </div>
            </td>
            <td>{{ product.category }}</td>
            <td>{{ formatPrice(product.price) }} / {{ product.unit }}</td>
            <td :class="{ 'low-stock': product.stock < 100 }">
              {{ product.stock }}
            </td>
            <td>
              <span
                class="status-badge"
                :class="product.is_active ? 'active' : 'inactive'"
              >
                {{ product.is_active ? '上架' : '下架' }}
              </span>
            </td>
            <td>
              <div class="actions">
                <button class="edit-btn" @click="openEditModal(product)">
                  编辑
                </button>
                <button class="delete-btn" @click="deleteProduct(product)">
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
        @click="fetchProducts(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button
        :disabled="currentPage === totalPages"
        @click="fetchProducts(currentPage + 1)"
      >
        下一页
      </button>
    </div>
    
    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingProduct ? '编辑产品' : '添加产品' }}</h2>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        
        <form @submit.prevent="saveProduct" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label>产品名称 *</label>
              <input v-model="formData.name" required />
            </div>
            <div class="form-group">
              <label>分类 *</label>
              <input v-model="formData.category" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>价格 *</label>
              <input v-model.number="formData.price" type="number" step="0.01" min="0" required />
            </div>
            <div class="form-group">
              <label>单位 *</label>
              <input v-model="formData.unit" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>最低起订量</label>
              <input v-model.number="formData.min_order_quantity" type="number" min="1" />
            </div>
            <div class="form-group">
              <label>库存</label>
              <input v-model.number="formData.stock" type="number" min="0" />
            </div>
          </div>
          
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="formData.description" rows="3"></textarea>
          </div>
          
          <div class="form-group checkbox">
            <label>
              <input type="checkbox" v-model="formData.is_active" />
              上架销售
            </label>
          </div>
          
          <div v-if="modalError" class="error-message">{{ modalError }}</div>
          
          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="closeModal">取消</button>
            <button type="submit" class="save-btn" :disabled="saving">
              {{ saving ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-products {
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
  margin-bottom: 1.5rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
  max-width: 400px;
}

.search-box input {
  flex: 1;
  padding: 0.625rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
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

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.error {
  color: #dc2626;
}

.products-table {
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

.product-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.product-thumb {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
}

.product-thumb.placeholder {
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
}

.low-stock {
  color: #dc2626;
  font-weight: 500;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.active {
  background: #dcfce7;
  color: #16a34a;
}

.status-badge.inactive {
  background: #f3f4f6;
  color: #6b7280;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
}

.edit-btn {
  background: #e0f2fe;
  color: #0369a1;
  border: none;
}

.edit-btn:hover {
  background: #bae6fd;
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
  max-width: 500px;
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
.form-group textarea {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #0f3460;
}

.form-group.checkbox label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.form-group.checkbox input {
  width: auto;
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

