<template>
  <div class="relative bg-white dark:text-gray-400 dark:bg-gray-900">
    <div class="mx-auto sm:px-5">
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

      <LoadingSpinner v-if="loadingRequest" class="pt-4" />

      <div v-if="!loadingRequest && productListResponse">
        <div class="mt-4 grid gap-y-10 gap-x-6 grid-cols-1 md:grid-cols-2 xl:grid-cols-3 xl:gap-x-8">
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
import LoadingSpinner from '@/components/LoadingSpinner.vue'

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
const loadingRequest = ref(true);
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

  loadingRequest.value = true;
  mainState
    .getProducts(type.value, page, showStatus)
    .then((response: IProductList) => {
      productListResponse = response;
      products = response.products;
      hasNextPage.value = productListResponse.has_next_page;
      hasPrevPage.value = productListResponse.page > 1;
      loadingRequest.value = false;
    })
    .catch((err) => {
      loadingRequest.value = false;
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
