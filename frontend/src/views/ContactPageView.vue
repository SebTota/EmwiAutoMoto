<template>
  <div class="px-5 py-4 mx-auto w-full flex sm:flex-nowrap flex-wrap">
    <div class="md:w-1/2 hidden md:flex bg-gray-300 rounded-lg overflow-hidden py-8 px-14 items-end justify-start relative">
      <iframe
        loading="lazy"
        class="w-full h-full absolute inset-0"
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2567.986996232842!2d20.55490997684331!3d49.93658527149866!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47162725adf82faf%3A0x4a6bbc223774a973!2sEMWI%20Auto-Moto!5e0!3m2!1sen!2sus!4v1704457757907!5m2!1sen!2sus"
        referrerpolicy="no-referrer-when-downgrade"
      ></iframe>
      <div class="bg-white relative hidden md:block xl:flex flex-wrap w-full py-4 rounded shadow-md">
        <div class="xl:w-1/2 px-6">
          <h2 class="title-font font-semibold text-gray-900 tracking-widest text-xs">ADDRESS</h2>
          <p class="mt-1">Poręba Spytkowska<br>Ul. Malownicza<br>60 32-800 Brzesko</p>
        </div>
        <div class="xl:w-1/2 px-6 mt-2 xl:mt-0">
          <h2 class="title-font font-semibold text-gray-900 tracking-widest text-xs">EMAIL</h2>
          <a class="text-indigo-500 leading-relaxed">pawelsowa1970@onet.pl</a>
          <h2 class="title-font font-semibold text-gray-900 tracking-widest text-xs mt-2">PHONE</h2>
          <p class="leading-relaxed">+48 731 853 937</p>
        </div>
      </div>
    </div>
    <div class="md:w-1/2 w-full bg-white flex flex-col md:ml-auto md:mt-0">
      <div class="bg-white px-4 overflow-hidden dark:bg-gray-900">
        <div v-if="emailSentStatus !== 'sent'" class="relative max-w-xl mx-auto">
          <div class="text-center">
            <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl dark:text-gray-400">Kontakt</h2>
          </div>
          <div class="text-center">
            <p class="mt-4 text-md leading-6 text-gray-500">
              Wyślij nam wiadomość lub zadzwoń pod numer +48 (731) 853-937
            </p>
          </div>
          <div class="mt-6">
            <form method="POST" @submit.prevent="submit" class="grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-8">
              <div>
                <label for="first-name" class="block text-sm font-medium text-gray-700 dark:text-gray-200">Imię</label>
                <div class="mt-1">
                  <input
                    type="text"
                    v-model="first_name"
                    :disabled="emailSentStatus === 'sending'"
                    required
                    name="first-name"
                    id="first-name"
                    autocomplete="given-name"
                    class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md disabled:bg-gray-200"
                  />
                </div>
              </div>
              <div>
                <label for="last-name" class="block text-sm font-medium text-gray-700 dark:text-gray-200"
                  >Nazwisko</label
                >
                <div class="mt-1">
                  <input
                    type="text"
                    v-model="last_name"
                    :disabled="emailSentStatus === 'sending'"
                    required
                    name="last-name"
                    id="last-name"
                    autocomplete="family-name"
                    class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md disabled:bg-gray-200"
                  />
                </div>
              </div>
              <div class="sm:col-span-2">
                <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-200">E-mail</label>
                <div class="mt-1">
                  <input
                    id="email"
                    v-model="email"
                    :disabled="emailSentStatus === 'sending'"
                    required
                    name="email"
                    type="email"
                    autocomplete="email"
                    class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md disabled:bg-gray-200"
                  />
                </div>
              </div>
              <div class="sm:col-span-2">
                <label for="phone-number" class="block text-sm font-medium text-gray-700 dark:text-gray-200"
                  >Numer telefonu</label
                >
                <div class="mt-1">
                  <input
                    type="text"
                    v-model="phone_number"
                    :disabled="emailSentStatus === 'sending'"
                    required
                    name="phone-number"
                    id="phone-number"
                    autocomplete="tel"
                    class="py-3 px-4 block w-full focus:ring-indigo-500 focus:border-indigo-500 border-gray-300 rounded-md disabled:bg-gray-200"
                    placeholder="+48 (555) 555 555"
                  />
                </div>
              </div>
              <div class="sm:col-span-2">
                <label for="message" class="block text-sm font-medium text-gray-700 dark:text-gray-200"
                  >Wiadomość</label
                >
                <div class="mt-1">
                  <textarea
                    id="message"
                    v-model="message"
                    :disabled="emailSentStatus === 'sending'"
                    required
                    name="message"
                    rows="5"
                    class="py-3 px-4 block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 border border-gray-300 rounded-md disabled:bg-gray-200"
                  />
                </div>
              </div>
              <div class="sm:col-span-2 text-center">
                <button
                  v-if="emailSentStatus !== 'sending'"
                  type="submit"
                  class="w-full inline-flex items-center justify-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300"
                >
                  Wyslij
                </button>
                <button
                  v-else
                  type="button"
                  disabled
                  class="w-full inline-flex items-center justify-center px-6 py-3 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300"
                >
                  <svg class="h-4 w-4 animate-spin" viewBox="3 3 18 18">
                    <path
                      class="fill-indigo-600"
                      d="M12 5C8.13401 5 5 8.13401 5 12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12C19 8.13401 15.866 5 12 5ZM3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12Z"
                    ></path>
                    <path
                      class="fill-indigo-100"
                      d="M16.9497 7.05015C14.2161 4.31648 9.78392 4.31648 7.05025 7.05015C6.65973 7.44067 6.02656 7.44067 5.63604 7.05015C5.24551 6.65962 5.24551 6.02646 5.63604 5.63593C9.15076 2.12121 14.8492 2.12121 18.364 5.63593C18.7545 6.02646 18.7545 6.65962 18.364 7.05015C17.9734 7.44067 17.3403 7.44067 16.9497 7.05015Z"
                    ></path>
                  </svg>
                  <span class="ml-2">Loading...</span>
                </button>
                <p v-if="error_message" class="text-red-600">
                  {{ error_message }}
                </p>
              </div>
            </form>
          </div>
        </div>
        <div v-else class="py-16">
          <div class="text-center">
            <h1 class="mt-2 text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl">E-mail wysłany.</h1>
            <div class="mt-6">
              <router-link to="/" class="text-base text-gray-500"> Wróć do listy motocykli. </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { api } from "@/api";

