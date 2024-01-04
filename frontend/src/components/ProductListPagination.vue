<template>
  <div class="pt-6">
    <nav
      class="bg-white px-4 pt-3 flex items-center justify-between sm:px-6 dark:text-gray-400 dark:bg-gray-900 dark:border-gray-400"
      aria-label="Pagination"
    >
      <div class="flex-1 flex justify-between sm:justify-end">
        <button
          :disabled="!props.hasPrevPage"
          @click="goBack"
          type="button"
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white disabled:opacity-25"
        >
          Previous
        </button>
        <button
          :disabled="!props.hasNextPage"
          @click="nextPage"
          type="button"
          class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white disabled:opacity-25"
        >
          Next
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  hasNextPage: Boolean,
  hasPrevPage: Boolean,
  nextPage: Function,
  prevPage: Function,
});

function goBack() {
  if (props.prevPage) {
    props.prevPage();
  }
}

function nextPage() {
  if (props.nextPage) {
    props.nextPage();
  }
}
</script>
