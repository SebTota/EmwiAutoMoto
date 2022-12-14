<template>
  <div class="my-8">
    <div>
      <form>
        <div class="sm:overflow-hidden sm:rounded-md">
          <div class="space-y-6 bg-white px-4 py-5 sm:p-6">
            <div class="grid grid-cols-6 gap-6">
              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="year" class="block text-sm font-medium text-gray-700">Rok</label>
                <input type="number" name="year" id="year" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="make" class="block text-sm font-medium text-gray-700">Marka</label>
                <input type="text" name="make" id="make" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="model" class="block text-sm font-medium text-gray-700">Model</label>
                <input type="text" name="model" id="model" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="odometer" class="block text-sm font-medium text-gray-700">Drogomierz</label>
                <input type="number" name="odometer" id="odometer" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="odometer_measurement" class="block text-sm font-medium text-gray-700">Pomiar Drogomierz</label>
                <select id="odometer_measurement" name="odometer_measurement" class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm">
                  <option value="mi">Miles</option>
                  <option value="km">Kilometers</option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="color" class="block text-sm font-medium text-gray-700">Kolor</label>
                <select id="color" name="color" class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm">
                  <option v-for="color in colors" :value="color">{{colorToPolish(color)}}</option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="price" class="block text-sm font-medium text-gray-700">Cena (zł)</label>
                <input type="number" name="price" id="price" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="sold" class="block text-sm font-medium text-gray-700">Sprzedany</label>
                <select id="sold" name="sold" class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm">
                  <option value="false">Na sprzedaż</option>
                  <option value="true">Sprzedany</option>
                </select>
              </div>

              <div class="col-span-6 sm:col-span-3 md:col-span-2">
                <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
                <select id="status" name="status" class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm">
                  <option value="active">Aktywny</option>
                  <option value="inactive">Nieaktywny</option>
                </select>
              </div>
            </div>

            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">Opis</label>
              <div class="mt-1">
                <textarea id="description" name="description" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Photo</label>
              <PhotoHandlerComponent @newFileUploaded="newFileUpload"/>
            </div>

          </div>
          <div class="px-4 py-3 text-right sm:px-6">
            <button type="submit" class="inline-flex justify-center rounded-md bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Zapisz</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>


<script setup lang="ts">
import {MotorcycleColor} from "@/enums/motorcycleColor";
import {colorToPolish} from "@/utils/colors";
import PhotoHandlerComponent from "@/components/PhotoHandlerComponent.vue";

const colors: string[] = Object.values(MotorcycleColor)

function newFileUpload(file: File) {
  console.log('New file uplaoded!!!')
  console.log(file)
}
</script>