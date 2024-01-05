<template>
  <Popover class="relative bg-white dark:text-grey-900 dark:bg-gray-900">
    <div class="mx-auto max-w-7xl sm:px-5">
      <div class="flex items-center justify-between border-gray-100 py-3 md:justify-start md:space-x-10">
        <div class="flex justify-start lg:w-0 lg:flex-1">
          <router-link :to="{ name: 'home' }">
            <span class="sr-only">EMWI Auto Moto</span>
            <img class="h-6 w-auto sm:h-8" src="/logo-no-border.png" alt="" />
          </router-link>
        </div>
        <div class="-my-2 -mr-2 md:hidden">
          <PopoverButton
            class="inline-flex items-center justify-center rounded-md bg-white p-2 focus:outline-none dark:bg-gray-900 dark:text-white dark:hover:bg-gray-800"
          >
            <span class="sr-only">Open menu</span>
            <Bars3Icon class="h-6 w-6" aria-hidden="true" />
          </PopoverButton>
        </div>
        <PopoverGroup as="nav" class="hidden space-x-10 md:flex">
          <router-link
            v-for="item in tabs"
            :key="item.name"
            :to="{ name: item.page }"
            class="-m-3 flex items-center rounded-md p-3 hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            <a class="text-base font-medium">{{ item.name }}</a>
          </router-link>
        </PopoverGroup>
        <div class="hidden items-center justify-end md:flex md:flex-1 lg:w-0">
          <div v-if="mainStateLoaded && !isLoggedIn">
            <router-link :to="{ name: 'login' }" class="whitespace-nowrap text-base font-medium">
              Zaloguj się
            </router-link>
          </div>
          <div v-else>
            <button @click="handleLogout" type="submit" class="whitespace-nowrap text-base font-medium">
              Wyloguj się
            </button>
          </div>
          <p v-if="mainStateLoaded && isLoggedIn">{{ getUsername() }}</p>
        </div>
      </div>
    </div>

    <transition
      enter-active-class="duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="duration-100 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <PopoverPanel
        v-slot="{ close }"
        focus
        class="z-10 absolute inset-x-0 top-0 origin-top-right transform p-2 transition md:hidden"
      >
        <div
          class="divide-y-2 divide-gray-50 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 bg-white dark:text-gray-400 dark:bg-gray-800"
        >
          <div class="px-5 py-5">
            <div class="flex items-center justify-between">
              <div>
                <img class="h-8 w-auto" src="/logo-no-border.png" alt="EMWI Auto Moto" />
              </div>
              <div class="-mr-2">
                <PopoverButton
                  class="inline-flex items-center justify-center rounded-md p-2 hover:bg-gray-100 focus:outline-none dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700"
                >
                  <span class="sr-only">Close menu</span>
                  <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                </PopoverButton>
              </div>
            </div>
            <div class="mt-6">
              <nav class="grid gap-y-8">
                <router-link
                  v-for="item in tabs"
                  :key="item.name"
                  :to="{ name: item.page }"
                  @click="close"
                  class="-m-3 flex items-center rounded-md p-3 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <component :is="item.icon" class="h-6 w-6 flex-shrink-0" aria-hidden="true" />
                  <span class="ml-3 text-base font-medium">{{ item.name }}</span>
                </router-link>
              </nav>
            </div>
          </div>
          <div class="space-y-5 py-5 px-5">
            <div>
              <link />
              <div v-if="mainStateLoaded && !isLoggedIn">
                <router-link
                  @click="close"
                  :to="{ name: 'login' }"
                  class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  Zaloguj się
                </router-link>
              </div>
              <div v-else>
                <button
                  @click="handleLogout"
                  type="submit"
                  class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                  Wyloguj się
                </button>
              </div>
            </div>
          </div>
        </div>
      </PopoverPanel>
    </transition>
  </Popover>
</template>

<script setup lang="ts">
import { Popover, PopoverButton, PopoverGroup, PopoverPanel } from "@headlessui/vue";
import { Bars3Icon, XMarkIcon, ArrowLongRightIcon } from "@heroicons/vue/24/outline";
import { useMainStore } from "@/stores/state";
import { storeToRefs } from "pinia";
import { ref } from "vue";

const mainState = useMainStore();
const mainStateLoaded = ref(false);
const { isLoggedIn, user } = storeToRefs(mainState);

let tabs = [
  {
    name: "Motocykle",
    description: "Motocykle",
    icon: ArrowLongRightIcon,
    page: "motorcycleList",
  },
  {
    name: "Kontakt",
    description: "Kontakt",
    icon: ArrowLongRightIcon,
    page: "contact",
  },
];

const addMotorcycleTab = {
  name: "Nowy Motocykl",
  description: "Nowy Motocykl",
  icon: ArrowLongRightIcon,
  page: "newProduct",
};

mainState.actionCheckLoggedIn().then(() => {
  if (mainState.isAdmin) {
    tabs = [tabs[0], addMotorcycleTab, tabs[1]];
  }
  mainStateLoaded.value = true;
});

function getUsername() {
  return mainState.user?.username;
}

async function handleLogout(event: Event) {
  event.preventDefault();
  await mainState.actionLogout();
  window.location.reload();
}
</script>
