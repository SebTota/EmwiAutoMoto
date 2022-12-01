<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import HelloWorld from "./components/HelloWorld.vue";
import LoginForm from "@/components/LoginForm.vue";
import HeaderComponent from "@/components/HeaderComponent.vue";
</script>

<template>
  <HeaderComponent />
  <LoginForm />

<!--  <RouterView />-->
</template>

<style scoped>
</style>
