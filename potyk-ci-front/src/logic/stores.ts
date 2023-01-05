import {computed, ref} from 'vue'
import {defineStore} from 'pinia'
import type {Project} from "@/logic/models";
import {mande} from "mande";
import {BASE_URL} from "@/logic/config";
import type {Job} from "@/logic/models";
import {JobVM} from "@/logic/vm";

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
    const _selectedProjJobs = ref<Job[]>([]);

    const selectedProjJobs = computed(
        () => _selectedProjJobs.value.map(j => new JobVM(j))
    )

    const projectListStore = useProjectListStore();

    async function select(projectId: number) {
        selectedProj.value = await projectListStore.find(projectId);
        await loadJobs();
    }

    async function loadJobs() {
        loadingJobs.value = true;

        try {
            const resp = await fetch(`http://127.0.0.1:8000/qa_job/list_for_project?project_id=${selectedProj.value!.id}`);
            _selectedProjJobs.value = await resp.json();
        } finally {
            loadingJobs.value = false;
        }
    }

    async function scheduleJob() {
        const resp = await fetch(`http://127.0.0.1:8000/project/schedule?project_id=${selectedProj.value!.id}`);
        const job = await resp.json()
        _selectedProjJobs.value = [job, ...selectedProjJobs.value];
    }

    return {
        selectedProj,
        loadingJobs,
        selectedProjJobs,
        loadJobs,
        scheduleJob,
        select,
    }
})