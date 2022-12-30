<script setup lang="ts">

import {onMounted, Ref, ref} from "vue";

interface QAJob {
  success: boolean;
  output: string;
  created: string;
  id: number;
}

interface Project {
  path: string;
  command: string;
  id: number;
  name: string;

}

const projects = ref<Project[]>([]);
const loadingProjects = ref(false);
const loadingJobs = ref(false);
const selectedProj = ref<Project | null>(null);
const selectedProjJobs = ref<QAJob[]>([]);

onMounted(
    async () => {
      loadingProjects.value = true;
      try {
        const resp = await fetch('http://127.0.0.1:8000/project/list');
        projects.value = await resp.json();
      } finally {
        loadingProjects.value = false;
      }
    }
);

async function loadJobs(proj: Project) {
  selectedProj.value = proj;

  loadingJobs.value = true;

  try {
    const resp = await fetch(`http://127.0.0.1:8000/qa_job/list_for_project?project_id=${proj.id}`);
    selectedProjJobs.value = await resp.json();
  } finally {
    loadingJobs.value = false;
  }
}

async function runJob(proj: Project) {
  selectedProj.value = proj;

  const resp = await fetch(`http://127.0.0.1:8000/project/run?project_id=${proj.id}`);
  const job = await resp.json()
  selectedProjJobs.value = [job, ...selectedProjJobs.value];
}


</script>

<template>
  <main>
    <template v-if="loadingProjects">Грузим проекты...</template>
    <template v-else>
      <template v-if="!projects.length">Нет проектов 🤷‍♂️</template>
      <template v-else>
        <ul>
          <li v-for="proj in projects">
            <div style="display: flex; justify-content: space-between; max-width: 1000px">
              <a href="#" @click="loadJobs(proj)">{{ proj.name }}</a>
              <button @click="runJob(proj)">run</button>
            </div>
            <div v-if="selectedProj">
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
          </li>
        </ul>
      </template>
    </template>


  </main>
</template>
