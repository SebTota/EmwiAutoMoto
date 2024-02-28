<template>
  <div>
    <VueDraggableNext
      class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-2"
      :list="props.media"
      v-bind="dragOptions"
    >
      <div v-for="media in props.media" :key="media.thumbnail_url" class="hover:bg-slate-10">
        <div class="aspect-w-5 aspect-h-3 w-full overflow-hidden">
          <img
            :src="media.thumbnail_url"
            class="rounded hover:transparency-80 h-full w-full object-cover object-center"
          />
        </div>
        <div class="rounded mt-1 text-center">
          <button
            @click.prevent="deleteMedia(media)"
            class="inline-flex justify-center rounded-md bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-rose-600 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:ring-offset-2"
          >
            Usuń
          </button>
        </div>
      </div>
    </VueDraggableNext>
  </div>
</template>

<script setup lang="ts">
import { VueDraggableNext } from "vue-draggable-next";
import type { IMedia } from "@/interfaces/media";

const props = defineProps({
  media: { type: Array as () => IMedia[], required: true },
  onDeleteMedia: { type: Function, required: true },
});

const dragOptions = {
  animation: 200,
  group: "description",
  disabled: false,
  ghostClass: "ghost",
};

function deleteMedia(media: IMedia) {
  console.log("Deleting media: ", media);
  props.onDeleteMedia(media.url);
}
</script>
