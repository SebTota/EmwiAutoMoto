import { createRouter, createWebHistory } from "vue-router";
import {useMainStore} from "@/stores/state";

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
      path: "/motorcycle/new",
      name: "newMotorcycle",
      component: () => import("../views/MotorcycleAdminView.vue"),
      beforeEnter: (to, from, next) => {
        const mainState = useMainStore();
        mainState.actionCheckLoggedIn().then(() => {
          if (mainState.isLoggedIn) {
            next();
          } else {
            next({name: 'login'})
          }
        })
      }
    },
    {
      path: "/motorcycle/:id/edit",
      name: "motorcycleEdit",
      component: () => import("../views/MotorcycleAdminView.vue"),
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
