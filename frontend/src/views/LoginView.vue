<template>
  <div
    class="flex min-h-full items-center justify-center py-8 px-4 sm:px-6 lg:px-8"
  >
    <div class="w-full max-w-md space-y-8">
      <div>
        <img
          class="mx-auto h-12 w-auto"
          src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
          alt="EMWI Auto Moto"
        />
        <h2
          class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900"
        >
          Zaloguj się na swoje konto
        </h2>
      </div>
      <form class="mt-8 space-y-6" action="#" method="POST">
        <input type="hidden" name="remember" value="true" />
        <div class="-space-y-px rounded-md shadow-sm">
          <div>
            <label for="username" class="sr-only">Nazwa użytkownika</label>
            <input
              v-model="username"
              id="username"
              name="username"
              type="text"
              required
              class="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
              placeholder="Username"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Hasło</label>
            <input
              v-model="password"
              id="password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              class="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
              placeholder="Password"
            />
          </div>
        </div>
        <div>
          <button
            @click="handleLogin"
            type="submit"
            class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Zaloguj się
          </button>
        </div>
        <div v-if="showLoginError" class="text-sm mb-4 w-max text-red-400">
          Nieprawidłowa nazwa użytkownika lub hasło.
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMainStore } from "@/stores/state";
import { ref } from "vue";

const mainStore = useMainStore();

const showLoginError = ref(false);
const username = ref("");
const password = ref("");

async function handleLogin(event: Event) {
  event.preventDefault();
  showLoginError.value = false;
  try {
    await mainStore.actionLogIn(username.value, password.value);
  } catch (error) {
    showLoginError.value = true;
  }
}
</script>

<style></style>
