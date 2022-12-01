<template>
  <button>
    <MoonIcon class="btn-icon h-6 w-6 flex-shrink-0 text-gray-500 hover:text-gray-900" @click="toggleDarkMode" />
  </button>
</template>

<script setup>
import {
  MoonIcon
} from '@heroicons/vue/24/outline'

function toggleDarkMode() {
  if (localStorage.emwi_auto_moto_theme) {
    if (localStorage.emwi_auto_moto_theme === 'dark') {
      localStorage.emwi_auto_moto_theme = 'light';
      document.documentElement.classList.remove('dark')
    } else {
      localStorage.emwi_auto_moto_theme = 'dark';
      document.documentElement.classList.add('dark')
    }
  } else {
    localStorage.emwi_auto_moto_theme = 'dark';
    document.documentElement.classList.add('dark')
  }
}

</script>

<style scoped>

</style>
