<template>
  <div class="bg-white py-8 px-4 overflow-hidden">
    <div class="relative max-w-xl mx-auto">
      <div class="text-center">
        <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">Kontakt</h2>
      </div>
      <div class="text-center mt-8">
        <p class="mt-4 text-lg leading-6 text-gray-500">Wyślij nam wiadomość lub zadzwoń pod numer +48 (731) 853-937</p>
      </div>
      <div class="mt-6">
        <form method="POST" @submit.prevent="submit" class="grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8">
          <div>
            <label for="first-name" class="block text-sm font-medium text-gray-700">Imię</label>
            <div class="mt-1">
              <input type="text" name="first-name" id="first-name" autocomplete="given-name" class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md" />
            </div>
          </div>
          <div>
            <label for="last-name" class="block text-sm font-medium text-gray-700">Nazwisko</label>
            <div class="mt-1">
              <input type="text" name="last-name" id="last-name" autocomplete="family-name" class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md" />
            </div>
          </div>
          <div class="sm:col-span-2">
            <label for="email" class="block text-sm font-medium text-gray-700">E-mail</label>
            <div class="mt-1">
              <input id="email" name="email" type="email" autocomplete="email" class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md" />
            </div>
          </div>
          <div class="sm:col-span-2">
            <label for="phone-number" class="block text-sm font-medium text-gray-700">Numer telefonu</label>
            <div class="mt-1">
              <input type="text" name="phone-number" id="phone-number" autocomplete="tel" class="py-3 px-4 block w-full focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md" placeholder="+48 (555) 555 555"/>
            </div>
          </div>
          <div class="sm:col-span-2">
            <label for="message" class="block text-sm font-medium text-gray-700">Wiadomość</label>
            <div class="mt-1">
              <textarea id="message" :value="message" name="message" rows="4" class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border border-gray-300 rounded-md" />
            </div>
          </div>
          <div class="sm:col-span-2">
            <button type="submit" class="w-full inline-flex items-center justify-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Wyslij</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from "vue";
import {useRoute} from "vue-router";

const route = useRoute();

const message = ref('');
const motorcycleRefLink: any = route.params.motorcycleRef;

function loadTemplate() {
  if (motorcycleRefLink) {
    message.value = `\n\nMotocykl: ${decodeURIComponent(motorcycleRefLink)}`
  }
}
loadTemplate();

function submit() {
  console.log('Submitted contact form')
}

</script>