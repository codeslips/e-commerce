<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore, useAuthStore } from '@/stores'
import { ordersApi } from '@/api'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const shippingAddress = ref('')
const notes = ref('')
const submitting = ref(false)
const error = ref('')

const canSubmit = computed(() => 
  !cartStore.isEmpty && 
  shippingAddress.value.trim() !== '' &&
  authStore.isApprovedDealer
)

function formatPrice(price: number | string) {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return `¥${numPrice.toFixed(2)}`
}

function updateQuantity(productId: string, event: Event) {
  const target = event.target as HTMLInputElement
  const quantity = parseInt(target.value, 10)
  if (!isNaN(quantity)) {
    cartStore.updateQuantity(productId, quantity)
  }
}

async function submitOrder() {
  if (!canSubmit.value) return
  
  submitting.value = true
  error.value = ''
  
  try {
    const orderData = {
      items: cartStore.items.map(item => ({
        product_id: item.product.id,
        product_name: item.product.name,
        quantity: item.quantity,
        unit_price: item.product.price,
      })),
      shipping_address: shippingAddress.value,
      notes: notes.value || undefined,
    }
    
    await ordersApi.create(orderData)
    cartStore.clearCart()
    router.push('/orders')
  } catch (e: any) {
    error.value = e.response?.data?.detail || '提交订单失败，请重试'
  } finally {
    submitting.value = false
  }
}

// Pre-fill address from dealer profile
if (authStore.user?.dealer?.address) {
  shippingAddress.value = authStore.user.dealer.address
}
</script>

<template>
  <div class="py-8">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">购物车</h1>
        <p v-if="!cartStore.isEmpty" class="text-slate-500">共 {{ cartStore.totalItems }} 件商品</p>
      </div>
      
      <!-- Empty Cart -->
      <div v-if="cartStore.isEmpty" class="text-center py-16 bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100">
        <div class="text-6xl mb-4">🛒</div>
        <p class="text-slate-500 font-medium mb-6">购物车是空的</p>
        <router-link 
          to="/products" 
          class="inline-block px-8 py-3 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 transition-all duration-200"
        >
          去选购
        </router-link>
      </div>
      
      <!-- Cart Content -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2 space-y-4">
          <div
            v-for="item in cartStore.items"
            :key="item.product.id"
            class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-5"
          >
            <div class="flex gap-4">
              <!-- Product Image -->
              <div class="w-20 h-20 rounded-xl overflow-hidden bg-slate-100 flex-shrink-0">
                <img
                  v-if="item.product.image_url"
                  :src="item.product.image_url"
                  :alt="item.product.name"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-amber-400 to-orange-500">
                  <span class="text-2xl font-bold text-white">{{ item.product.name.charAt(0) }}</span>
                </div>
              </div>
              
              <!-- Product Info -->
              <div class="flex-1 min-w-0">
                <h3 class="font-bold text-slate-900 mb-1">{{ item.product.name }}</h3>
                <p class="text-xs text-amber-600 font-medium mb-1">{{ item.product.category }}</p>
                <p class="text-orange-500 font-semibold">
                  {{ formatPrice(item.product.price) }} / {{ item.product.unit }}
                </p>
              </div>
              
              <!-- Quantity -->
              <div class="flex flex-col items-center gap-1">
                <label class="text-xs text-slate-400">数量</label>
                <input
                  type="number"
                  :value="item.quantity"
                  :min="item.product.min_order_quantity"
                  class="w-20 px-3 py-2 border-2 border-slate-200 rounded-xl text-center font-medium focus:border-amber-500 focus:ring-0 transition-all duration-200"
                  @change="updateQuantity(item.product.id, $event)"
                />
                <span class="text-[10px] text-slate-400">最低 {{ item.product.min_order_quantity }}</span>
              </div>
              
              <!-- Subtotal -->
              <div class="text-right">
                <p class="text-xs text-slate-400 mb-1">小计</p>
                <p class="text-lg font-bold text-slate-900">
                  {{ formatPrice(item.product.price * item.quantity) }}
                </p>
              </div>
              
              <!-- Remove Button -->
              <button
                class="px-3 py-2 text-sm font-medium text-red-500 border-2 border-red-200 rounded-xl hover:bg-red-500 hover:text-white hover:border-red-500 transition-all duration-200 self-start"
                @click="cartStore.removeItem(item.product.id)"
              >
                删除
              </button>
            </div>
          </div>
        </div>
        
        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-2xl shadow-lg shadow-slate-100/50 border border-slate-100 p-6 sticky top-24">
            <h2 class="text-xl font-bold text-slate-900 mb-6 pb-4 border-b border-slate-100">订单信息</h2>
            
            <!-- Total -->
            <div class="flex justify-between items-center mb-6 pb-4 border-b border-slate-100">
              <span class="text-slate-600">商品总额</span>
              <span class="text-2xl font-bold text-orange-500">{{ formatPrice(cartStore.totalAmount) }}</span>
            </div>
            
            <!-- Shipping Address -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-slate-700 mb-2">配送地址 *</label>
              <textarea
                v-model="shippingAddress"
                placeholder="请输入详细配送地址"
                rows="3"
                class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 placeholder-slate-400 focus:border-amber-500 focus:ring-0 transition-all duration-200 resize-none"
              ></textarea>
            </div>
            
            <!-- Notes -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-slate-700 mb-2">备注</label>
              <textarea
                v-model="notes"
                placeholder="如有特殊要求请备注"
                rows="2"
                class="w-full px-4 py-3 border-2 border-slate-200 rounded-xl bg-white text-slate-900 placeholder-slate-400 focus:border-amber-500 focus:ring-0 transition-all duration-200 resize-none"
              ></textarea>
            </div>
            
            <!-- Error Message -->
            <div v-if="error" class="p-4 mb-4 bg-red-50 border border-red-100 text-red-600 rounded-xl text-sm font-medium">
              {{ error }}
            </div>
            
            <!-- Warning Message -->
            <div v-if="!authStore.isApprovedDealer" class="p-4 mb-4 bg-amber-50 border border-amber-100 text-amber-700 rounded-xl text-sm font-medium">
              您的账户尚未通过审核，暂时无法下单
            </div>
            
            <!-- Submit Button -->
            <button
              class="w-full py-4 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 active:scale-[0.98] transition-all duration-200 shadow-lg shadow-slate-900/20 disabled:opacity-60 disabled:cursor-not-allowed mb-4"
              :disabled="!canSubmit || submitting"
              @click="submitOrder"
            >
              {{ submitting ? '提交中...' : '提交订单' }}
            </button>
            
            <!-- Continue Shopping -->
            <router-link 
              to="/products" 
              class="block text-center text-slate-500 text-sm font-medium hover:text-amber-600 transition-colors duration-200"
            >
              继续选购
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
