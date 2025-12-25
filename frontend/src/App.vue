<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <div id="app" class="min-h-screen flex flex-col">
    <NavBar />
    <main class="flex-1">
      <RouterView />
    </main>
    <footer class="bg-white border-t border-slate-100 py-10">
      <div class="container mx-auto px-4">
        <div class="flex flex-col items-center justify-center gap-4">
          <div class="flex items-center gap-2 grayscale opacity-50">
            <div class="w-6 h-6 rounded-lg bg-slate-900 flex items-center justify-center">
              <span class="text-white font-bold text-[8px]">XT</span>
            </div>
            <span class="text-sm font-bold text-slate-900">欣与甜</span>
          </div>
          <p class="text-slate-400 text-sm font-medium">一路同行，共同见证梦想的力量</p>
          <div class="text-slate-300 text-[10px] mt-2">© 2025 XIN YU TIAN. All rights reserved.</div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
/* Global styles are now in tailwind.css */
</style>
