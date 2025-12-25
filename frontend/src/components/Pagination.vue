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
  <div v-if="totalPages > 1" class="flex justify-center items-center gap-1.5 mt-8">
    <button
      class="min-w-9 h-9 px-2 border-2 border-slate-200 rounded-lg bg-white text-slate-600 text-xl font-normal cursor-pointer transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:cursor-not-allowed disabled:opacity-50"
      :disabled="currentPage === 1"
      @click="goToPage(currentPage - 1)"
    >
      ‹
    </button>
    
    <button
      v-for="(page, index) in visiblePages"
      :key="index"
      class="min-w-9 h-9 px-2 border-2 rounded-lg text-sm font-medium cursor-pointer transition-all duration-200"
      :class="[
        page === currentPage 
          ? 'bg-slate-900 border-slate-900 text-white' 
          : page === '...' 
            ? 'border-transparent bg-transparent cursor-default' 
            : 'border-slate-200 bg-white text-slate-600 hover:border-amber-500 hover:text-amber-600'
      ]"
      :disabled="page === '...'"
      @click="goToPage(page)"
    >
      {{ page }}
    </button>
    
    <button
      class="min-w-9 h-9 px-2 border-2 border-slate-200 rounded-lg bg-white text-slate-600 text-xl font-normal cursor-pointer transition-all duration-200 hover:border-amber-500 hover:text-amber-600 disabled:cursor-not-allowed disabled:opacity-50"
      :disabled="currentPage === totalPages"
      @click="goToPage(currentPage + 1)"
    >
      ›
    </button>
  </div>
</template>
