<script setup lang="ts">
import { RouterView } from "vue-router";
import HeaderComponent from "@/components/HeaderComponent.vue";
</script>

<template>
  <HeaderComponent />
  <RouterView :key="$route.fullPath" />
</template>

<style scoped>
</style>
