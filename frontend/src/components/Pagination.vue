<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  currentPage: number
  totalPages: number
  maxVisible?: number
}

const props = withDefaults(defineProps<Props>(), {
  maxVisible: 5,
})

const emit = defineEmits<{
  (e: 'page-change', page: number): void
}>()

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const total = props.totalPages
  const current = props.currentPage
  const max = props.maxVisible
  
  if (total <= max) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)
    
    // Calculate range around current page
    let start = Math.max(2, current - 1)
    let end = Math.min(total - 1, current + 1)
    
    // Add ellipsis if needed
    if (start > 2) {
      pages.push('...')
    }
    
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
    
    if (end < total - 1) {
      pages.push('...')
    }
    
    // Always show last page
    pages.push(total)
  }
  
  return pages
})

function goToPage(page: number | string) {
  if (typeof page === 'number' && page !== props.currentPage) {
    emit('page-change', page)
  }
}
</script>

<template>
  <div v-if="totalPages > 1" class="pagination">
    <button
      class="page-btn prev"
      :disabled="currentPage === 1"
      @click="goToPage(currentPage - 1)"
    >
      ‹
    </button>
    
    <button
      v-for="(page, index) in visiblePages"
      :key="index"
      class="page-btn"
      :class="{ active: page === currentPage, ellipsis: page === '...' }"
      :disabled="page === '...'"
      @click="goToPage(page)"
    >
      {{ page }}
    </button>
    
    <button
      class="page-btn next"
      :disabled="currentPage === totalPages"
      @click="goToPage(currentPage + 1)"
    >
      ›
    </button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.375rem;
  margin-top: 2rem;
}

.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 0.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled):not(.ellipsis) {
  border-color: #0f3460;
  color: #0f3460;
}

.page-btn.active {
  background: #0f3460;
  border-color: #0f3460;
  color: white;
}

.page-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.page-btn.ellipsis {
  border: none;
  background: none;
  cursor: default;
}

.prev, .next {
  font-size: 1.25rem;
  font-weight: 400;
}
</style>

