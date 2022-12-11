<template>
  <div class="pt-6">
    <nav class="bg-white px-4 pt-3 flex items-center justify-between border-t border-gray-200 sm:px-6" aria-label="Pagination">
<!--      <div class="hidden sm:block">-->
<!--        <p class="text-sm text-gray-700">-->
<!--          Showing-->
<!--          {{ ' ' }}-->
<!--          <span class="font-medium">1</span>-->
<!--          {{ ' ' }}-->
<!--          to-->
<!--          {{ ' ' }}-->
<!--          <span class="font-medium">10</span>-->
<!--          {{ ' ' }}-->
<!--          of-->
<!--          {{ ' ' }}-->
<!--          <span class="font-medium">20</span>-->
<!--          {{ ' ' }}-->
<!--          results-->
<!--        </p>-->
<!--      </div>-->
      <div class="flex-1 flex justify-between sm:justify-end">
        <button :disabled="!props.hasPrevPage" @click="props.prevPage" type="button" class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white disabled:opacity-25"> Previous </button>
        <button :disabled="!props.hasNextPage" @click="props.nextPage" type="button" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white disabled:opacity-25"> Next </button>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  hasNextPage: Boolean,
  hasPrevPage: Boolean,
  nextPage: Function,
  prevPage: Function
})
</script>