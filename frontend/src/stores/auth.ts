import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, getAccessToken, clearTokens } from '@/api'
import type { UserInfo, LoginRequest } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<UserInfo | null>(null)
  const loading = ref(false)
  const initialized = ref(false)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isDealer = computed(() => user.value?.role === 'dealer')
  const isApprovedDealer = computed(() => 
    user.value?.role === 'dealer' && user.value?.dealer?.status === 'approved'
  )
  const dealerId = computed(() => user.value?.dealer?.id)

  // Actions
  async function login(credentials: LoginRequest): Promise<void> {
    loading.value = true
    try {
      const response = await authApi.login(credentials)
      user.value = response.user
    } finally {
      loading.value = false
    }
  }

  async function logout(): Promise<void> {
    loading.value = true
    try {
      await authApi.logout()
    } finally {
      user.value = null
      loading.value = false
    }
  }

  async function fetchCurrentUser(): Promise<void> {
    const token = getAccessToken()
    if (!token) {
      initialized.value = true
      return
    }

    loading.value = true
    try {
      const response = await authApi.getCurrentUser()
      user.value = response
    } catch (error) {
      clearTokens()
      user.value = null
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  function reset(): void {
    user.value = null
    loading.value = false
  }

  return {
    // State
    user,
    loading,
    initialized,
    // Getters
    isAuthenticated,
    isAdmin,
    isDealer,
    isApprovedDealer,
    dealerId,
    // Actions
    login,
    logout,
    fetchCurrentUser,
    reset,
  }
})

