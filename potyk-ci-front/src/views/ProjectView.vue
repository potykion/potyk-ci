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

    <h1>{{ selectedProjectStore.selectedProj.name }}</h1>
    <button @click="selectedProjectStore.scheduleJob()">run</button>


    <div>
      <template v-if="selectedProjectStore.loadingJobs">Грузим джобы...</template>
      <template v-else>
        <ul>
          <li v-for="job in selectedProjectStore.selectedProjJobs">
            <details class="details-right">
              <summary :class="[job.statusColor, 'cursor-pointer']">
                <div class="inline-block ">Job № {{ job.id }}<br>{{ job.created }}</div>

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
