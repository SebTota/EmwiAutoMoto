<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <div class="z-50 bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-2xl font-bold mb-4">Ostrzeżenie</h2>
      <p class="text-gray-700 mb-6">
        Ta strona została przeniesiona do nowej domeny. Aby kontynuować, wejdź na stronę
        <a href="https://emwiautomoto.pl" class="text-blue-500 hover:underline">emwiautomoto.pl</a>
        ub kliknij przycisk poniżej.
      </p>
      <div class="flex justify-end">
        <button
          class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          @click="navigateToNewDomain"
        >
          Przejdź do nowej strony
        </button>
      </div>
    </div>
    <div class="fixed inset-0 backdrop-blur-sm backdrop-filter bg-black/50" @click.self="navigateToNewDomain"></div>
  </div>
</template>

<script setup lang="ts">
function navigateToNewDomain() {
  window.location.href = "https://emwiautomoto.pl";
}
</script>