<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <router-link :to="{name: 'home'}">potyk-ci</router-link>
  </header>

  <RouterView />
</template>

<style scoped>
</style>
