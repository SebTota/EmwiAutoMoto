import { createRouter, createWebHistory } from "vue-router";
import { useMainStore } from "@/stores/state";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import { RouteNameEnum } from "@/enums/routeNameEnum";

const authGuard = (to: any, from: any, next: any) => {
  const mainState = useMainStore();
  mainState.actionCheckLoggedIn().then(() => {
    if (mainState.isLoggedIn) {
      next();
    } else {
      next({ name: RouteNameEnum.LOGIN });
    }
  });
};

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: RouteNameEnum.HOME,
      component: () => import("../views/Home.vue"),
    },
    {
      path: "/login",
      name: RouteNameEnum.LOGIN,
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/kontakt",
      name: RouteNameEnum.CONTACT,
      component: () => import("../views/ContactPageView.vue"),
    },
    // Motorcycle routes
    {
      path: "/motocykle/nowy",
      name: RouteNameEnum.NEW_MOTORCYCLE,
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: authGuard,
      props: {
        productType: ProductTypeEnum.MOTORCYCLE,
        isNewProduct: true,
      },
    },
    {
      path: "/motocykle/:id/edytuj",
      name: RouteNameEnum.EDIT_MOTORCYCLE,
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: authGuard,
      props: route => ({
        productType: ProductTypeEnum.MOTORCYCLE,
        isNewProduct: false,
        id: route.params.id
      }),
    },
    {
      path: "/motocykle/:id/przeglad-sugestii-produktu",
      name: RouteNameEnum.MOTORCYCLE_DETAIL_SUGGESTIONS,
      component: () => import("../views/ProductSuggestionView.vue"),
      beforeEnter: authGuard,
      props: route => ({
        productType: ProductTypeEnum.MOTORCYCLE,
        id: route.params.id
      }),
    },
    {
      path: "/motocykle/:id",
      name: RouteNameEnum.MOTORCYCLE_DETAILS,
      component: () => import("../views/ProductDetailView.vue"),
      props: route => ({
        productType: ProductTypeEnum.MOTORCYCLE,
        id: route.params.id
      }),
    },
    {
      path: "/motocykle",
      name: RouteNameEnum.MOTORCYCLE_LIST,
      component: () => import("../views/ProductListView.vue"),
      props: { productType: ProductTypeEnum.MOTORCYCLE },
    },
    // Mower routes
    {
      path: "/traktory-ogrodowe/nowy",
      name: RouteNameEnum.NEW_MOWER,
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: authGuard,
      props: {
        productType: ProductTypeEnum.MOWER,
        isNewProduct: true,
      },
    },
    {
      path: "/traktory-ogrodowe/:id/edytuj",
      name: RouteNameEnum.EDIT_MOWER,
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: authGuard,
      props: route => ({
        productType: ProductTypeEnum.MOWER,
        isNewProduct: false,
        id: route.params.id
      }),
    },
    {
      path: "/traktory-ogrodowe/:id",
      name: RouteNameEnum.MOWER_DETAILS,
      component: () => import("../views/ProductDetailView.vue"),
      props: route => ({
        productType: ProductTypeEnum.MOWER,
        id: route.params.id
      }),
    },
    {
      path: "/traktory-ogrodowe",
      name: RouteNameEnum.MOWER_LIST,
      component: () => import("../views/ProductListView.vue"),
      props: { productType: ProductTypeEnum.MOWER },
    },
    // Parts routes
    {
      path: "/czesci-i-akcesoria/nowy",
      name: RouteNameEnum.NEW_PART,
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: authGuard,
      props: {
        productType: ProductTypeEnum.PART,
        isNewProduct: true,
      },
    },
    {
      path: "/czesci-i-akcesoria/:id/edytuj",
      name: RouteNameEnum.EDIT_PART,
      component: () => import("../views/ProductAdminView.vue"),
      beforeEnter: authGuard,
      props: route => ({
        productType: ProductTypeEnum.PART,
        isNewProduct: false,
        id: route.params.id
      }),
    },
    {
      path: "/czesci-i-akcesoria/:id",
      name: RouteNameEnum.PART_DETAILS,
      component: () => import("../views/ProductDetailView.vue"),
      props: route => ({
        productType: ProductTypeEnum.PART,
        id: route.params.id
      }),
    },
    {
      path: "/czesci-i-akcesoria",
      name: RouteNameEnum.PART_LIST,
      component: () => import("../views/ProductListView.vue"),
      props: { productType: ProductTypeEnum.PART },
    },
    // 404 route
    {
      path: "/:pathMatch(.*)*",
      name: "404",
      component: () => import("../views/NotFound.vue"),
    },
  ],
});

export default router;