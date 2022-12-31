<script setup lang="ts">

import {onMounted, ref} from "vue";
import {useProjectStore} from "@/logic/stores";

let projectStore = useProjectStore();
onMounted(() => projectStore.loadProjects());

</script>

<template>
  <main>
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
  </main>
</template>
