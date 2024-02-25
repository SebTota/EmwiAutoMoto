<template>
  <div>
    <div class="aspect-w-5 aspect-h-3 w-full overflow-hidden rounded-md bg-gray-200">
      <img :src="product.medium_thumbnail_url" class="h-full w-full object-cover object-center lg:h-full lg:w-full" />
    </div>
    <div class="mt-4 flex justify-between">
      <div>
        <h3 class="font-medium text-gray-900 dark:text-gray-300">
          <a>
            {{ product.year + " " + product.make }}
          </a>
        </h3>
        <p class="mt-1 text-gray-700 dark:text-gray-400">
          {{ product.model }}
        </p>
      </div>
      <div class="text-right">
        <p
          v-if="product.price && product.status === ProductStatusEnum.SOLD"
          class="font-medium text-gray-900 dark:text-gray-300"
        >
          {{ statusToPolish(product.status) + " - " + product.price.toLocaleString("pl-PL") }} zł
        </p>
        <p
          v-else-if="product.status === ProductStatusEnum.RESERVED"
          class="font-medium text-gray-900 dark:text-gray-300"
        >
          {{ statusToPolish(product.status) }}
        </p>
        <p v-else-if="product.price" class="font-medium text-gray-900 dark:text-gray-300">
          {{ product.price.toLocaleString("pl-PL") }} zł
        </p>
        <p v-else class="font-medium text-gray-900 dark:text-gray-300">
          {{ statusToPolish(product.status) }}
        </p>
        <p class="mt-1 justify-end text-gray-500 dark:text-gray-400">
          {{ product.odometer.toLocaleString("pl-PL") }} {{ product.odometer_type }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import type { IProduct } from "@/interfaces/product";
import { statusToPolish } from "@/utils/status";

const props = defineProps({
  product: { type: Object as () => IProduct, required: true },
  selectedStatus: { type: Object as () => ProductStatusEnum, required: true },
});
</script>
