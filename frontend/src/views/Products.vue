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

function formatPrice(price: number | string) {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return `¥${numPrice.toFixed(2)}`
}

const showAddToCart = computed(() => authStore.isApprovedDealer)
</script>

<template>
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">产品目录</h1>
        <p class="text-slate-500">浏览我们的全部产品</p>
      </div>
      
      <!-- Search & Filters -->
      <div class="mb-8 space-y-4">
        <!-- Search Box -->
        <div class="bg-white p-2 rounded-2xl shadow-xl shadow-slate-200/60 border border-slate-100">
          <div class="flex flex-col sm:flex-row gap-2">
            <div class="flex-1 relative">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                v-model="searchInput"
                type="text"
                placeholder="搜索产品..."
                class="block w-full pl-11 pr-4 py-4 rounded-xl border-0 bg-slate-50 text-slate-900 placeholder-slate-400 focus:ring-2 focus:ring-amber-500 transition-all duration-200"
                @keyup.enter="handleSearch"
              />
            </div>
            <button 
              @click="handleSearch" 
              class="px-8 py-4 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 active:scale-95 transition-all duration-200 shadow-lg shadow-slate-900/20"
            >
              搜索
            </button>
          </div>
        </div>
        
        <!-- Category Filters -->
        <div class="flex flex-wrap gap-2">
          <button
            class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
            :class="!productStore.selectedCategory 
              ? 'bg-slate-900 text-white shadow-lg shadow-slate-900/20' 
              : 'bg-white text-slate-600 border-2 border-slate-200 hover:border-amber-300 hover:text-amber-600'"
            @click="handleCategoryChange(null)"
          >
            全部
          </button>
          <button
            v-for="cat in productStore.categories"
            :key="cat"
            class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
            :class="productStore.selectedCategory === cat 
              ? 'bg-slate-900 text-white shadow-lg shadow-slate-900/20' 
              : 'bg-white text-slate-600 border-2 border-slate-200 hover:border-amber-300 hover:text-amber-600'"
            @click="handleCategoryChange(cat)"
          >
            {{ cat }}
          </button>
        </div>
      </div>
      
      <!-- Loading State -->
      <div v-if="productStore.loading" class="text-center py-16">
        <div class="inline-flex items-center gap-3 text-slate-500">
          <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>加载中...</span>
        </div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="productStore.error" class="text-center py-16">
        <p class="text-red-500 font-medium">{{ productStore.error }}</p>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="productStore.products.length === 0" class="text-center py-16">
        <div class="text-6xl mb-4">📦</div>
        <p class="text-slate-500 font-medium">暂无产品</p>
      </div>
      
      <!-- Products Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="product in productStore.products"
          :key="product.id"
          class="bg-white rounded-2xl overflow-hidden shadow-lg shadow-slate-100/50 border border-slate-100 hover:shadow-xl hover:shadow-slate-200/50 hover:-translate-y-1 transition-all duration-300"
        >
          <!-- Product Image -->
          <div class="aspect-[4/3] overflow-hidden bg-slate-100">
            <img
              v-if="product.image_url"
              :src="product.image_url"
              :alt="product.name"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-400 to-orange-500">
              <span class="text-5xl font-black text-white/80">{{ product.name.charAt(0) }}</span>
            </div>
          </div>
          
          <!-- Product Info -->
          <div class="p-5">
            <span class="inline-block px-2.5 py-1 mb-3 text-xs font-semibold text-amber-700 bg-amber-100 rounded-lg">
              {{ product.category }}
            </span>
            <h3 class="text-lg font-bold text-slate-900 mb-2">{{ product.name }}</h3>
            <p v-if="product.description" class="text-sm text-slate-500 mb-4 line-clamp-2">
              {{ product.description }}
            </p>
            
            <div class="flex items-baseline gap-1 mb-3">
              <span class="text-2xl font-bold text-orange-500">{{ formatPrice(product.price) }}</span>
              <span class="text-sm text-slate-400">/ {{ product.unit }}</span>
            </div>
            
            <div class="flex justify-between items-center text-xs text-slate-400 mb-4">
              <span>最低{{ product.min_order_quantity }}{{ product.unit }}起订</span>
              <span :class="product.stock < 100 ? 'text-red-500 font-medium' : ''">
                库存: {{ product.stock }}
              </span>
            </div>
            
            <button
              v-if="showAddToCart"
              class="w-full py-3 rounded-xl font-semibold transition-all duration-200"
              :class="product.stock === 0 
                ? 'bg-slate-100 text-slate-400 cursor-not-allowed' 
                : 'bg-slate-900 text-white hover:bg-slate-800 active:scale-[0.98] shadow-lg shadow-slate-900/20'"
              :disabled="product.stock === 0"
              @click="addToCart(product)"
            >
              {{ product.stock === 0 ? '缺货' : '加入购物车' }}
            </button>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="productStore.totalPages > 1" class="flex justify-center items-center gap-4 mt-10">
        <button
          :disabled="productStore.currentPage === 1"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="handlePageChange(productStore.currentPage - 1)"
        >
          上一页
        </button>
        <span class="text-slate-500 text-sm">
          第 {{ productStore.currentPage }} / {{ productStore.totalPages }} 页
        </span>
        <button
          :disabled="productStore.currentPage === productStore.totalPages"
          class="px-5 py-2.5 border-2 border-slate-200 rounded-xl bg-white text-slate-600 font-medium transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="handlePageChange(productStore.currentPage + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>
