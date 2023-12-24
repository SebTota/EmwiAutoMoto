<template>
  <Popover class="relative bg-white dark:text-grey-900 dark:bg-gray-900">
    <div class="mx-auto max-w-7xl px-5">
      <div
        class="flex items-center justify-between border-gray-100 py-3 md:justify-start md:space-x-10"
      >
        <div class="flex justify-start lg:w-0 lg:flex-1">
          <a href="/">
            <span class="sr-only">EMWI AUto Moto</span>
            <img
              class="h-8 w-auto sm:h-10"
              src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
              alt=""
            />
          </a>
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
          <a
            v-for="item in tabs"
            :key="item.name"
            href="#"
            @click="item.onClickHandler()"
            class="-m-3 flex items-center rounded-md p-3 hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            <a class="text-base font-medium">{{ item.name }}</a>
          </a>
        </PopoverGroup>
        <div class="hidden items-center justify-end md:flex md:flex-1 lg:w-0">
          <a
            v-if="mainStateLoaded && !isLoggedIn"
            href="#"
            @click="goToLogin()"
            class="whitespace-nowrap text-base font-medium"
            >Sign in</a
          >
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
        focus
        class="z-10 absolute inset-x-0 top-0 origin-top-right transform p-2 transition md:hidden"
      >
        <div
          class="divide-y-2 divide-gray-50 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 bg-white dark:text-gray-400 dark:bg-gray-800"
        >
          <div class="px-5 py-5">
            <div class="flex items-center justify-between">
              <div>
                <img
                  class="h-8 w-auto"
                  src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
                  alt="EMWI Auto Moto"
                />
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
                <a
                  v-for="item in tabs"
                  :key="item.name"
                  href="#"
                  @click="item.onClickHandler()"
                  class="-m-3 flex items-center rounded-md p-3 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <component
                    :is="item.icon"
                    class="h-6 w-6 flex-shrink-0"
                    aria-hidden="true"
                  />
                  <span class="ml-3 text-base font-medium">{{
                    item.name
                  }}</span>
                </a>
              </nav>
            </div>
          </div>
          <div class="space-y-5 py-5 px-5">
            <div>
              <link />
              <a
                v-if="mainStateLoaded && !isLoggedIn"
                href="#"
                @click="goToLogin"
                class="group relative flex w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >Sign in</a
              >
            </div>
          </div>
        </div>
      </PopoverPanel>
    </transition>
  </Popover>
</template>

<script setup lang="ts">
import {
  Popover,
  PopoverButton,
  PopoverGroup,
  PopoverPanel,
} from "@headlessui/vue";
import {
  Bars3Icon,
  XMarkIcon,
  ArrowLongRightIcon,
} from "@heroicons/vue/24/outline";
import { useMainStore } from "@/stores/state";
import { storeToRefs } from "pinia";
import { ref } from "vue";
import router from "@/router";

const mainState = useMainStore();
const mainStateLoaded = ref(false);
const { isLoggedIn, user } = storeToRefs(mainState);

let tabs = [
  {
    name: "Motocykle",
    description: "Motocykle",
    onClickHandler: goHome,
    icon: ArrowLongRightIcon,
  },
  {
    name: "Kontakt",
    description: "Kontakt",
    onClickHandler: goToContactPage,
    icon: ArrowLongRightIcon,
  },
];

const addMotorcycleTab = {
  name: "Nowy Motocykl",
  description: "Nowy Motocykl",
  onClickHandler: goToNewMotorcyclePage,
  icon: ArrowLongRightIcon,
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

function goToLogin() {
  router.push({ name: "login" });
}

function goHome() {
  router.push({ name: "motorcycleList" });
}

function goToContactPage() {
  router.push({ name: "contact" });
}

function goToNewMotorcyclePage() {
  router.push({ name: "newMotorcycle" });
}
</script>
