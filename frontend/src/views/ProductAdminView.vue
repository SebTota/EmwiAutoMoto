<template>
  <div>
    <LoadingSpinner v-if="loadingRequest" />
    <div v-else>
      <form @submit.prevent="submit">
        <div class="sm:overflow-hidden sm:rounded-md">
          <div class="space-y-6 bg-white py-5 sm:p-6">
            <p class="block text-xl font-medium text-gray-700">Informacje o produkcie: {{ productNameToSingular(props.productType) }}</p>
            <div class="grid grid-cols-6 gap-6">
              <div
                v-for="fieldSchema in getNonTextareaFields()"
                :key="fieldSchema.name"
                class="col-span-6 sm:col-span-3 md:col-span-2"
              >
                <label :for="fieldSchema.name" class="block text-sm font-medium text-gray-700">{{
                  fieldSchema.title
                }}</label>
                <template v-if="fieldSchema.fieldType === 'select'">
                  <select
                    :name="fieldSchema.name"
                    :required="fieldSchema.required"
                    :value="product[fieldSchema.name]"
                    @input="updateField(fieldSchema.name, $event.target.value)"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  >
                    <option v-for="selectField in fieldSchema.options" :key="selectField" :value="selectField.value">
                      {{ selectField.label }}
                    </option>
                  </select>
                </template>
                <template v-else>
                  <input
                    :type="fieldSchema.fieldType"
                    :name="fieldSchema.name"
                    :required="fieldSchema.required"
                    :value="product[fieldSchema.name]"
                    @input="updateField(fieldSchema.name, $event.target.value)"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  />
                </template>
              </div>
            </div>

            <div
              v-for="fieldSchema in getTextareaFields()"
              :key="fieldSchema.name"
              class="col-span-6 sm:col-span-3 md:col-span-2"
            >
              <label :for="fieldSchema.name" class="block text-sm font-medium text-gray-700">{{
                fieldSchema.title
              }}</label>
              <div class="mt-1">
                <textarea
                  :name="fieldSchema.name"
                  :required="fieldSchema.required"
                  :value="product[fieldSchema.name]"
                  @input="updateField(fieldSchema.name, $event.target.value)"
                  rows="8"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                ></textarea>
              </div>
            </div>

            <!-- Media component -->
            <div>
              <p class="block text-xl font-medium text-gray-700">Media</p>
              <label class="block text-sm font-medium text-gray-700">YouTube Wideo</label>
              <div class="flex items-center py-2">
                <input
                  v-model="youtubeLink"
                  class="mr-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  type="text"
                  placeholder="https://youtube.com"
                />
                <button
                  class="flex-shrink-0 rounded-md bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                  type="button"
                  @click="addVideo"
                >
                  Dodaj wideo
                </button>
              </div>
              <div v-if="youtubeLinkError" class="text-sm mb-0 w-100 text-red-400 text-right">
                <p>{{ youtubeLinkError }}</p>
              </div>
              <label class="block text-sm font-medium text-gray-700">Zdjęcia</label>
              <PhotoHandlerComponent @newFileUploaded="newFileUpload" />
            </div>
            <DraggableMediaGalleryComponent :media="media" :on-delete-media="deleteImage" />
          </div>

          <div v-if="showError()" class="text-sm mb-0 w-100 text-red-400 text-right">
            <p>{{ error }}</p>
          </div>
          <div class="px-4 py-3 text-right sm:px-6">
            <button
              type="submit"
              class="inline-flex justify-center rounded-md bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              Zapisz
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import router from "@/router";
import PhotoHandlerComponent from "@/components/PhotoHandlerComponent.vue";
import { useRoute } from "vue-router";
import { useMainStore } from "@/stores/state";
import type { IMedia } from "@/interfaces/media";
import { productNameToSingular, ProductTypeEnum } from "@/enums/productTypeEnum";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import DraggableMediaGalleryComponent from "@/components/DraggableMediaGalleryComponent.vue";
import { MediaTypeEnum } from "@/enums/mediaTypeEnum";
import { RouteNameEnum } from "@/enums/routeNameEnum";
import { createMotorcycle, MotorcycleSchema, updateMotorcycle } from '@/interfaces/motorcycle'
import { createMower, MowerSchema, updateMower } from '@/interfaces/mower'
import { type IProductWithContent, ProductSchema } from "@/interfaces/product";
import { createPart, updatePart } from '@/interfaces/parts'

const route = useRoute();
const mainStore = useMainStore();
const loadingRequest = ref(true);

const error = ref("");
const youtubeLinkError = ref("");
const youtubeLink = ref("");

let product: any = {};
const media = ref<IMedia[]>([]);

const productId: any = route.params.id;
const props = defineProps({
  productType: { type: Object as () => ProductTypeEnum, required: true },
  isNewProduct: { type: Boolean, required: true },
});

async function onStartUp() {
  if (props.isNewProduct) {
    loadingRequest.value = false;
  } else {
    if (!productId) {
      console.error("Product id is required for fetching existing product.");
      return;
    }
    try {
      product = await mainStore.getProduct(props.productType, productId);
      media.value = product.media;
      loadingRequest.value = false;
    } catch (err: any) {
      console.error("Failed to fetch product.", err);
      await router.push({ name: RouteNameEnum.MOTORCYCLE_LIST });
    }
  }
}
onStartUp();

