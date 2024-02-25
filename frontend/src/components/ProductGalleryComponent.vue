<template>
  <div class="flex flex-col grow col-span-3 grid-rows-1">
    <!-- Image View -->
    <div>
      <div class="w-full h-full relative group">
        <div class="aspect-w-5 aspect-h-4">
          <div
            v-for="(image, index) in images"
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
          class="absolute left-0 top-1/2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md sm:opacity-50 group-hover:opacity-100 transition-opacity drop-shadow-lg"
          @click="selectedImage = (selectedImage - 1 + images.length) % images.length"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <button
          class="absolute right-0 top-1/2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md sm:opacity-50 group-hover:opacity-100 transition-opacity drop-shadow-lg"
          @click="selectedImage = (selectedImage + 1) % images.length"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
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
            @click.stop="selectedImage = (selectedImage - 1 + images.length) % images.length"
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
            @click.stop="selectedImage = (selectedImage + 1) % images.length"
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
          v-for="(image, index) in images"
          :key="image.thumbnail_url"
          class="relative h-24 bg-white rounded-md flex items-center justify-center cursor-pointer focus:outline-none focus:ring focus:ring-offset-4 focus:ring-opacity-50"
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
</template>
<script setup lang="ts">
import { ref } from "vue";
import type { IImage } from "@/interfaces/image";

const props = defineProps({
  images: { type: Array as () => IImage[], required: true },
});

let selectedImage = ref(0);
const modalOpen = ref(false);

function getProductImage() {
  return props.images[selectedImage.value].medium_thumbnail_url;
}
</script>
