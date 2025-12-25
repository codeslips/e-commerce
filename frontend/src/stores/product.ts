import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsApi } from '@/api'
import type { Product, ProductsParams, PaginatedResponse } from '@/api'

export const useProductStore = defineStore('product', () => {
  // State
  const products = ref<Product[]>([])
  const categories = ref<string[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // Pagination
  const currentPage = ref(1)
  const pageSize = ref(20)
  const totalItems = ref(0)
  const totalPages = ref(0)
  
  // Filters
  const selectedCategory = ref<string | null>(null)
  const searchQuery = ref('')

  // Getters
  const filteredProducts = computed(() => products.value)
  const hasMore = computed(() => currentPage.value < totalPages.value)

  // Actions
  async function fetchProducts(params?: ProductsParams): Promise<void> {
    loading.value = true
    error.value = null
    
    try {
      const queryParams: ProductsParams = {
        page: params?.page ?? currentPage.value,
        page_size: params?.page_size ?? pageSize.value,
        category: params?.category ?? selectedCategory.value ?? undefined,
        search: params?.search ?? (searchQuery.value || undefined),
      }
      
      const response: PaginatedResponse<Product> = await productsApi.list(queryParams)
      products.value = response.items
      totalItems.value = response.total
      totalPages.value = response.pages
      currentPage.value = response.page
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load products'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories(): Promise<void> {
    try {
      categories.value = await productsApi.getCategories()
    } catch (e) {
      console.error('Failed to fetch categories:', e)
    }
  }

  async function loadMore(): Promise<void> {
    if (!hasMore.value || loading.value) return
    
    loading.value = true
    error.value = null
    
    try {
      const response = await productsApi.list({
        page: currentPage.value + 1,
        page_size: pageSize.value,
        category: selectedCategory.value ?? undefined,
        search: searchQuery.value || undefined,
      })
      
      products.value = [...products.value, ...response.items]
      currentPage.value = response.page
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to load more products'
    } finally {
      loading.value = false
    }
  }

  function setCategory(category: string | null): void {
    selectedCategory.value = category
    currentPage.value = 1
  }

  function setSearch(query: string): void {
    searchQuery.value = query
    currentPage.value = 1
  }

  function reset(): void {
    products.value = []
    currentPage.value = 1
    totalItems.value = 0
    totalPages.value = 0
    selectedCategory.value = null
    searchQuery.value = ''
    error.value = null
  }

  return {
    // State
    products,
    categories,
    loading,
    error,
    currentPage,
    pageSize,
    totalItems,
    totalPages,
    selectedCategory,
    searchQuery,
    // Getters
    filteredProducts,
    hasMore,
    // Actions
    fetchProducts,
    fetchCategories,
    loadMore,
    setCategory,
    setSearch,
    reset,
  }
})

