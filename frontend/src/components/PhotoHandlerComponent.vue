<template>
  <div @drop.prevent="onFileDrop" class="mt-1 flex justify-center rounded-md border-2 border-dashed border-gray-300 px-6 pt-5 pb-6">
    <div class="space-y-1 text-center">
      <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
        <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
      <div class="flex text-sm text-gray-600">
        <label for="file-upload" class="relative cursor-pointer rounded-md bg-white font-medium text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 hover:text-indigo-500">
          <span>Wybierz zdjęcie</span>
          <input @change="onFileSelect($event.target.files);" id="file-upload" name="file-upload" type="file" accept="image/png, image/jpeg" class="sr-only" />
        </label>
        <p class="pl-1">lub przeciągnij i upuść zdjęcie tuta</p>
      </div>
      <p class="text-xs text-gray-500">PNG lub JPG</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted} from "vue";

const emit = defineEmits(['newFileUploaded'])

function onFileSelect(files: File[]) {
  console.log('New file selected');
  emit('newFileUploaded', files[0]);
}

const events = ['dragenter', 'dragover', 'dragleave', 'drop']
function onFileDrop(e: any) {
  console.log('New file dropped')
  emit('newFileUploaded', e.dataTransfer.files[0]);
}

onMounted(() => {
    events.forEach((eventName) => {
        document.body.addEventListener(eventName, preventDefaults)
    })
})

onUnmounted(() => {
    events.forEach((eventName) => {
        document.body.removeEventListener(eventName, preventDefaults)
    })
})

function preventDefaults(e: any) {
    e.preventDefault()
}
</script>