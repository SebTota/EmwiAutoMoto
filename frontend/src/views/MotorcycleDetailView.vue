<template>
  <div v-if="loadingRequest" class="text-center">
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
      Loading...
    </div>
  </div>

  <div v-else class="bg-white dark:bg-gray-900 dark:text-gray-400">
    <div
      class="max-w-2xl mx-auto py-2 px-4 sm:py-12 sm:px-6 lg:max-w-7xl lg:px-8"
    >
      <div class="lg:grid lg:grid-cols-5 lg:gap-x-8 lg:items-start">
        <!-- Image gallery -->
        <TabGroup as="div" class="flex flex-col grow col-span-3 grid-rows-1">
          <!-- Image View -->
          <TabPanels class="w-full aspect-w-5 aspect-h-3">
            <TabPanel v-for="image in product.images" :key="image.image_url">
              <img
                :src="image.image_url"
                class="w-full h-full object-center object-cover sm:rounded-lg"
              />
            </TabPanel>
          </TabPanels>
          <!-- Image selector -->
          <div class="mt-6 w-full max-w-2xl mx-auto sm:block">
            <TabList class="grid grid-cols-3 md:grid-cols-4 gap-3">
              <Tab
                v-for="image in product.images"
                :key="image.thumbnail_url"
                class="relative h-24 bg-white rounded-md flex items-center justify-center text-sm font-medium uppercase text-gray-900 dark:text-gray-400 cursor-pointer hover:bg-gray-50 focus:outline-none focus:ring focus:ring-offset-4 focus:ring-opacity-50"
                v-slot="{ selected }"
              >
                <span class="absolute inset-0 rounded-md overflow-hidden">
                  <img
                    :src="image.thumbnail_url ? image.thumbnail_url : undefined"
                    alt=""
                    class="w-full h-full object-center object-cover"
                  />
                </span>
                <span
                  :class="[
                    selected ? 'ring-indigo-500' : 'ring-transparent',
                    'absolute inset-0 rounded-md ring-2 ring-offset-2 pointer-events-none',
                  ]"
                  aria-hidden="true"
                />
              </Tab>
            </TabList>
          </div>
        </TabGroup>

        <!-- Product info -->
        <div class="mt-10 px-4 sm:px-0 sm:mt-16 lg:mt-0 col-span-2">
          <a
            class="text-sm tracking-tight text-gray-900 dark:text-gray-400"
            href="#"
            @click="goBack"
            >&#8592;Wszystkie Motocykle</a
          >
          <h1
            class="text-3xl font-extrabold tracking-tight text-gray-900 dark:text-gray-400"
          >
            {{ product.make + " " + product.model }}
          </h1>

          <!-- Price -->
          <div class="mt-1">
            <h2 class="sr-only">Price</h2>
            <p class="text-3xl text-gray-900 dark:text-gray-400">
              {{ product.price }} zł
            </p>
          </div>


          <hr />

          <!-- Odometer -->
          <div class="mt-5">
            <h3 class="sr-only">Odometer</h3>
            <p class="text-l text-gray-900 dark:text-gray-400">
              Drogomierz: {{ product.odometer_miles }} mill
            </p>
          </div>

          <!-- Colors -->
          <div class="mt-1">
            <h3 class="sr-only">Color</h3>
            <p class="text-l text-gray-900 dark:text-gray-400">
              Kolor: {{ colorToPolish(product.color) }}
            </p>
            <div
              :class="[
                colorCss,
                'h-8 w-8 border border-black border-opacity-50 rounded-full',
              ]"
            />
          </div>
          <div class="mt-6">
            <!-- Description -->
            <h3 class="sr-only">Description</h3>
            <div
              class="text-base text-gray-700 dark:text-gray-200 space-y-6"
              v-html="product.description"
            />
          </div>

          <form class="mt-6">
            <div class="mt-10 flex sm:flex-col1">
              <button
                type="submit"
                @click="goToContactPage"
                class="max-w-xs flex-1 bg-indigo-600 border border-transparent rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-50 focus:ring-indigo-500 sm:w-full"
              >
                Skontaktuj się z nami
              </button>
            </div>
            <div v-if="isAdmin()" class="mt-2 flex sm:flex-col1">
              <button
                type="submit"
                @click="goToEditMotorcyclePage"
                class="max-w-xs flex-1 bg-indigo-600 border border-transparent rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-50 focus:ring-indigo-500 sm:w-full"
              >
                Edytuj motocykl
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from "@headlessui/vue";
import { useRoute } from "vue-router";
import { useMainStore } from "@/stores/state";
import type { IMotorcycleWithImages } from "@/interfaces/motorcycle";
import { colorToPolish, getCssClassFromColor } from "@/utils/colors";
import router from "@/router";
import { storeToRefs } from "pinia";

const route = useRoute();
const mainStore = useMainStore();
const { isLoggedIn } = storeToRefs(mainStore);

const loadingRequest = ref(true);
const mainStateLoaded = ref(false);
const motorcycleId: any = route.params.id;
let product: IMotorcycleWithImages;
let colorCss: string;

mainStore.actionCheckLoggedIn().then(() => {
  mainStateLoaded.value = true;
});

if (typeof motorcycleId === "string") {
  mainStore.getMotorcycle(motorcycleId).then((response) => {
    product = response;
    colorCss = getCssClassFromColor(product.color);
    loadingRequest.value = false;
  });
}

function goBack() {
  // TODO: Save the last search preferences (page, filters, etc.) in local storage and reference them here
  router.push({ name: "motorcycleList" });
}

function goToContactPage(event: any) {
  event.preventDefault();
  router.push({
    name: "contact",
    query: { motorcycleRef: encodeURIComponent(window.location.href) },
  });
}

function goToEditMotorcyclePage(event: any) {
  event.preventDefault();
  router.push({ name: "motorcycleEdit", params: { id: motorcycleId } });
}

function isAdmin() {
  return mainStateLoaded.value && isLoggedIn.value;
}
</script>
