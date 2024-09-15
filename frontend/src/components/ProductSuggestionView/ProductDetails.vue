<template>
  <div class="flex flex-col items-start">
    <div v-if="'make' in product && product.make">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-400">Marka</h3>
      <p class="text-sm text-gray-700 dark:text-gray-400">{{ product.make }}</p>
    </div>
    <div v-if="'model' in product && product.model" class="mt-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-400">Model</h3>
      <p class="text-sm text-gray-700 dark:text-gray-400">{{ product.model }}</p>
    </div>
    <div v-if="'color' in product && product.color" class="mt-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-400">Kolor</h3>
      <p class="text-sm text-gray-700 dark:text-gray-400">{{ product.color }}</p>
    </div>
    <div class="mt-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-400">Tytuł</h3>
      <p class="text-sm text-gray-700 dark:text-gray-400">{{ product.title }}</p>
    </div>
    <div class="mt-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-400">Podtytuł</h3>
      <p class="text-sm text-gray-700 dark:text-gray-400">{{ product.subtitle }}</p>
    </div>
    <div class="mt-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-400">Opis</h3>
      <p class="text-sm text-gray-700 dark:text-gray-400 whitespace-pre-line">{{ product.description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { IMotorcycleWithContent } from "@/interfaces/motorcycle";
import type { IMowerWithContent } from "@/interfaces/mower";
import type { IPartWithContent } from "@/interfaces/part";

type ProductType = IMotorcycleWithContent | IMowerWithContent | IPartWithContent;

const props = defineProps<{
  product: ProductType;
}>();
</script>