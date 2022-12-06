import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "motorcycleList",
      component: () => import("../views/MotorcycleListView.vue"),
    },
    {
      path: "/motorcycle/:id",

      name: "motorcycleDetail",
      component: () => import("../views/MotorcycleDetailView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "404",
      redirect: '/'
    }
  ],
});

export default router;
