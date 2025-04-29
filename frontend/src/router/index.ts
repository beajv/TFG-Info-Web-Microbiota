import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import UploadView from '../views/UploadView.vue';
import DataView from '../views/DataView.vue';
import AnalyticView from '../views/AnalyticView.vue';
import SearchView from '../views/SearchView.vue';


const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'Home',
        component: HomeView,
    },
    {
        path: '/Analytic/:id',
        name: 'Analytic',
        props: true,
        component: AnalyticView
    },
    {
        path: '/data/:site',
        name: 'Data',
        props: true,
        component: DataView
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView
    },
    {
        path: '/upload',
        name: 'Upload',
        component: UploadView
    },
    {
        path: '/search/:id',
        name: 'Search',
        component: SearchView,
        props: true,
      }
];


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
  })


export default router;
