<script setup lang="ts">

import type {Project} from "@/logic/models";
import {onMounted, ref} from "vue";
import {QAJob} from "@/logic/models";
import {useRoute} from "vue-router";
import {useProjectStore} from "@/logic/stores";

const projStore = useProjectStore();
const route = useRoute();

const selectedProj = ref<Project | null>(null);
const loadingJobs = ref(false);
const selectedProjJobs = ref<QAJob[]>([]);


onMounted(() => {
  selectedProj.value = projStore.projects.find(p => p.id === parseInt(route.query.id as string))!;
  loadJobs();
})


async function loadJobs() {
  console.log(selectedProj.value)

  loadingJobs.value = true;

  try {
    const resp = await fetch(`http://127.0.0.1:8000/qa_job/list_for_project?project_id=${selectedProj.value!.id}`);
    selectedProjJobs.value = await resp.json();
  } finally {
    loadingJobs.value = false;
  }
}

async function runJob() {
  const resp = await fetch(`http://127.0.0.1:8000/project/run?project_id=${selectedProj.value!.id}`);
  const job = await resp.json()
  selectedProjJobs.value = [job, ...selectedProjJobs.value];
}
</script>

<template>
  <div v-if="selectedProj">

      <h1>{{ selectedProj.name }}</h1>
      <button @click="runJob()">run</button>


    <div>
      <template v-if="loadingJobs">Грузим джобы...</template>
      <template v-else>
        <ul>
          <li v-for="job in selectedProjJobs">
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
