<template>
  <div>
    <LoadingSpinner v-if="loadingRequest" />
    <div v-else>
      <form @submit.prevent="submit">
        <div class="sm:overflow-hidden sm:rounded-md">
          <div class="space-y-6 bg-white py-5 sm:p-6">
            <div class="grid grid-cols-6 gap-6">
              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="type" class="block text-sm font-medium text-gray-700">Produkt</label>
                <select
                  v-model="type"
                  id="type"
                  name="type"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                >
                  <option v-for="(productType, index) in ProductTypeEnum" :key="index" :value="productType">
                    {{ productType }}
                  </option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="year" class="block text-sm font-medium text-gray-700">Rok</label>
                <input
                  v-model="year"
                  type="number"
                  name="year"
                  id="year"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="make" class="block text-sm font-medium text-gray-700">Marka</label>
                <input
                  v-model="make"
                  type="text"
                  name="make"
                  id="make"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="model" class="block text-sm font-medium text-gray-700">Model</label>
                <input
                  v-model="model"
                  type="text"
                  name="model"
                  id="model"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div v-if="hideVinInput()" class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="model" class="block text-sm font-medium text-gray-700">VIN (opcjonalne)</label>
                <input
                  v-model="vin"
                  type="text"
                  name="vin"
                  id="vin"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="odometer" class="block text-sm font-medium text-gray-700"
                  >Przebieg ({{ odometer_type }})</label
                >
                <input
                  v-model="odometer"
                  type="number"
                  name="odometer"
                  id="odometer"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="color" class="block text-sm font-medium text-gray-700">Kolor</label>
                <select
                  v-model="color"
                  id="color"
                  name="color"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                >
                  <option v-for="(color, index) in colors" :key="index" :value="color">
                    {{ colorToPolish(color) }}
                  </option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="price" class="block text-sm font-medium text-gray-700">Cena (zł) (opcjonalne)</label>
                <input
                  v-model="price"
                  type="number"
                  name="price"
                  id="price"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
                <select
                  v-model="status"
                  id="status"
                  name="status"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                >
                  <option :value="ProductStatusEnum.FOR_SALE">Na sprzedaż</option>
                  <option :value="ProductStatusEnum.RESERVED">Zarezerwowany</option>
                  <option :value="ProductStatusEnum.SOLD">Sprzedane</option>
                  <option :value="ProductStatusEnum.DRAFT">Szkic</option>
                  <option :value="ProductStatusEnum.DELETED">Sunięte</option>
                </select>
              </div>
            </div>

            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">Opis (opcjonalne)</label>
              <div class="mt-1">
                <textarea
                  v-model="description"
                  id="description"
                  name="description"
                  rows="8"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <DraggableImageGalleryComponent :images="images" :onDelete="deleteImage" />
              <label class="block text-sm font-medium text-gray-700">Photo</label>
              <PhotoHandlerComponent @newFileUploaded="newFileUpload" />
            </div>
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
import { ref, watch } from "vue";
import router from "@/router";
import { ProductColor } from "@/enums/productColor";
import { colorToPolish } from "@/utils/colors";
import PhotoHandlerComponent from "@/components/PhotoHandlerComponent.vue";
import type { IProduct, IProductCreate, IProductWithImages } from "@/interfaces/product";
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import { useRoute } from "vue-router";
import { useMainStore } from "@/stores/state";
import type { IImage } from "@/interfaces/image";
import DraggableImageGalleryComponent from "@/components/DraggableImageGalleryComponent.vue";
import { ProductTypeEnum } from "@/enums/productTypeEnum";
import { OdometerTypeEnum } from "@/enums/odometerTypeEnum";
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const route = useRoute();
const mainStore = useMainStore();
const loadingRequest = ref(true);
const error = ref("");

const colors: string[] = Object.values(ProductColor);

const type = ref();
const year = ref();
const make = ref();
const model = ref();
const vin = ref();
const odometer = ref();
const odometer_type = ref();
const color = ref();
const price = ref();
const status = ref();
const description = ref();

watch(type, (newType) => {
  odometer_type.value = newType === ProductTypeEnum.MOTOCYKL ? OdometerTypeEnum.MIL : OdometerTypeEnum.GODZIN;
});

const productId: any = route.params.id;
const images = ref<IImage[]>([]);

async function onStartUp() {
  if (isAddNew()) {
    type.value = ProductTypeEnum.MOTOCYKL;
    loadingRequest.value = false;
  } else {
    try {
      const product: IProductWithImages = await mainStore.getProduct(productId);
      type.value = product.type;
      year.value = product.year;
      make.value = product.make;
      model.value = product.model;
      vin.value = product.vin;
      odometer.value = product.odometer;
      color.value = product.color;
      price.value = product.price;
      status.value = product.status;
      description.value = product.description;
      images.value = product.images;
      loadingRequest.value = false;
    } catch (err: any) {
      await router.push({ name: "productList" });
    }
  }
}
onStartUp();

function isAddNew() {
  return router.currentRoute.value.path.startsWith("/produkt/nowy");
}

function showError() {
  return error.value && error.value.length > 0;
}

function hideVinInput() {
  return type.value === ProductTypeEnum.MOTOCYKL;
}

function trimFormValues() {
  make.value = make.value?.trim();
  model.value = model.value?.trim();
  vin.value = vin.value?.trim();
  description.value = description.value?.trim();
}

function submit() {
  error.value = "";
  trimFormValues();

  if (isAddNew()) {
    createProduct();
  } else {
    updateProduct();
  }
}

async function createProduct() {
  error.value = "";

  const productCreate: IProductCreate = {
    type: type.value,
    year: year.value,
    make: make.value,
    model: model.value,
    vin: vin.value,
    odometer: odometer.value,
    odometer_type: odometer_type.value,
    color: color.value,
    price: price.value ? price.value : null,
    description: description.value,
    status: ProductStatusEnum.FOR_SALE,
    images: images.value,
  };

  try {
    loadingRequest.value = true;
    const createdProduct: IProduct = await mainStore.createProducts(productCreate);
    await router.push({
      name: "productDetails",
      params: { id: createdProduct.id },
    });
  } catch (err: any) {
    console.error(err);
    error.value = "Failed to create product.";
  } finally {
    loadingRequest.value = false;
  }
}

async function updateProduct() {
  const product: IProductCreate = {
    type: type.value,
    year: year.value,
    make: make.value,
    model: model.value,
    vin: vin.value,
    odometer: odometer.value,
    odometer_type: odometer_type.value,
    color: color.value,
    price: price.value ? price.value : null,
    description: description.value,
    status: status.value,
    images: images.value,
  };

  try {
    loadingRequest.value = true;
    await mainStore.updateProducts(productId, product);
    await router.push({
      name: "productDetails",
      params: { id: productId },
    });
  } catch (err: any) {
    error.value = "Failed to update product.";
  } finally {
    loadingRequest.value = false;
  }
}

async function newFileUpload(files: FileList) {
  error.value = "";
  loadingRequest.value = true;
  try {
    console.log("Uploading new image...");
    const newImages: [IImage] = await mainStore.uploadProductImage(files);
    for (const newImage of newImages) {
      images.value.push(newImage);
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
  for (let i = 0; i < images.value.length; i++) {
    if (images.value[i].image_url === imageUrl) {
      images.value.splice(i, 1);
      break;
    }
  }
}
</script>
