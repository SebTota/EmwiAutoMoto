<template>
  <div class="relative bg-white dark:text-grey-900 dark:bg-gray-900">
    <div class="mx-auto sm:px-5">
      <div class="flex items-center justify-between border-gray-100 py-3 pb-6 lg:justify-start lg:space-x-10">
        <div class="flex justify-start flex-1">
          <router-link :to="{ name: RouteNameEnum.HOME }"
            ><span class="sr-only">EMWI Auto Moto</span>
            <img class="h-7 w-auto block sm:hidden" src="/logo-no-border.png" alt="Company Logo" />
            <img class="h-14 w-auto hidden sm:block" src="/logo-stacked.png" alt="Company Logo"
          /></router-link>
        </div>
        <div class="-my-2 -mr-2 lg:hidden">
          <button
            @click="toggleMobileMenu"
            id="mobile-menu-button"
            class="inline-flex items-center justify-center rounded-md bg-white p-2 focus:outline-none dark:bg-gray-900 dark:text-white dark:hover:bg-gray-800"
          >
            <span class="sr-only">Open menu</span>
            <Bars3Icon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <nav class="hidden space-x-4 lg:space-x-10 lg:flex">
          <router-link
            v-for="item in tabs"
            :key="item.name"
            :to="{ name: item.page }"
            class="-m-3 flex items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-800"
            :class="{
              'border-b-2 border-indigo-600': $route.name === item.page,
            }"
          >
            <a class="text-base font-medium">{{ item.name }}</a>
          </router-link>
          <div v-if="mainStateLoaded && isAdmin" class="relative">
            <button
              @click="toggleAdminDropdown"
              id="admin-dropdown-button"
              class="-m-3 flex items-center rounded-md p-3 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
              <span class="text-base font-medium">Nowy Produkt</span>
              <ChevronDownIcon class="ml-2 h-5 w-5" aria-hidden="true" />
            </button>
            <div
              v-if="adminDropdownOpen"
              id="admin-dropdown"
              class="absolute right-0 z-50 mt-2 w-48 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-gray-800"
            >
              <div class="py-1">
                <router-link
                  v-for="adminTab in adminTabs"
                  :key="adminTab.name"
                  :to="{ name: adminTab.page }"
                  @click="closeAdminDropdown"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                >
                  {{ adminTab.name }}
                </router-link>
              </div>
            </div>
          </div>
        </nav>
        <div class="hidden items-center justify-end lg:flex lg:flex-1 w-0">
          <div v-if="mainStateLoaded && !isLoggedIn">
            <router-link :to="{ name: RouteNameEnum.LOGIN }" class="whitespace-nowrap text-base font-medium">
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

    <div
      v-if="mobileMenuOpen"
      id="mobile-menu"
      class="z-10 absolute inset-x-0 top-0 origin-top-right transform p-2 transition lg:hidden"
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
              <button
                @click="toggleMobileMenu"
                class="inline-flex items-center justify-center rounded-md p-2 hover:bg-gray-100 focus:outline-none dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700"
              >
                <span class="sr-only">Close menu</span>
                <XMarkIcon class="h-6 w-6" aria-hidden="true" />
              </button>
            </div>
          </div>
          <div class="mt-6">
            <nav class="grid gap-y-8">
              <router-link
                v-for="item in tabs"
                :key="item.name"
                :to="{ name: item.page }"
                @click="toggleMobileMenu"
                class="-m-3 flex items-center rounded-md p-3 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <component :is="item.icon" class="h-6 w-6 flex-shrink-0" aria-hidden="true" />
                <span class="ml-3 text-base font-medium">{{ item.name }}</span>
              </router-link>
              <div v-if="mainStateLoaded && isAdmin" class="w-full">
                <button
                  @click="toggleAdminDropdown"
                  id="mobile-admin-dropdown-button"
                  class="-m-3 w-full flex items-center rounded-md p-3 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <ArrowLongRightIcon class="h-6 w-6 flex-shrink-0" aria-hidden="true" />
                  <span class="w-full ml-3 text-base font-medium text-left">Nowy Produkt</span>
                </button>
                <div v-if="adminDropdownOpen" class="space-y-1 px-2 pt-2 pb-3">
                  <router-link
                    v-for="adminTab in adminTabs"
                    :key="adminTab.name"
                    :to="{ name: adminTab.page }"
                    @click="toggleMobileMenu"
                    class="block rounded-md px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                  >
                    {{ adminTab.name }}
                  </router-link>
                </div>
              </div>
            </nav>
          </div>
        </div>
        <div class="space-y-5 py-5 px-5">
          <div>
            <link />
            <div v-if="mainStateLoaded && !isLoggedIn">
              <router-link
                @click="toggleMobileMenu"
                :to="{ name: RouteNameEnum.LOGIN }"
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
    </div>
  </div>