function getNonTextareaFields() {
  switch (props.productType) {
    case ProductTypeEnum.MOTORCYCLE:
      return MotorcycleSchema.filter((field) => field.fieldType !== "textarea");
    case ProductTypeEnum.MOWER:
      return MowerSchema.filter((field) => field.fieldType !== "textarea");
    case ProductTypeEnum.PART:
      return ProductSchema.filter((field) => field.fieldType !== "textarea");
    default:
      return [];
  }
}

function getTextareaFields() {
  switch (props.productType) {
    case ProductTypeEnum.MOTORCYCLE:
      return MotorcycleSchema.filter((field) => field.fieldType === "textarea");
    case ProductTypeEnum.MOWER:
      return MowerSchema.filter((field) => field.fieldType === "textarea");
    case ProductTypeEnum.PART:
      return ProductSchema.filter((field) => field.fieldType === "textarea");
    default:
      return [];
  }
}

const updateField = (fieldName: string, value: string | number) => {
  product[fieldName] = typeof value === "string" ? value.trim() : value;
};

function submit() {
  error.value = "";

  product.media = media.value;
  if (props.isNewProduct) {
    createProduct();
  } else if (productId) {
    updateProduct();
  }
}

async function createProduct() {
  console.log("Creating new product...", product);

  try {
    loadingRequest.value = true;
    if (props.productType === ProductTypeEnum.MOTORCYCLE) {
      const createdProduct: IProductWithContent = await createMotorcycle(product);
      await router.push({
        name: RouteNameEnum.MOTORCYCLE_DETAILS,
        params: { id: createdProduct.id },
      });
    } else if (props.productType === ProductTypeEnum.MOWER) {
      const createdProduct: IProductWithContent = await createMower(product);
      await router.push({
        name: RouteNameEnum.MOWER_DETAILS,
        params: { id: createdProduct.id },
      });
    } else if (props.productType === ProductTypeEnum.PART) {
      const createdProduct: IProductWithContent = await createPart(product);
      await router.push({
        name: RouteNameEnum.PART_DETAILS,
        params: { id: createdProduct.id },
      });
    }
  } catch (err: any) {
    console.error(err);
    error.value = "Nie udało się utworzyć produktu.";
  } finally {
    loadingRequest.value = false;
  }
}

async function updateProduct() {
  console.log("Updating product...", product);

  try {
    loadingRequest.value = true;
    if (props.productType === ProductTypeEnum.MOTORCYCLE) {
      await updateMotorcycle(productId, product);
      await router.push({
        name: RouteNameEnum.MOTORCYCLE_DETAILS,
        params: { id: productId },
      });
    } else if (props.productType === ProductTypeEnum.MOWER) {
      await updateMower(productId, product);
      await router.push({
        name: RouteNameEnum.MOWER_DETAILS,
        params: { id: productId },
      });
    } else if (props.productType === ProductTypeEnum.PART) {
      await updatePart(productId, product);
      await router.push({
        name: RouteNameEnum.PART_DETAILS,
        params: { id: productId },
      });
    }
  } catch (err: any) {
    console.error(err);
    error.value = "Nie udało się zaktualizować produktu.";
  } finally {
    loadingRequest.value = false;
  }
}

async function newFileUpload(files: FileList) {
  error.value = "";
  loadingRequest.value = true;
  try {
    console.log("Uploading new image...");
    const newImages: [IMedia] = await mainStore.uploadProductImage(files);
    for (const newImage of newImages) {
      media.value.push(newImage);
    }
    loadingRequest.value = false;
  } catch (err: any) {
    console.error(err);
    error.value = "Failed to upload image.";
  } finally {
    loadingRequest.value = false;
  }
}

async function deleteImage(imageUrl: string) {
  for (let i = 0; i < media.value.length; i++) {
    if (media.value[i].url === imageUrl) {
      media.value.splice(i, 1);
      break;
    }
  }
}

function addVideo() {
  youtubeLinkError.value = "";

  try {
    const videoId: string = extractYouTubeVideoIdFromLink(youtubeLink.value);
    console.log("Extracted YouTube video id: ", videoId);

    const video: IMedia = generateYouTubeVideoObject(videoId);
    console.log("Generated YouTube video object: ", video);

    media.value.push(video);
    youtubeLink.value = ""; // Reset input form
  } catch (e) {
    console.error("Failed to extract YouTube video id.", e);
    youtubeLinkError.value = "Nie udało się wyodrębnić identyfikatora wideo YouTube z linku.";
    return;
  }
}

function generateYouTubeVideoObject(videoId: string): IMedia {
  const videoUrl: string = `https://www.youtube-nocookie.com/embed/${videoId}`;
  const baseThumbnailUrl: string = `https://img.youtube.com/vi/${videoId}`;

  return {
    type: MediaTypeEnum.YOUTUBE_VIDEO,
    url: videoUrl,
    thumbnail_url: `${baseThumbnailUrl}/mqdefault.jpg`,
    medium_thumbnail_url: `${baseThumbnailUrl}/hqdefault.jpg`,
  };
}

function extractYouTubeVideoIdFromLink(url: string): string {
  const regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  const match = url.match(regExp);
  if (match && match[2].length == 11) {
    return match[2];
  } else {
    throw Error("Failed to extract YouTube video id from link.");
  }
}

function showError() {
  return error.value && error.value.length > 0;
}
</script>
