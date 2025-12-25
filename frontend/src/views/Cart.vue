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

function formatPrice(price: number) {
  return `¥${price.toFixed(2)}`
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
  <div class="cart-page">
    <div class="page-header">
      <h1>购物车</h1>
      <p v-if="!cartStore.isEmpty">共 {{ cartStore.totalItems }} 件商品</p>
    </div>
    
    <div v-if="cartStore.isEmpty" class="empty-cart">
      <div class="empty-icon">🛒</div>
      <p>购物车是空的</p>
      <router-link to="/products" class="browse-btn">去选购</router-link>
    </div>
    
    <div v-else class="cart-content">
      <div class="cart-items">
        <div
          v-for="item in cartStore.items"
          :key="item.product.id"
          class="cart-item"
        >
          <div class="item-image">
            <img
              v-if="item.product.image_url"
              :src="item.product.image_url"
              :alt="item.product.name"
            />
            <div v-else class="no-image">
              {{ item.product.name.charAt(0) }}
            </div>
          </div>
          
          <div class="item-info">
            <h3>{{ item.product.name }}</h3>
            <p class="item-category">{{ item.product.category }}</p>
            <p class="item-price">
              {{ formatPrice(item.product.price) }} / {{ item.product.unit }}
            </p>
          </div>
          
          <div class="item-quantity">
            <label>数量</label>
            <input
              type="number"
              :value="item.quantity"
              :min="item.product.min_order_quantity"
              @change="updateQuantity(item.product.id, $event)"
            />
            <span class="min-qty">最低 {{ item.product.min_order_quantity }}</span>
          </div>
          
          <div class="item-subtotal">
            <p class="subtotal-label">小计</p>
            <p class="subtotal-price">
              {{ formatPrice(item.product.price * item.quantity) }}
            </p>
          </div>
          
          <button
            class="remove-btn"
            @click="cartStore.removeItem(item.product.id)"
          >
            删除
          </button>
        </div>
      </div>
      
      <div class="cart-summary">
        <h2>订单信息</h2>
        
        <div class="summary-row total">
          <span>商品总额</span>
          <span class="total-amount">{{ formatPrice(cartStore.totalAmount) }}</span>
        </div>
        
        <div class="form-group">
          <label for="address">配送地址 *</label>
          <textarea
            id="address"
            v-model="shippingAddress"
            placeholder="请输入详细配送地址"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="notes">备注</label>
          <textarea
            id="notes"
            v-model="notes"
            placeholder="如有特殊要求请备注"
            rows="2"
          ></textarea>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div v-if="!authStore.isApprovedDealer" class="warning-message">
          您的账户尚未通过审核，暂时无法下单
        </div>
        
        <button
          class="submit-btn"
          :disabled="!canSubmit || submitting"
          @click="submitOrder"
        >
          {{ submitting ? '提交中...' : '提交订单' }}
        </button>
        
        <router-link to="/products" class="continue-shopping">
          继续选购
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cart-page {
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

.empty-cart {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-cart p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.browse-btn {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: #0f3460;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
}

.browse-btn:hover {
  background: #1a1a2e;
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 2rem;
}

@media (max-width: 900px) {
  .cart-content {
    grid-template-columns: 1fr;
  }
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr 120px 100px auto;
  gap: 1rem;
  align-items: center;
  padding: 1.25rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

@media (max-width: 700px) {
  .cart-item {
    grid-template-columns: 60px 1fr;
    grid-template-rows: auto auto auto;
  }
  
  .item-quantity,
  .item-subtotal,
  .remove-btn {
    grid-column: 2;
  }
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  background: #f3f4f6;
}

.item-image img {
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
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.item-info h3 {
  font-size: 1rem;
  color: #1a1a2e;
  margin-bottom: 0.25rem;
}

.item-category {
  font-size: 0.75rem;
  color: #0f3460;
  margin-bottom: 0.25rem;
}

.item-price {
  font-size: 0.875rem;
  color: #dc2626;
  font-weight: 500;
}

.item-quantity {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-quantity label {
  font-size: 0.75rem;
  color: #64748b;
}

.item-quantity input {
  width: 80px;
  padding: 0.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  text-align: center;
}

.item-quantity input:focus {
  outline: none;
  border-color: #0f3460;
}

.min-qty {
  font-size: 0.7rem;
  color: #9ca3af;
}

.item-subtotal {
  text-align: right;
}

.subtotal-label {
  font-size: 0.75rem;
  color: #64748b;
}

.subtotal-price {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a1a2e;
}

.remove-btn {
  padding: 0.5rem 1rem;
  background: none;
  border: 1px solid #dc2626;
  color: #dc2626;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.remove-btn:hover {
  background: #dc2626;
  color: white;
}

.cart-summary {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 1rem;
}

.cart-summary h2 {
  font-size: 1.25rem;
  color: #1a1a2e;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.95rem;
}

.summary-row.total {
  font-weight: 600;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 1.5rem;
}

.total-amount {
  font-size: 1.5rem;
  color: #dc2626;
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

.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  resize: vertical;
}

.form-group textarea:focus {
  outline: none;
  border-color: #0f3460;
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

.warning-message {
  background: #fffbeb;
  border: 1px solid #fde68a;
  color: #d97706;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(15, 52, 96, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.continue-shopping {
  display: block;
  text-align: center;
  color: #0f3460;
  text-decoration: none;
  font-size: 0.875rem;
}

.continue-shopping:hover {
  text-decoration: underline;
}
</style>

