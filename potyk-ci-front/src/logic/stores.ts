import {ref} from 'vue'
import {defineStore} from 'pinia'
import type {Project} from "@/logic/models";
import {mande} from "mande";
import {BASE_URL} from "@/logic/config";
import type {QAJob} from "@/logic/models";

export const useProjectListStore = defineStore('project', () => {
    const projects = ref<Project[]>([]);
    const loadingProjects = ref(false);

    const api = mande(BASE_URL);

    async function find(projectId: number) {
        if (!projects.value.length) await loadProjects();
        return projects.value.find(p => p.id === projectId)!;
    }

    async function loadProjects() {
        loadingProjects.value = true;
        try {
            projects.value = await api.get('/project/list');
        } finally {
            loadingProjects.value = false;
        }
    }


    const createProject = async (proj: Project) => {
        const project = await api.post('/project/create', proj) as Project;
        projects.value = [...projects.value, project];
    };


    return {projects, loadingProjects, loadProjects, createProject, find};
})


export const useSelectedProjectStore = defineStore('selected-project', () => {
    const selectedProj = ref<Project | null>(null);
    const loadingJobs = ref(false);
    const selectedProjJobs = ref<QAJob[]>([]);

    const projectListStore = useProjectListStore();

    async function select(projectId: number) {
        selectedProj.value = await projectListStore.find(projectId);
        await loadJobs();
    }

    async function loadJobs() {
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

    return {
        selectedProj,
        loadingJobs,
        selectedProjJobs,
        loadJobs,
        runJob,
        select,
    }
})