<template>
  <LoadingSpinner v-if="loadingRequest" />
  <div v-else class="relative bg-white dark:bg-gray-900 dark:text-gray-400">
    <div class="max-w-2xl mx-auto py-2 sm:px-5 lg:max-w-7xl">
      <div class="lg:grid lg:grid-cols-5 lg:gap-x-8 lg:items-start">
        <!-- Image gallery -->
        <ProductGalleryComponent :media="product.media" />

        <!-- Product info -->
        <div class="mt-8 lg:mt-0 col-span-2">
          <router-link :to="getGoBackLink()" class="text-sm tracking-tight text-gray-900 dark:text-gray-400">
            &#8592; Wróć
          </router-link>

          <h1 class="text-2xl font-semibold mt-2 tracking-tight text-gray-900 dark:text-gray-400">
            {{ product.title }}
          </h1>

          <h1 class="text-2xl font-semibold tracking-tight text-gray-900 dark:text-gray-400">
            {{ product.subtitle }}
          </h1>

          <!-- Price -->
          <div v-if="product.price && product.status !== ProductStatusEnum.RESERVED" class="mt-1">
            <h2 class="sr-only">Price</h2>
            <p class="text-md text-gray-900 dark:text-gray-400">{{ product.price.toLocaleString("pl-PL") }} zł</p>
          </div>

          <div>
            <div class="mt-2 border-t border-gray-100">
              <dl class="divide-y divide-gray-100">
                <!-- Display year -->
                <div v-if="product && 'year' in product" class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Rok</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.year }}
                  </dd>
                </div>

                <!-- Display make -->
                <div v-if="product && 'make' in product" class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Marka</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.make }}
                  </dd>
                </div>

                <!-- Display model -->
                <div v-if="product && 'model' in product" class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Model</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.model }}
                  </dd>
                </div>

                <!-- Display VIN -->
                <div v-if="product && 'vin' in product && product.vin" class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">VIN</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.vin }}
                  </dd>
                </div>

                <!-- Display odometer -->
                <div
                  v-if="product && 'odometer' in product"
                  class="py-2 sm:grid sm:grid-cols-3 sm:gap-4"
                >
                  <dt class="text-sm font-medium leading-6 text-gray-900">Przebieg</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.odometer.toLocaleString("pl-PL") }} {{ getOdometerType() }}
                  </dd>
                </div>

                <!-- Display color -->
                <div v-if="product && 'color' in product" class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Kolor</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.color }}
                  </dd>
                </div>

                <!-- Display description -->
                <div v-if="product.description && product.description.length > 0" class="py-2 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Opis</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 whitespace-pre-line">
                    {{ product.description }}
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          <form class="mt-2">
            <div>
              <router-link
                :to="{
                  name: RouteNameEnum.CONTACT,
                  query: {
                    productRef: encodeURIComponent(getCurrentHref()),
                  },
                }"
              >
                <button
                  type="button"
                  class="max-w-xs flex-1 bg-indigo-600 border border-transparent rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-50 focus:ring-indigo-500 sm:w-full"
                >
                  Skontaktuj się z nami
                </button>
              </router-link>
            </div>

            <div v-if="isAdmin()" class="mt-2 flex sm:flex-col1">
              <router-link
                class="w-full"
                :to="{ name: getProductEditRouteName(props.productType), params: { id: productId } }"
              >
                <button
                  type="button"
                  class="max-w-xs flex-1 bg-indigo-600 border border-transparent rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-50 focus:ring-indigo-500 sm:w-full"
                >
                  Edytuj
                </button>
              </router-link>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useMainStore } from "@/stores/state";
import { storeToRefs } from "pinia";
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import ProductGalleryComponent from "@/components/ProductGalleryComponent.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import { getProductEditRouteName, getProductListRouteName, RouteNameEnum } from "@/enums/routeNameEnum";
import type { IMotorcycleWithContent } from "@/interfaces/motorcycle";
import type { IMowerWithContent } from "@/interfaces/mower";
import type { IPartWithContent } from "@/interfaces/part";

const route = useRoute();
const mainStore = useMainStore();
const { isLoggedIn } = storeToRefs(mainStore);

const loadingRequest = ref(true);
const mainStateLoaded = ref(false);
const productId: any = route.params.id;
let product: IMotorcycleWithContent | IMowerWithContent | IPartWithContent;

mainStore.actionCheckLoggedIn().then(() => {
  mainStateLoaded.value = true;
});

const props = defineProps<{
  productType: ProductTypeEnum;
}>();

if (typeof productId === "string") {
  mainStore
    .getProduct(props.productType, productId)
    .then((response) => {
      product = response;
    })
    .catch((error) => {
      // TODO: Better error handling
      console.log("Something went wrong when fetching the product details.", error);
    })
    .finally(() => {
      loadingRequest.value = false;
    });
}

function isAdmin() {
  return mainStateLoaded.value && isLoggedIn.value;
}

function getOdometerType() {
  if (props.productType === ProductTypeEnum.MOTORCYCLE) {
    return "Mil";
  } else if (props.productType === ProductTypeEnum.MOWER) {
    return "Godzin";
  } else {
    return "";
  }
}

function getCurrentHref() {
  return window.location.href;
}

function getGoBackLink() {
  try {
    const previousRoute = window.history.state.back;
    if (previousRoute) {
      const url = new URL(window.location.origin + previousRoute);

      if (!(url.pathname.endsWith("edytuj") || url.pathname.endsWith("nowy"))) {
        const query: Record<string, string> = {};
        for (const [key, value] of url.searchParams) {
          query[key] = value;
        }
        return { name: getProductListRouteName(props.productType), query };
      }
    }
    return { name: getProductListRouteName(props.productType) } as const;
  } catch (error) {
    console.log("Error when trying to get the previous route", error);
    return { name: getProductListRouteName(props.productType) } as const;
  }
}
</script>
