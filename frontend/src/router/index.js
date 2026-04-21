import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/stars',
    name: 'Stars',
    component: () => import('../views/Stars.vue')
  },
  {
    path: '/stars/:id',
    name: 'StarDetail',
    component: () => import('../views/StarDetail.vue')
  },
  {
    path: '/rank',
    name: 'Rank',
    component: () => import('../views/Rank.vue')
  },
  {
    path: '/crawl',
    name: 'Crawl',
    component: () => import('../views/Crawl.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