</template>
<script setup lang="ts">
import { ArrowLongRightIcon, Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline";
import { useMainStore } from "@/stores/state";
import { storeToRefs } from "pinia";
import { onMounted, onUnmounted, ref } from "vue";
import { RouteNameEnum } from "@/enums/routeNameEnum";

const mainState = useMainStore();
const mainStateLoaded = ref(false);
const { isLoggedIn, isAdmin } = storeToRefs(mainState);
const adminDropdownOpen = ref(false);
const mobileMenuOpen = ref(false);

onMounted(() => {
  document.addEventListener("click", closeAllDropDowns);
});

onUnmounted(() => {
  document.removeEventListener("click", closeAllDropDowns);
});

let tabs = [
  {
    name: "Strona Główna",
    description: "Strona Główna",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.HOME,
  },
  {
    name: "Motocykle",
    description: "Motocykle",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.MOTORCYCLE_LIST,
  },
  {
    name: "Traktory Ogrodowe",
    description: "Traktory Ogrodowe",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.MOWER_LIST,
  },
  {
    name: "Części i Akcesoria",
    description: "Części i Akcesoria",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.PART_LIST,
  },
  {
    name: "Kontakt",
    description: "Kontakt",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.CONTACT,
  },
];

const adminTabs = [
  {
    name: "Nowy Motocykl",
    description: "Nowy Motocykl",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.NEW_MOTORCYCLE,
  },
  {
    name: "Nowy Traktor Ogrodowy",
    description: "Nowy Traktor Ogrodowy",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.NEW_MOWER,
  },
  {
    name: "Nowa Część lub Akcesorium",
    description: "Nowa Część lub Akcesorium",
    icon: ArrowLongRightIcon,
    page: RouteNameEnum.NEW_PART,
  },
];

mainState.actionCheckLoggedIn().then(() => {
  mainStateLoaded.value = true;
});

function getUsername() {
  return mainState.user?.username;
}

async function handleLogout(event: Event) {
  event.preventDefault();
  mainState.actionLogout();
  window.location.reload();
}

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value;
  adminDropdownOpen.value = false;
}

function toggleAdminDropdown() {
  adminDropdownOpen.value = !adminDropdownOpen.value;
}

function closeAdminDropdown() {
  adminDropdownOpen.value = false;
}

function closeAllDropDowns(event: Event) {
  const adminDropdownButton = document.getElementById("admin-dropdown-button");
  const mobileAdminMenuButton = document.getElementById("mobile-admin-dropdown-button");
  const adminDropdown = document.getElementById("admin-dropdown");

  const mobileMenuButton = document.getElementById("mobile-menu-button");
  const mobileMenu = document.getElementById("mobile-menu");

  const clickedElement = event.target as Node;

  if (
    (adminDropdownButton && adminDropdownButton.contains(clickedElement)) ||
    (mobileAdminMenuButton && mobileAdminMenuButton.contains(clickedElement))
  ) {
    return;
  }

  if (mobileMenuButton && mobileMenuButton.contains(clickedElement)) {
    return;
  }

  if (adminDropdown && !adminDropdown.contains(clickedElement)) {
    adminDropdownOpen.value = false;
  }

  if (mobileMenu && !mobileMenu.contains(clickedElement)) {
    mobileMenuOpen.value = false;
  }
}
</script>
