<template>
  <div>
    <div class="aspect-w-5 aspect-h-3 w-full overflow-hidden rounded-md bg-gray-200">
      <img :src="product.medium_thumbnail_url" class="h-full w-full object-cover object-center lg:h-full lg:w-full" />
    </div>
    <div class="mt-4 flex justify-between">
      <div>
        <h3 class="font-medium text-gray-900 dark:text-gray-300">
          <a>
            {{ product.title }}
          </a>
        </h3>
        <p class="mt-1 text-gray-700 dark:text-gray-400">
          {{ product.subtitle }}
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
        <p v-if="'odometer' in product" class="mt-1 justify-end text-gray-500 dark:text-gray-400">
          {{ product.odometer.toLocaleString("pl-PL") }} {{ getOdometerType() }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import { statusToPolish } from "@/utils/status";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import type { IMotorcycle } from "@/interfaces/motorcycle";
import type { IMower } from "@/interfaces/mower";
import type { IPart } from "@/interfaces/part";

const props = defineProps({
  product: { type: Object as () => IMotorcycle | IMower | IPart, required: true },
  productType: { type: Object as () => ProductTypeEnum, required: true },
});

function getOdometerType() {
  if (props.productType === ProductTypeEnum.MOTORCYCLE) {
    return "Mil";
  } else if (props.productType === ProductTypeEnum.MOWER) {
    return "Godzin";
  } else {
    return "";
  }
}
</script>
