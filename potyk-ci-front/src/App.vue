<script setup lang="ts">
import {RouterLink, RouterView} from 'vue-router'
</script>

<template>
  <v-app id="inspire">

    <v-app-bar>
      <v-toolbar-title>
        <router-link :to="{name: 'home'}">potyk-ci</router-link>
      </v-toolbar-title>
    </v-app-bar>

    <v-main>
      <RouterView/>
    </v-main>
  </v-app>


</template>

<style scoped>



</style>
