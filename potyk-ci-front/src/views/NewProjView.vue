<script setup lang="ts">
import {onMounted, ref} from "vue";
import * as path from "path";

interface Step {
  key: string;
  name: string;
  command: string | object;
  depends?: string;
  versions?: string[];
  selectedVersions?: string[];
}

const steps: Step[] = [
  {
    key: 'qa',
    name: 'qa',
    command: 'pre-commit run -a',
  },
  {
    depends: 'qa',
    key: 'deploy',
    name: 'deploy',
    versions: ['app', '1', 'admin', 'pd'],
    selectedVersions: [],
    command: {
      pd: 'scripts/deploy_pd.bat',
    }
  },
]

const project = {
  name: 'automation-gae',
  path: 'C:\\...',
  steps,
}


const conn = new WebSocket('ws://localhost:8000/ws-run-step');

const selectedStep = ref<Step | null>(null);

function run() {
  output.value = '';
  conn.send(JSON.stringify({
    command: selectedStep.value!.command,
    path: project.path,
  }))
}

const output = ref('');

onMounted(() => {
  conn.onmessage = e => output.value += e.data;
})

const toggleStep = (step: Step) => selectedStep.value = selectedStep.value?.key === step.key ? null : step;

</script>

<template>
  <v-container>
    <h1>{{ project.name }}</h1>

    <v-row>
      <v-col>
        <div class="d-flex align-center">
          <template v-for="step in steps">
            <hr style="width: 100px" v-if="step.depends"/>
            <v-btn color="primary" :variant="selectedStep && selectedStep.key === step.key ? 'tonal' : 'elevated'"
                   @click="toggleStep(step)">
              {{ step.name }}
            </v-btn>
          </template>
        </div>
      </v-col>
    </v-row>


    <v-row v-if="selectedStep">
      <v-col>
        <template v-if="selectedStep.versions?.length">
          <template v-for="version in selectedStep.versions">
            <v-checkbox hide-details :value="version" :label="version"
                        v-model="selectedStep.selectedVersions"></v-checkbox>
          </template>
        </template>
        <v-btn v-if="!selectedStep.versions?.length || selectedStep.selectedVersions?.length" color="primary"
               @click="run">
          run
        </v-btn>
      </v-col>

    </v-row>

    <v-row>
      <v-col>
        <v-code>{{ output }}</v-code>
      </v-col>
    </v-row>

  </v-container>
</template>

<style>
</style>
