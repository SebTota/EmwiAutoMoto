import { createRouter, createWebHistory } from "vue-router";
import { useMainStore } from "@/stores/state";
import { ProductTypeEnum } from '@/enums/productTypeEnum'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/motocykle",
      name: ProductTypeEnum.MOTORCYCLE,
      component: () => import("../views/ProductListView.vue"),
      props: { productType: ProductTypeEnum.MOTORCYCLE },
    },
    {
      path: "/traktory-ogrodowe",
      name: ProductTypeEnum.MOWER,
      component: () => import("../views/ProductListView.vue"),
      props: { productType: ProductTypeEnum.MOWER },
    },
    {
      path: "/produkt/nowy",
      name: "newProduct",
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: (to, from, next) => {
        const mainState = useMainStore();
        mainState.actionCheckLoggedIn().then(() => {
          if (mainState.isLoggedIn) {
            next();
          } else {
            next({ name: "login" });
          }
        });
      },
    },
    {
      path: "/motocykle/:id/edytuj",
      name: "productEdit",
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: (to, from, next) => {
        const mainState = useMainStore();
        mainState.actionCheckLoggedIn().then(() => {
          if (mainState.isLoggedIn) {
            next();
          } else {
            next({ name: "login" });
          }
        });
      },
    },
    {
      path: "/motocykle/:id",
      name: "productDetails",
      component: () => import("../views/ProductDetailView.vue"),
    },
    {
      path: "/kontakt",
      name: "contact",
      component: () => import("../views/ContactPageView.vue"),
    },
    {
      path: "/",
      name: "home",
      redirect: "/motocykle",
    },
    {
      path: "/:pathMatch(.*)*",
      name: "404",
      component: () => import("../views/NotFound.vue"),
    },
  ],
});

export default router;
