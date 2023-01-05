<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <router-link :to="{name: 'home'}">potyk-ci</router-link>
  </header>

  <main>
    <RouterView/>
  </main>
</template>

<style scoped>

header {
  border-bottom: 1px solid black;
  padding: 10px;
}

main {
  padding: 10px;
}

</style>
