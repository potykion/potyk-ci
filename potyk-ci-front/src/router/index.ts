import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/project',
            name: 'project',
            component: () => import('../views/ProjectView.vue'),
        },
        {
            path: '/new-project',
            name: 'new-project',
            component: () => import('../views/NewProjView.vue'),
        },
    ]
})

export default router
