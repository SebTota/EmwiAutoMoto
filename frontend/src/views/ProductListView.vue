<template>
  <div class="relative bg-white dark:text-gray-400 dark:bg-gray-900">
    <div class="mx-auto max-w-2xl sm:px-5 lg:max-w-7xl">
      <div>
        <div class="text-center relative z-0">
          <section aria-labelledby="filter-heading" class="border-b border-gray-200 pb-2">
            <div class="flex items-center justify-between">
              <h2 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-200">{{ getPageHeader() }}</h2>

              <div class="flex items-center">
                <label for="statusFilter" class="text-sm font-medium text-gray-900 hidden sm:block">Pokaż:</label>
                <select
                  v-model="selectedStatus"
                  id="statusFilter"
                  name="statusFilter"
                  class="ml-2 block w-full pl-3 pr-10 py-2 text-small border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md bg-white text-gray-700"
                  @change="changeStatus"
                >
                  <option :value="ProductStatusEnum.FOR_SALE">Na sprzedaż</option>
                  <option :value="ProductStatusEnum.SOLD">Sprzedane</option>
                  <option :value="ProductStatusEnum.DRAFT" v-if="isAdmin">Szkic</option>
                  <option :value="ProductStatusEnum.DELETED" v-if="isAdmin">Sunięte</option>
                </select>
              </div>
            </div>
          </section>
        </div>
      </div>

      <div v-if="isLoading" class="text-center pt-4">
        <div
          class="text-center text-white bg-blue-700 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 inline-flex items-center"
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

      <div v-if="!isLoading && productListResponse">
        <div class="mt-4 grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-1 lg:grid-cols-2 xl:gap-x-8">
          <div
            v-for="product in productListResponse.products"
            :key="product.id"
            @click="getProductUrl(product.id)"
            class="hover:opacity-75"
          >
            <ProductListComponent :selected-status="selectedStatus" :product="product" />
          </div>
        </div>
        <ProductListPagination
          :hasNextPage="hasNextPage"
          :hasPrevPage="hasPrevPage"
          :nextPage="navigateToNextPage"
          :prevPage="navigateToPreviousPage"
        />
      </div>

      <div v-if="errorMessage" class="pt-4">
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span class="block sm:inline">{{ errorMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { IProductList } from '@/interfaces/product'
import { useMainStore } from '@/stores/state'
import router from '@/router'
import ProductListPagination from '@/components/ProductListPagination.vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { ProductStatusEnum } from '@/enums/productStatusEnum'
import ProductListComponent from '@/components/ProductListComponent.vue'
import { ProductTypeEnum } from '@/enums/productTypeEnum'

const route = useRoute();
const type = ref<ProductTypeEnum>(
  route.query.produkt ? (route.query.produkt as ProductTypeEnum) : ProductTypeEnum.MOTOCYKL
);
const page = ref(route.query.strona ? parseInt(route.query.strona as string) : 1);
const selectedStatus = ref<ProductStatusEnum>(
  route.query.wybranyStatus ? (route.query.wybranyStatus as ProductStatusEnum) : ProductStatusEnum.FOR_SALE
);

console.log("type", type.value);
console.log("query", route.query.produkt);
const mainState = useMainStore();
const isLoading = ref(true);
const hasNextPage = ref(false);
const hasPrevPage = ref(false);
let products = [];

let productListResponse: IProductList;
let errorMessage = ref("");

const mainStore = useMainStore();
const { isAdmin } = storeToRefs(mainStore);
const mainStateLoaded = ref(false);
mainStore.actionCheckLoggedIn().then(() => {
  mainStateLoaded.value = true;
});

onMounted(() => {
  getProductList(page.value);
});

function getPageHeader() {
  if (type.value === ProductTypeEnum.MOTOCYKL) {
    return "Motocykle";
  } else if (type.value === ProductTypeEnum.TRAKTOR) {
    return "Traktory Ogrodowe";
  } else {
    return "Produkty";
  }
}

function changeStatus() {
  router.push({
    name: "productList",
    query: {
      produkt: type.value,
      strona: 1,
      wybranyStatus: selectedStatus.value,
    },
  });
}

function getProductList(page: number) {
  let showStatus = [selectedStatus.value];
  if (selectedStatus.value === ProductStatusEnum.SOLD) {
    showStatus = [ProductStatusEnum.SOLD, ProductStatusEnum.RESERVED];
  }

  isLoading.value = true;
  mainState
    .getProducts(type.value, page, showStatus)
    .then((response: IProductList) => {
      productListResponse = response;
      products = response.products;
      hasNextPage.value = productListResponse.has_next_page;
      hasPrevPage.value = productListResponse.page > 1;
      isLoading.value = false;
    })
    .catch((err) => {
      isLoading.value = false;
      errorMessage.value = "Coś poszło nie tak. Spróbuj ponownie później.";
      console.log("Failed to load products.", err);
    });
}

function getProductUrl(productId: string) {
  router.push({ name: "productDetails", params: { id: productId } });
}

function navigateToNextPage() {
  if (productListResponse.has_next_page) {
    router.push({
      name: "productList",
      query: {
        produkt: type.value,
        strona: productListResponse.page + 1,
        wybranyStatus: selectedStatus.value,
      },
    });
  }
}

function navigateToPreviousPage() {
  if (productListResponse.page > 1) {
    router.push({
      name: "productList",
      query: {
        produkt: type.value,
        strona: productListResponse.page - 1,
        wybranyStatus: selectedStatus.value,
      },
    });
  }
}
</script>