const route = useRoute();
const productRefLink: any = route.query.productRef;

const error_message = ref("");
const first_name = ref("");
const last_name = ref("");
const phone_number = ref("");
const email = ref("");
const message = ref("");

const emailSentStatus = ref(""); // '', 'sending', 'sent', 'failed'

function loadTemplate() {
  if (productRefLink) {
    message.value = `\n\nLink: ${decodeURIComponent(productRefLink)}`;
  }
}
loadTemplate();

function submit() {
  error_message.value = "";
  emailSentStatus.value = "";

  if (!first_name.value) {
    error_message.value = "Wpisz imię";
  } else if (!last_name.value) {
    error_message.value = "Wpisz nazwisko";
  } else if (!email.value || !email.value.includes("@")) {
    error_message.value = "Wpisz email";
  } else if (!phone_number.value) {
    error_message.value = "Wpisz numer telefonu";
  } else if (!message.value) {
    error_message.value = "Wpisz wiadomość";
  } else {
    emailSentStatus.value = "sending";
    api
      .sendEmail(first_name.value, last_name.value, email.value, phone_number.value, message.value)
      .then((resp) => {
        console.log("Sent email");
        emailSentStatus.value = "sent";
      })
      .catch((err) => {
        console.log("Error sending email.", err);
        emailSentStatus.value = "failed";
        error_message.value =
          "Wystąpił problem z wysłaniem tego e-maila. Spróbuj skontaktować się z nami ponownie później.";
      });
  }
}
</script>
