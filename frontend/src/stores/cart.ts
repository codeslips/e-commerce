import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { Product } from '@/api'

export interface CartItem {
  product: Product
  quantity: number
}

const CART_STORAGE_KEY = 'xinyutian_cart'

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref<CartItem[]>([])

  // Load from localStorage
  function loadFromStorage(): void {
    const stored = localStorage.getItem(CART_STORAGE_KEY)
    if (stored) {
      try {
        items.value = JSON.parse(stored)
      } catch {
        items.value = []
      }
    }
  }

  // Save to localStorage
  function saveToStorage(): void {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items.value))
  }

  // Watch for changes and persist
  watch(items, saveToStorage, { deep: true })

  // Getters
  const totalItems = computed(() => 
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const totalAmount = computed(() => 
    items.value.reduce((sum, item) => sum + item.product.price * item.quantity, 0)
  )

  const isEmpty = computed(() => items.value.length === 0)

  // Actions
  function addItem(product: Product, quantity: number = 1): void {
    const existingIndex = items.value.findIndex(item => item.product.id === product.id)
    
    if (existingIndex >= 0) {
      items.value[existingIndex].quantity += quantity
    } else {
      items.value.push({ product, quantity })
    }
  }

  function removeItem(productId: string): void {
    const index = items.value.findIndex(item => item.product.id === productId)
    if (index >= 0) {
      items.value.splice(index, 1)
    }
  }

  function updateQuantity(productId: string, quantity: number): void {
    const item = items.value.find(item => item.product.id === productId)
    if (item) {
      if (quantity <= 0) {
        removeItem(productId)
      } else {
        item.quantity = quantity
      }
    }
  }

  function clearCart(): void {
    items.value = []
  }

  function getItemQuantity(productId: string): number {
    const item = items.value.find(item => item.product.id === productId)
    return item?.quantity || 0
  }

  // Initialize
  loadFromStorage()

  return {
    // State
    items,
    // Getters
    totalItems,
    totalAmount,
    isEmpty,
    // Actions
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    getItemQuantity,
    loadFromStorage,
  }
})

