<template>
  <div class="min-h-full pt-16 pb-12 flex flex-col bg-white">
    <main
      class="flex-grow flex flex-col justify-center max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8"
    >
      <div class="py-16">
        <div class="text-center">
          <p
            class="text-sm font-semibold text-indigo-600 uppercase tracking-wide"
          >
            Błąd 404
          </p>
          <h1
            class="mt-2 text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl"
          >
            Nie znaleziono strony.
          </h1>
          <p class="mt-2 text-base text-gray-500">
            Niestety, nie udało nam się znaleźć strony, której szukasz.
          </p>
          <div class="mt-6">
            <router-link
              to="/"
              class="text-base font-medium text-indigo-600 hover:text-indigo-500"
            >
              Wróć do listy motocykli.
            </router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
<script setup lang="ts"></script>
