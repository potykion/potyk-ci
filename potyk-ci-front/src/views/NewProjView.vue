<script setup lang="ts">
import {onMounted, ref} from "vue";
import {JobStatuses} from "@/logic/models";
import type {Dict} from "@/logic/core/types";


interface Step {
  key: string;
  name: string;
  command: string | Dict;
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
  path: 'C:\\Users\\potyk\\PycharmProjects\\automation-gae',
  steps,
}


interface Command {
  proj_id: number;
  commands: string[];
}

// @ts-ignore
const conn = new WebSocket('ws://localhost:8000/ws-run-step');

const selectedStep = ref<Step | null>(null);
const selectedStepRunning = ref<boolean>(false);

function run() {
  let step: Step | null = selectedStep.value!;
  let stepChain: Step[] = [step];
  while (step?.depends) {
    step = steps.find(s => s.key === step!.depends) ?? null;
    if (step) stepChain = [step!, ...stepChain]
  }

  const commandChain: Command = {
    commands: stepChain.flatMap(s => {
      if (typeof s.command === 'string') {
        return [s.command];
      } else {
        return s.selectedVersions!.map(v => (s.command as Dict)[v]);
      }
    }),
    proj_id: project.id,
  }


  selectedStepRunning.value = true;

  output.value = `Running ${selectedStep.value!.key}...\n`;
  conn.send(JSON.stringify(commandChain))
}

const output = ref('');

onMounted(() => {
  conn.onmessage = e => {
    let message = e.data;
    output.value += `${message}\n`;
    if (message === JobStatuses.DONE || message === JobStatuses.ERR) {
      selectedStepRunning.value = false;
    }
  };
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


    <template v-if="selectedStep">


      <v-row>
        <v-col>
          <template v-if="selectedStep.versions?.length">
            Versions:
            <template v-for="version in selectedStep.versions">
              <v-checkbox hide-details :value="version" :label="version"
                          v-model="selectedStep.selectedVersions"></v-checkbox>
            </template>
          </template>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-code style="white-space: pre-line">
            <template v-if="typeof selectedStep.command === 'string'">{{ selectedStep.command }}</template>
            <template v-else >
              {{
                selectedStep.selectedVersions
                    .map(v => selectedStep.command[v])
                    .filter(c => c)
                    .join('\n')
                || 'Не нашлось'
              }}
            </template>
          </v-code>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-btn :disabled="selectedStep.versions?.length && !selectedStep.selectedVersions?.length"
                 color="primary"
                 @click="run" :loading="selectedStepRunning">
            run
          </v-btn>
        </v-col>
      </v-row>
    </template>

    <v-row v-if="output">
      <v-col>
        <pre><v-code>{{ output }}</v-code></pre>

      </v-col>
    </v-row>

  </v-container>
</template>

<style>
</style>
