import { createRouter, createWebHistory } from 'vue-router'
import diagnosticoView from '@/views/diagnosticoView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: diagnosticoView

  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [],
})

export default router
