<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores'

const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => authStore.isAdmin)
const username = computed(() => authStore.user?.username)
const companyName = computed(() => authStore.user?.dealer?.company_name)
</script>

<template>
  <div class="home-page">
    <div class="hero-section">
      <div class="hero-content">
        <h1>欢迎来到<span class="highlight">欣与甜</span></h1>
        <p class="subtitle">经销商订货平台</p>
        
        <div v-if="isLoggedIn" class="welcome-message">
          <p v-if="isAdmin">您好，管理员 <strong>{{ username }}</strong></p>
          <p v-else-if="companyName">您好，<strong>{{ companyName }}</strong></p>
          <p v-else>您好，<strong>{{ username }}</strong></p>
        </div>
        
        <div class="hero-actions">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="btn btn-primary">
              登录
            </router-link>
            <router-link to="/products" class="btn btn-secondary">
              浏览产品
            </router-link>
          </template>
          <template v-else-if="isAdmin">
            <router-link to="/admin" class="btn btn-primary">
              进入管理后台
            </router-link>
            <router-link to="/products" class="btn btn-secondary">
              浏览产品
            </router-link>
          </template>
          <template v-else>
            <router-link to="/products" class="btn btn-primary">
              开始选购
            </router-link>
            <router-link to="/orders" class="btn btn-secondary">
              查看订单
            </router-link>
          </template>
        </div>
      </div>
    </div>
    
    <div class="features-section">
      <h2>为什么选择我们</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🍞</div>
          <h3>优质产品</h3>
          <p>精选优质原料，严格品质把控，为您提供放心的食品</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🚚</div>
          <h3>快速配送</h3>
          <p>专业物流团队，确保产品新鲜送达</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💰</div>
          <h3>优惠价格</h3>
          <p>经销商专享批发价格，合作共赢</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📱</div>
          <h3>便捷订货</h3>
          <p>在线下单，随时查询订单状态</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  margin: -2rem;
}

.hero-section {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 4rem 2rem;
  text-align: center;
  color: white;
}

.hero-content {
  max-width: 600px;
  margin: 0 auto;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.highlight {
  color: #fbbf24;
}

.subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 1.5rem;
}

.welcome-message {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.welcome-message p {
  margin: 0;
  font-size: 1.1rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.875rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  background: #fbbf24;
  color: #1a1a2e;
}

.btn-primary:hover {
  box-shadow: 0 10px 20px rgba(251, 191, 36, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
}

.features-section {
  padding: 4rem 2rem;
  background: #f8fafc;
}

.features-section h2 {
  text-align: center;
  font-size: 1.75rem;
  color: #1a1a2e;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.125rem;
  color: #1a1a2e;
  margin-bottom: 0.5rem;
}

.feature-card p {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.5;
}
</style>
