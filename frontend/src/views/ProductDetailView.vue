<template>
  <div v-if="loadingRequest" class="text-center">
    <div
      class="text-center text-white bg-blue-700 font-medium rounded-lg text-sm px-5 py-2.5 my-6 mr-2 inline-flex items-center"
    >
      <svg
        class="inline mr-3 w-4 h-4 text-white animate-spin"
        viewBox="0 0 100 101"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
          fill="#E5E7EB"
        />
        <path
          d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
          fill="currentColor"
        />
      </svg>
      Ładowanie...
    </div>
  </div>

  <div v-else class="relative bg-white dark:bg-gray-900 dark:text-gray-400">
    <div class="max-w-2xl mx-auto py-2 sm:px-5 lg:max-w-7xl">
      <div class="lg:grid lg:grid-cols-5 lg:gap-x-8 lg:items-start">
        <!-- Image gallery -->
        <div class="flex flex-col grow col-span-3 grid-rows-1">
          <!-- Image View -->
          <div>
            <div class="w-full h-full relative group">
              <div class="aspect-w-5 aspect-h-3">
                <div
                  v-for="(image, index) in product.images"
                  :key="image.medium_thumbnail_url"
                  v-show="selectedImage === index"
                >
                  <img
                    :src="image.medium_thumbnail_url"
                    @click="modalOpen = true"
                    class="w-full h-full object-center object-cover sm:rounded-lg"
                    alt="Product Image"
                  />
                </div>
              </div>

              <button
                class="absolute left-0 top-1/2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md sm:opacity-0 group-hover:opacity-100 transition-opacity drop-shadow-lg"
                @click="selectedImage = (selectedImage - 1 + product.images.length) % product.images.length"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  class="h-6 w-6"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>

              <button
                class="absolute right-0 top-1/2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md sm:opacity-0 group-hover:opacity-100 transition-opacity drop-shadow-lg"
                @click="selectedImage = (selectedImage + 1) % product.images.length"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  class="h-6 w-6"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Modal View -->
          <div
            v-show="modalOpen"
            @click="modalOpen = false"
            class="fixed inset-0 overflow-y-auto z-10 w-full h-full bg-stone-100"
          >
            <div class="flex items-center justify-center min-h-screen w-full h-full">
              <div
                class="absolute top-0 right-0 p-4 cursor-pointer text-black text-l font-semibold"
                @click.stop="modalOpen = false"
              >
                Zamknij
              </div>

              <div class="p-2 md:p-8 relative group">
                <img :src="getProductImage()" @click.stop="" class="w-full h-full object-contain rounded-md drop-shadow-lg" />

                <button
                  class="absolute top-1/2 left-2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md drop-shadow-lg"
                  @click.stop="selectedImage = (selectedImage - 1 + product.images.length) % product.images.length"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    class="h-6 w-6"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                  </svg>
                </button>

                <button
                  class="absolute top-1/2 right-2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md drop-shadow-lg"
                  @click.stop="selectedImage = (selectedImage + 1) % product.images.length"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    class="h-6 w-6"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Image selector -->
          <div class="mt-4 w-full mx-auto sm:block">
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              <div
                v-for="(image, index) in product.images"
                :key="image.thumbnail_url"
                class="relative h-24 bg-white rounded-md flex items-center justify-center text-sm font-medium uppercase text-gray-900 dark:text-gray-400 cursor-pointer hover:bg-gray-50 focus:outline-none focus:ring focus:ring-offset-4 focus:ring-opacity-50"
                @click="selectedImage = index"
              >
                <span class="absolute inset-0 rounded-md overflow-hidden">
                  <img :src="image.thumbnail_url" alt="" class="w-full h-full object-center object-cover" />
                </span>
                <span
                  :class="[
                    selectedImage === index ? 'ring-indigo-500' : 'ring-transparent',
                    'absolute inset-0 rounded-md ring-2 ring-offset-2 pointer-events-none',
                  ]"
                  aria-hidden="true"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Product info -->
        <div class="mt-8 lg:mt-0 col-span-2">
          <router-link :to="getGoBackLink()" class="text-sm tracking-tight text-gray-900 dark:text-gray-400">
            &#8592; Wróć
          </router-link>

          <h1 class="text-3xl font-extrabold mt-2 tracking-tight text-gray-900 dark:text-gray-400">
            {{ product.year + " " + product.make + " " + product.model }}
          </h1>

          <!-- Price -->
          <div v-if="product.price && product.status !== ProductStatusEnum.RESERVED" class="mt-1">
            <h2 class="sr-only">Price</h2>
            <p class="text-2xl text-gray-900 dark:text-gray-400">{{ product.price.toLocaleString("pl-PL") }} zł</p>
          </div>

          <div>
            <div class="mt-2 border-t border-gray-100">
              <dl class="divide-y divide-gray-100">
                <div class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Rok</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.year }}
                  </dd>
                </div>
                <div class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Marka</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.make }}
                  </dd>
                </div>
                <div class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Model</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.model }}
                  </dd>
                </div>
                <div v-if="product.vin" class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">VIN</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.vin }}
                  </dd>
                </div>
                <div class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Przebieg</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ product.odometer.toLocaleString("pl-PL") }} {{ product.odometer_type }}
                  </dd>
                </div>
                <div class="py-2 sm:grid sm:grid-cols-3 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Kolor</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">
                    {{ colorToPolish(product.color) }}
                  </dd>
                </div>
                <div v-if="product.description" class="py-2 sm:gap-4">
                  <dt class="text-sm font-medium leading-6 text-gray-900">Opis</dt>
                  <dd class="mt-1 text-sm leading-6 text-gray-700">
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
                  name: 'contact',
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
              <router-link class="w-full" :to="{ name: 'productEdit', params: { id: productId } }">
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
import type { IProductWithImages } from "@/interfaces/product";
import { colorToPolish } from "@/utils/colors";
import { storeToRefs } from "pinia";
import { ProductStatusEnum } from "@/enums/productStatusEnum";

const route = useRoute();
const mainStore = useMainStore();
const { isLoggedIn } = storeToRefs(mainStore);

const loadingRequest = ref(true);
const mainStateLoaded = ref(false);
const productId: any = route.params.id;
let product: IProductWithImages;
let selectedImage = ref(0);
const modalOpen = ref(false);

mainStore.actionCheckLoggedIn().then(() => {
  mainStateLoaded.value = true;
});

function getProductImage() {
  return product.images[selectedImage.value].medium_thumbnail_url;
}

if (typeof productId === "string") {
  mainStore
    .getProduct(productId)
    .then((response) => {
      product = response;
    })
    .finally(() => {
      loadingRequest.value = false;
    });
}

function isAdmin() {
  return mainStateLoaded.value && isLoggedIn.value;
}

function getCurrentHref() {
  return window.location.href;
}

function getGoBackLink() {
  const previousRoute = window.history.state.back;
  const url = new URL(window.location.origin + previousRoute);

  if (url.pathname === "/produkty") {
    const query: Record<string, string> = {};

    for (const [key, value] of url.searchParams) {
      query[key] = value;
    }

    return { path: previousRoute, query };
  } else {
    return { name: "productList" } as const;
  }
}
</script>
