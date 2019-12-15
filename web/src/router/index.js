import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import('@/views/Login.vue')
  },
  {
    path: "/403",
    name: "forbidden",
    component: () => import('@/views/Forbidden.vue')
  },
];

const router = new VueRouter({
  mode: "history",
  routes
});

export default router
