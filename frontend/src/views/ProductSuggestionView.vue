<template>
  <div class="py-2 sm:px-5">
    <h1 class="text-3xl font-semibold text-gray-900 dark:text-gray-400 mb-4">Porównaj sugestie</h1>
    <LoadingSpinner v-if="loadingCurrentProductRequest || loadingSuggestionRequest" />
    <div v-else-if="currentProduct && productSuggestion" class="mx-auto grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Original Content -->
      <div class="flex flex-col items-start bg-white dark:bg-gray-900 dark:text-gray-400 p-4 rounded-md shadow-md">
        <h2 class="text-xl font-semibold mb-2">Oryginał</h2>
        <ProductDetails :product="currentProduct" />
      </div>

      <!-- Suggested Content -->
      <div class="flex flex-col items-start bg-white dark:bg-gray-900 dark:text-gray-400 p-4 rounded-md shadow-md">
        <h2 class="text-xl font-semibold mb-2">Sugestia</h2>
        <ProductDetails :product="productSuggestion" />
      </div>
    </div>

    <!-- Action Buttons -->
    <div v-if="currentProduct && productSuggestion" class="mt-6 flex flex-col md:flex-row md:justify-between">
      <button
        class="bg-red-600 text-white font-medium py-2 px-4 rounded-md hover:bg-red-700 mb-4 md:mb-0 md:mr-4"
        @click="keepOriginal"
      >
        Zachowaj oryginał
      </button>
      <button
        class="bg-green-600 text-white font-medium py-2 px-4 rounded-md hover:bg-green-700"
        @click="takeSuggestion"
      >
        Przyjmij sugestię
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { type IMotorcycleWithContent, updateMotorcycle } from "@/interfaces/motorcycle";
import { type IMowerWithContent, updateMower } from "@/interfaces/mower";
import { type IPartWithContent, updatePart } from "@/interfaces/part";
import { useMainStore } from "@/stores/state";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import ProductDetails from "@/components/ProductSuggestionView/ProductDetails.vue";
import { RouteNameEnum } from "@/enums/routeNameEnum";

const route = useRoute();
const router = useRouter();
const mainStore = useMainStore();

const loadingCurrentProductRequest = ref(true);
const loadingSuggestionRequest = ref(true);
const currentProduct = ref<IMotorcycleWithContent | IMowerWithContent | IPartWithContent | null>(null);
const productSuggestion = ref<IMotorcycleWithContent | IMowerWithContent | IPartWithContent | null>(null);

const props = defineProps<{
  productType: ProductTypeEnum;
}>();

onMounted(async () => {
  const productId = route.params.id as string;
  if (productId) {
    try {
      currentProduct.value = await mainStore.getProduct(props.productType, productId);
    } catch (error) {
      console.error("Error fetching current product details:", error);
    } finally {
      loadingCurrentProductRequest.value = false;
    }

    try {
      productSuggestion.value = await mainStore.getProductDetailRecommendation(props.productType, productId);
    } catch (error) {
      console.error("Error fetching product recommendation details:", error);
    } finally {
      loadingSuggestionRequest.value = false;
    }
  }
});

async function keepOriginal() {
  console.log("Keeping original content.");

  const productId = route.params.id as string;
  if (productId) {
    await router.push({
      name: RouteNameEnum.MOTORCYCLE_DETAILS,
      params: { id: productId },
    });
  } else {
    await router.push({ name: RouteNameEnum.MOTORCYCLE_LIST });
  }
}

async function takeSuggestion() {
  console.log("Update product with suggested content.");

  if (productSuggestion.value == null) {
    console.error("Could not find product suggestion to update.");
    await router.push({ name: RouteNameEnum.MOTORCYCLE_LIST });
    return;
  }

  const product = productSuggestion.value;
  try {
    if (props.productType === ProductTypeEnum.MOTORCYCLE) {
      await updateMotorcycle(product.id, product);
      await router.push({
        name: RouteNameEnum.MOTORCYCLE_DETAILS,
        params: { id: product.id },
      });
    } else if (props.productType === ProductTypeEnum.MOWER) {
      await updateMower(product.id, product);
      await router.push({
        name: RouteNameEnum.MOWER_DETAILS,
        params: { id: product.id },
      });
    } else if (props.productType === ProductTypeEnum.PART) {
      await updatePart(product.id, product);
      await router.push({
        name: RouteNameEnum.PART_DETAILS,
        params: { id: product.id },
      });
    }
  } catch (err: any) {
    console.error(err);
  }
}
</script>
