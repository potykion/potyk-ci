<script setup lang="ts">

import {onMounted} from "vue";
import {useRoute} from "vue-router";
import {useSelectedProjectStore} from "@/logic/stores";

const route = useRoute();
const selectedProjectStore = useSelectedProjectStore();


onMounted(() => {
  selectedProjectStore.select(parseInt(route.query.id as string));
})


</script>

<template>
  <div v-if="selectedProjectStore.selectedProj">

    <h1 >{{ selectedProjectStore.selectedProj.name }}</h1>
    <button @click="selectedProjectStore.runJob()">run</button>


    <div>
      <template v-if="selectedProjectStore.loadingJobs">Грузим джобы...</template>
      <template v-else>
        <ul>
          <li v-for="job in selectedProjectStore.selectedProjJobs">
            <details>
              <summary :style="{color: job.success ? 'green' : 'red', cursor: 'pointer'}">
                {{ job.created }}
              </summary>

              <div style="white-space: pre">
                <code>{{ job.output }}</code>
              </div>
            </details>
          </li>
        </ul>
      </template>
    </div>
  </div>
</template>

<style>
</style>
