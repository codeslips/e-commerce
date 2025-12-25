<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <div id="app">
    <NavBar />
    <main class="app-main">
      <RouterView />
    </main>
    <footer class="app-footer">
      <p>&copy; 2024 欣与甜. All rights reserved.</p>
    </footer>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f8fafc;
  color: #1a1a2e;
  min-height: 100vh;
  line-height: 1.5;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background: #1a1a2e;
  color: rgba(255, 255, 255, 0.6);
  padding: 1rem;
  text-align: center;
  font-size: 0.875rem;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* Input focus styling */
input:focus,
textarea:focus,
select:focus {
  outline: none;
}

/* Button reset */
button {
  font-family: inherit;
}

/* Link reset */
a {
  color: inherit;
}

@media (max-width: 768px) {
  .app-main {
    padding: 1rem;
  }
}
</style>
