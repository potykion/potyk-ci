import {ref, computed} from 'vue'
import {defineStore} from 'pinia'
import type {Project} from "@/logic/models";

export const useProjectStore = defineStore('project', () => {

    const projects = ref<Project[]>([]);
    const loadingProjects = ref(false);


    async function loadProjects() {
        loadingProjects.value = true;
        try {
            const resp = await fetch('http://127.0.0.1:8000/project/list');
            projects.value = await resp.json();
        } finally {
            loadingProjects.value = false;
        }
    }

    return {projects, loadingProjects, loadProjects};
})


