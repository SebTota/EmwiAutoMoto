import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/motorcycles",
      name: "motorcycleList",
      component: () => import("../views/MotorcycleListView.vue"),
    },
    {
      path: "/motorcycle/:id",
      name: "motorcycleDetail",
      component: () => import("../views/MotorcycleDetailView.vue"),
    },
    {
      path: "/contact",
      name: "contact",
      component: () => import("../views/ContactPageView.vue"),
    },
    {
      path: "/",
      name: "home",
      redirect: '/motorcycles'
    },
    {
      path: "/:pathMatch(.*)*",
      name: "404",
      component: () => import("../views/NotFound.vue")
    }
  ],
});

export default router;
