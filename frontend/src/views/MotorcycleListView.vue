<template>
  <div class="bg-white dark:text-gray-400 dark:bg-gray-900">
    <div class="mx-auto max-w-2xl py-16 px-4 sm:px-6 lg:max-w-7xl lg:px-8">
      <h2 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-200">Motocykle</h2>

      <div v-if="isLoadingMotorcycles" class="text-center">
        <div class="text-center text-white bg-blue-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 inline-flex items-center">
            <svg class="inline mr-3 w-4 h-4 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
            </svg>
            Loading...
        </div>
      </div>

      <div v-else>
        <div class="mt-6 grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-1 lg:grid-cols-2 xl:gap-x-8">
          <div v-for="product in motorcycleResponse.motorcycles" :key="product.id"
               @click="getProductUrl(product.id)" class="hover:opacity-75">
            <div class="min-h-80 aspect-w-5 aspect-h-3 w-full overflow-hidden rounded-md bg-gray-200 lg:aspect-none lg:h-80">
              <img :src="product.medium_thumbnail_url" class="h-full w-full object-cover object-center lg:h-full lg:w-full" />
            </div>
            <div class="mt-4 flex justify-between">
              <div>
                <h3 class="text-medium font-medium text-gray-900 dark:text-gray-300">
                  <a>
                    {{ product.make + ' ' + product.model }}
                  </a>
                </h3>
                <p class="mt-1 text-medium text-gray-500 dark:text-gray-400">{{colorToPolish(product.color)}}</p>
              </div>
              <p class="text-medium font-medium text-gray-900 dark:text-gray-300">{{ product.price }}</p>
            </div>
          </div>
        </div>
        <MotorcycleListPagination :hasNextPage="hasNextPage"
                                :hasPrevPage="hasPrevPage"
                                :nextPage="navigateToNextPage"
                                :prevPage="navigateToPreviousPage"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";

import type {IMotorcycleList} from "@/interfaces/motorcycle";
import {useMainStore} from "@/stores/state";
import router from "@/router";
import MotorcycleListPagination from "@/components/MotorcycleListPagination.vue";
import {colorToPolish} from "@/utils/colors";
import {useRoute} from "vue-router";

const route = useRoute();
const page: any = route.query.page ? parseInt(route.query.page as string) : 1;

const mainState = useMainStore();
const isLoadingMotorcycles = ref(true);
const hasNextPage = ref(false);
const hasPrevPage = ref(false);
let products = [];

let motorcycleResponse: IMotorcycleList;
let errorMessage = null;

function updateMotorcycles(page: number) {
  isLoadingMotorcycles.value = true;
  mainState.getMotorcycles(page).then((motorcycleListResponse: IMotorcycleList) => {
    motorcycleResponse = motorcycleListResponse;
    products = motorcycleListResponse.motorcycles;
    hasNextPage.value = motorcycleResponse.has_next_page;
    hasPrevPage.value = motorcycleResponse.page > 1;
    isLoadingMotorcycles.value = false;
  }).catch(err => {
    errorMessage = "Uh oh. Something went wrong. Please try again later.";
    console.log('Failed to load motorcycles', err);
  })
}

function getProductUrl(productId: string) {
  router.push({ name: 'motorcycleDetail', params: { id: productId } })
}

function navigateToNextPage() {
  if (motorcycleResponse.has_next_page) {
      router.push({name: 'motorcycleList', query: {
        page: motorcycleResponse.page + 1
      }})
  }
}

function navigateToPreviousPage() {
  if (motorcycleResponse.page > 1) {
    router.push({name: 'motorcycleList', query: {
        page: motorcycleResponse.page - 1
      }})
  }
}

updateMotorcycles(page);
</script>