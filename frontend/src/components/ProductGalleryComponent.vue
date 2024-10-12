<template>
  <div class="flex flex-col grow col-span-3 grid-rows-1">
    <!-- Image View -->
    <div>
      <div class="w-full h-full relative group">
        <div class="aspect-w-5 aspect-h-4">
          <div
            v-for="(media_obj, index) in media"
            :key="media_obj.medium_thumbnail_url"
            v-show="selectedImageIndex === index"
            @click="modalOpen = true"
          >
            <img
              loading="lazy"
              :src="media_obj.medium_thumbnail_url"
              class="w-full h-full object-center object-cover sm:rounded-lg"
              alt="Product Image"
            />
            <div
              v-if="media_obj.type == MediaTypeEnum.YOUTUBE_VIDEO"
              class="absolute inset-0 m-auto h-24 w-24 bg-white bg-opacity-50 rounded-md"
            >
              <img src="/icons/play-button.png" class="p-6" />
            </div>
          </div>
        </div>

        <button
          class="absolute left-0 top-1/2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md sm:opacity-50 group-hover:opacity-100 transition-opacity drop-shadow-lg"
          @click="selectedImageIndex = (selectedImageIndex - 1 + media.length) % media.length"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <button
          class="absolute right-0 top-1/2 transform -translate-y-1/2 m-1 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md sm:opacity-50 group-hover:opacity-100 transition-opacity drop-shadow-lg"
          @click="selectedImageIndex = (selectedImageIndex + 1) % media.length"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <div class="absolute right-0 bottom-0 m-1 p-2 bg-white rounded-md drop-shadow-lg">
          <p class="text-xs">{{ selectedImageIndex + 1 + " / " + media.length }}</p>
        </div>
      </div>
    </div>

    <!-- Modal View -->
    <div
      v-if="modalOpen"
      @click="modalOpen = false"
      class="fixed inset-0 overflow-y-auto z-10 w-full h-full bg-stone-100"
    >
      <div class="flex items-center justify-center h-screen w-full">
        <div class="p-2 max-w-5xl h-full w-full md:h-5/6 md:w-11/12 flex items-center justify-center">
          <img
            v-if="getProductImage().type === MediaTypeEnum.IMAGE"
            :src="getProductImage().medium_thumbnail_url"
            @click.stop=""
            class="rounded-md drop-shadow-lg w-full h-full object-contain"
          />
          <iframe
            v-else
            :src="getProductImage().url"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            class="w-full"
            style="aspect-ratio: 16/9"
          ></iframe>

          <button
            class="absolute top-1/2 left-0 transform -translate-y-1/2 m-4 md:m-8 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md drop-shadow-lg"
            @click.stop="selectedImageIndex = (selectedImageIndex - 1 + media.length) % media.length"
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
            class="absolute top-1/2 right-0 transform -translate-y-1/2 m-4 md:m-8 p-2 bg-white hover:bg-gray-800 hover:text-white rounded-md drop-shadow-lg"
            @click.stop="selectedImageIndex = (selectedImageIndex + 1) % media.length"
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

          <div class="absolute bottom-0 right-0 m-4 md:m-8 p-2 bg-white rounded-md drop-shadow-lg">
            <p class="text-xs">{{ selectedImageIndex + 1 + " / " + media.length }}</p>
          </div>
        </div>
        <div
          class="absolute top-0 right-0 m-4 md:m-8 p-2 cursor-pointer bg-white hover:bg-gray-800 hover:text-white rounded-md drop-shadow-lg"
          @click.stop="modalOpen = false"
        >
          <div class="p-2 text-l font-semibold">Zamknij</div>
        </div>
      </div>
    </div>

    <!-- Image selector -->
    <div class="mt-4 w-full mx-auto sm:block">
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        <div
          v-for="(media_obj, index) in media"
          :key="media_obj.thumbnail_url"
          class="relative h-24 bg-white rounded-md flex items-center justify-center cursor-pointer focus:outline-none focus:ring focus:ring-offset-4 focus:ring-opacity-50"
          @click="selectedImageIndex = index"
        >
          <span class="absolute inset-0 rounded-md overflow-hidden">
            <img :src="media_obj.thumbnail_url" alt="" class="w-full h-full object-center object-cover" />
            <div
              v-if="media_obj.type == MediaTypeEnum.YOUTUBE_VIDEO"
              class="absolute inset-0 m-auto h-16 w-16 bg-white bg-opacity-50 rounded-md"
            >
              <img src="/icons/play-button.png" class="p-4" />
            </div>
          </span>
          <span
            :class="[
              selectedImageIndex === index ? 'ring-indigo-500' : 'ring-transparent',
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
import type { IMedia } from "@/interfaces/media";
import { MediaTypeEnum } from "@/enums/mediaTypeEnum";

const props = defineProps({
  media: { type: Array as () => IMedia[], required: true },
});

let selectedImageIndex = ref(0);
const modalOpen = ref(false);

function getProductImage() {
  return props.media[selectedImageIndex.value];
}
</script>
