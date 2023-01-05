<script setup lang="ts">

import {FormKit} from "@formkit/vue";
import {useProjectListStore} from "@/logic/stores";
import {ref} from "vue";

const projectStore = useProjectListStore();

const name = ref<string>("");
const path = ref<string>("");

function setNameFromPath(path: string) {
  const parts = path.split('\\');
  name.value = parts[parts.length - 1];
}

</script>
<template>
  <FormKit type="form" @submit="projectStore.createProject">
    <FormKit type="text" name="path" label="Path" v-model="path" @input="setNameFromPath"/>
    <FormKit type="text" name="name" label="Name" v-model="name"/>
  </FormKit>
</template>