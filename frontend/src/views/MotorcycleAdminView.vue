<template>
  <div class="my-8">
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

    <div v-else>
      <form @submit.prevent="submit">
        <div class="sm:overflow-hidden sm:rounded-md">
          <div class="space-y-6 bg-white px-4 py-5 sm:p-6">
            <div class="grid grid-cols-6 gap-6">
              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label
                  for="year"
                  class="block text-sm font-medium text-gray-700"
                  >Rok</label
                >
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
                <label
                  for="make"
                  class="block text-sm font-medium text-gray-700"
                  >Marka</label
                >
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
                <label
                  for="model"
                  class="block text-sm font-medium text-gray-700"
                  >Model</label
                >
                <input
                  v-model="model"
                  type="text"
                  name="model"
                  id="model"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label
                  for="odometer_miles"
                  class="block text-sm font-medium text-gray-700"
                  >Drogomierz (Mil)</label
                >
                <input
                  v-model="odometer_miles"
                  type="number"
                  name="odometer_miles"
                  id="odometer_miles"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label
                  for="color"
                  class="block text-sm font-medium text-gray-700"
                  >Kolor</label
                >
                <select
                  v-model="color"
                  id="color"
                  name="color"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                >
                  <option
                    v-for="(color, index) in colors"
                    :key="index"
                    :value="color"
                  >
                    {{ colorToPolish(color) }}
                  </option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label
                  for="price"
                  class="block text-sm font-medium text-gray-700"
                  >Cena (zł)</label
                >
                <input
                  v-model="price"
                  type="number"
                  name="price"
                  id="price"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label
                  for="status"
                  class="block text-sm font-medium text-gray-700"
                  >Status</label
                >
                <select
                  v-model="status"
                  id="status"
                  name="status"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="FOR_SALE">Na sprzedaż</option>
                  <option value="SOLD">Sprzedany</option>
                  <option value="DRAFT">Szkic</option>
                  <option value="DELETED">Usunięty</option>
                </select>
              </div>
            </div>

            <div>
              <label
                for="description"
                class="block text-sm font-medium text-gray-700"
                >Opis</label
              >
              <div class="mt-1">
                <textarea
                  v-model="description"
                  id="description"
                  name="description"
                  rows="3"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
              </div>
            </div>

            <div>
              <ImageGallery :images="images" :onDelete="deleteImage" />
              <label class="block text-sm font-medium text-gray-700"
                >Photo</label
              >
              <PhotoHandlerComponent @newFileUploaded="newFileUpload" />
            </div>
          </div>

          <div
            v-if="showError()"
            class="text-sm mb-0 w-100 text-red-400 text-right"
          >
            <p>{{ error }}</p>
          </div>
          <!--          <div v-if="isAddNew()" class="px-4 py-3 text-right sm:px-6">-->
          <!--            <button-->
          <!--              type="submit"-->
          <!--              class="inline-flex justify-center rounded-md bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"-->
          <!--            >-->
          <!--              Dalej-->
          <!--            </button>-->
          <!--          </div>-->
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
import { MotorcycleColor } from "@/enums/motorcycleColor";
import { colorToPolish } from "@/utils/colors";
import PhotoHandlerComponent from "@/components/PhotoHandlerComponent.vue";
import type {
  IMotorcycle,
  IMotorcycleCreate,
  IMotorcycleWithImages,
} from "@/interfaces/motorcycle";
import { ProductStatusEnum } from "@/enums/productStatusEnum";
import { useRoute } from "vue-router";
import { useMainStore } from "@/stores/state";
import type { IImage } from "@/interfaces/image";
import ImageGallery from "@/components/ImageGallery.vue";

const route = useRoute();
const mainStore = useMainStore();
const loadingRequest = ref(true);
const error = ref("");

const colors: string[] = Object.values(MotorcycleColor);

const year = ref();
const make = ref();
const model = ref();
const odometer_miles = ref();
const color = ref();
const price = ref();
const status = ref();
const description = ref();

const motorcycleId: any = route.params.id;
const images = ref<IImage[]>([]);

async function onStartUp() {
  if (isAddNew()) {
    loadingRequest.value = false;
  } else {
    try {
      const motorcycle: IMotorcycleWithImages = await mainStore.getMotorcycle(
        motorcycleId
      );
      year.value = motorcycle.year;
      make.value = motorcycle.make;
      model.value = motorcycle.model;
      odometer_miles.value = motorcycle.odometer_miles;
      color.value = motorcycle.color;
      price.value = motorcycle.price;
      status.value = motorcycle.status;
      description.value = motorcycle.description;
      images.value = motorcycle.images;
      loadingRequest.value = false;
    } catch (err: any) {
      await router.push({ name: "motorcycleList" });
    }
  }
}
onStartUp();

function isAddNew() {
  return router.currentRoute.value.path.startsWith("/motorcycle/new");
}

function showError() {
  return error.value && error.value.length > 0;
}

function submit() {
  error.value = "";

  if (isAddNew()) {
    createMotorcycle();
  } else {
    updateMotorcycle();
  }
}

async function createMotorcycle() {
  error.value = "";

  const motorcycle: IMotorcycleCreate = {
    year: year.value,
    make: make.value,
    model: model.value,
    odometer_miles: odometer_miles.value,
    color: color.value,
    price: price.value,
    description: description.value,
    status: ProductStatusEnum.FOR_SALE,
    images: images.value,
  };

  try {
    loadingRequest.value = true;
    const createdMotorcycle: IMotorcycle = await mainStore.createMotorcycle(
      motorcycle
    );
    await router.push({
      name: "motorcycleDetail",
      params: { id: createdMotorcycle.id },
    });
  } catch (err: any) {
    console.error(err);
    error.value = "Failed to create motorcycle.";
  } finally {
    loadingRequest.value = false;
  }
}

async function updateMotorcycle() {
  const motorcycle: IMotorcycleCreate = {
    year: year.value,
    make: make.value,
    model: model.value,
    odometer_miles: odometer_miles.value,
    color: color.value,
    price: price.value,
    description: description.value,
    status: status.value,
    images: images.value,
  };

  try {
    loadingRequest.value = true;
    await mainStore.updateMotorcycle(motorcycleId, motorcycle);
    await router.push({
      name: "motorcycleDetail",
      params: { id: motorcycleId },
    });
  } catch (err: any) {
    error.value = "Failed to update motorcycle.";
  } finally {
    loadingRequest.value = false;
  }
}

async function newFileUpload(file: File) {
  error.value = "";
  loadingRequest.value = true;
  try {
    console.log("Uploading new image...");
    const newImage: IImage = await mainStore.uploadProductImage(file);
    images.value.push(newImage);
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
