<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useProductStore, useCartStore, useAuthStore } from '@/stores'

const productStore = useProductStore()
const cartStore = useCartStore()
const authStore = useAuthStore()

const searchInput = ref('')

onMounted(async () => {
  await Promise.all([
    productStore.fetchProducts(),
    productStore.fetchCategories(),
  ])
})

async function handleSearch() {
  productStore.setSearch(searchInput.value)
  await productStore.fetchProducts()
}

async function handleCategoryChange(category: string | null) {
  productStore.setCategory(category)
  await productStore.fetchProducts()
}

async function handlePageChange(page: number) {
  await productStore.fetchProducts({ page })
}

function addToCart(product: any) {
  const minQty = product.min_order_quantity || 1
  cartStore.addItem(product, minQty)
}

function formatPrice(price: number) {
  return `¥${price.toFixed(2)}`
}

const showAddToCart = computed(() => authStore.isApprovedDealer)
</script>

<template>
  <div class="products-page">
    <div class="page-header">
      <h1>产品目录</h1>
      <p>浏览我们的全部产品</p>
    </div>
    
    <div class="filters-section">
      <div class="search-box">
        <input
          v-model="searchInput"
          type="text"
          placeholder="搜索产品..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" class="search-btn">搜索</button>
      </div>
      
      <div class="category-filters">
        <button
          class="category-btn"
          :class="{ active: !productStore.selectedCategory }"
          @click="handleCategoryChange(null)"
        >
          全部
        </button>
        <button
          v-for="cat in productStore.categories"
          :key="cat"
          class="category-btn"
          :class="{ active: productStore.selectedCategory === cat }"
          @click="handleCategoryChange(cat)"
        >
          {{ cat }}
        </button>
      </div>
    </div>
    
    <div v-if="productStore.loading" class="loading">
      加载中...
    </div>
    
    <div v-else-if="productStore.error" class="error">
      {{ productStore.error }}
    </div>
    
    <div v-else-if="productStore.products.length === 0" class="empty">
      暂无产品
    </div>
    
    <div v-else class="products-grid">
      <div
        v-for="product in productStore.products"
        :key="product.id"
        class="product-card"
      >
        <div class="product-image">
          <img
            v-if="product.image_url"
            :src="product.image_url"
            :alt="product.name"
          />
          <div v-else class="no-image">
            <span>{{ product.name.charAt(0) }}</span>
          </div>
        </div>
        
        <div class="product-info">
          <div class="product-category">{{ product.category }}</div>
          <h3 class="product-name">{{ product.name }}</h3>
          <p v-if="product.description" class="product-desc">
            {{ product.description }}
          </p>
          
          <div class="product-meta">
            <span class="price">{{ formatPrice(product.price) }}</span>
            <span class="unit">/ {{ product.unit }}</span>
          </div>
          
          <div class="product-footer">
            <span class="min-qty">最低{{ product.min_order_quantity }}{{ product.unit }}起订</span>
            <span class="stock" :class="{ low: product.stock < 100 }">
              库存: {{ product.stock }}
            </span>
          </div>
          
          <button
            v-if="showAddToCart"
            class="add-to-cart-btn"
            @click="addToCart(product)"
            :disabled="product.stock === 0"
          >
            {{ product.stock === 0 ? '缺货' : '加入购物车' }}
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="productStore.totalPages > 1" class="pagination">
      <button
        :disabled="productStore.currentPage === 1"
        @click="handlePageChange(productStore.currentPage - 1)"
      >
        上一页
      </button>
      <span class="page-info">
        第 {{ productStore.currentPage }} / {{ productStore.totalPages }} 页
      </span>
      <button
        :disabled="productStore.currentPage === productStore.totalPages"
        @click="handlePageChange(productStore.currentPage + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<style scoped>
.products-page {
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

.filters-section {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-box {
  display: flex;
  gap: 0.5rem;
}

.search-box input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
}

.search-box input:focus {
  outline: none;
  border-color: #0f3460;
}

.search-btn {
  padding: 0.75rem 1.5rem;
  background: #0f3460;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.search-btn:hover {
  background: #1a1a2e;
}

.category-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.category-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.875rem;
}

.category-btn:hover {
  border-color: #0f3460;
}

.category-btn.active {
  background: #0f3460;
  color: white;
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

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.15);
}

.product-image {
  aspect-ratio: 4/3;
  overflow: hidden;
  background: #f3f4f6;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.no-image span {
  font-size: 3rem;
  color: white;
  font-weight: bold;
}

.product-info {
  padding: 1.25rem;
}

.product-category {
  font-size: 0.75rem;
  color: #0f3460;
  background: rgba(15, 52, 96, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 0.5rem;
}

.product-name {
  font-size: 1.125rem;
  color: #1a1a2e;
  margin-bottom: 0.5rem;
}

.product-desc {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-meta {
  margin-bottom: 0.75rem;
}

.price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #dc2626;
}

.unit {
  font-size: 0.875rem;
  color: #64748b;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 1rem;
}

.stock.low {
  color: #dc2626;
}

.add-to-cart-btn {
  width: 100%;
  padding: 0.75rem;
  background: #0f3460;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.add-to-cart-btn:hover:not(:disabled) {
  background: #1a1a2e;
}

.add-to-cart-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
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
  font-weight: 500;
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
