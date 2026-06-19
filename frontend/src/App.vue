<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import HomeView from './Views/HomeView.vue'
</script>

<template>
  <div id="app">
    <AppHeader />
    <HomeView />
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  width: 100%;
  overflow-x: hidden;
}
</style>
