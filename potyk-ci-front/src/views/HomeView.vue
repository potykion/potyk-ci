<script setup lang="ts">

import {onMounted, ref} from "vue";
import {useProjectListStore} from "@/logic/stores";
import ProjectForm from "@/components/ProjectForm.vue";

let projectStore = useProjectListStore();
onMounted(() => projectStore.loadProjects());

</script>

<template>
  <div>
    <h1 >Projects</h1>

    <details>
      <summary>New Project</summary>
      <ProjectForm></ProjectForm>
    </details>

    <template v-if="projectStore.loadingProjects">Грузим проекты...</template>
    <template v-else>
      <template v-if="!projectStore.projects.length">Нет проектов 🤷‍♂️</template>
      <template v-else>
        <ul>
          <li v-for="proj in projectStore.projects">
            <router-link :to="{name: 'project', query: {id:proj.id}}">{{ proj.name }}</router-link>
          </li>
        </ul>
      </template>
    </template>
  </div>
</template>
