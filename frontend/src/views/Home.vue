<template>
  <!-- Hero Section -->
  <section class="relative text-white text-center py-20 md:py-40 lg:py-60 bg-cover bg-center">
    <!-- Background image -->
    <div
      class="absolute inset-0 bg-cover bg-center"
      style="background-image: url('https://emwiautomotofilesr2.sebtota.com/488be40b-6b9c-4b1c-a03e-749e9007fc15.jpg')"
    ></div>

    <!-- Overlay for darkening the background -->
    <div class="absolute inset-0 bg-black opacity-50"></div>

    <!-- Content -->
    <div class="relative container mx-auto">
      <h1 class="text-2xl md:text-5xl font-bold">EMWI Auto-Moto</h1>
    </div>
  </section>

  <!-- Features Section -->
  <section class="py-16">
    <div class="px-4">
      <h2 class="text-3xl font-bold text-center text-gray-800">Nasze Produkty</h2>
      <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Motorcycles Card -->
        <router-link
          to="/motocykle"
          class="bg-white p-6 shadow-md rounded-lg transform transition duration-300 hover:scale-105 hover:shadow-xl cursor-pointer"
        >
          <img
            src="https://emwiautomotofilesr2.sebtota.com/488be40b-6b9c-4b1c-a03e-749e9007fc15.jpg"
            alt="Motorcycles"
            class="w-full h-48 object-cover rounded-lg"
          />
          <h3 class="text-xl font-semibold text-gray-800 mt-4">Motocykle</h3>
          <p class="mt-2 text-gray-600">Wyrusz na drogę ze stylem na naszych motocyklach z importu.</p>
        </router-link>

        <!-- Ride-on Mowers Card -->
        <router-link
          to="/traktory-ogrodowe"
          class="bg-white p-6 shadow-md rounded-lg transform transition duration-300 hover:scale-105 hover:shadow-xl cursor-pointer"
        >
          <img
            src="https://emwiautomotofilesr2.sebtota.com/9a9f30a1-c4d3-40c2-b0a9-722a08452bc1.jpeg"
            alt="Ride-on Mowers"
            class="w-full h-48 object-cover rounded-lg"
          />
          <h3 class="text-xl font-semibold text-gray-800 mt-4">Traktory Ogrodowe</h3>
          <p class="mt-2 text-gray-600">Ułatw sobie pielęgnację trawnika dzięki naszym traktorom ogrodowym.</p>
        </router-link>

        <!-- Parts & Accessories Card -->
        <router-link
          to="/czesci-i-akcesoria"
          class="bg-white p-6 shadow-md rounded-lg transform transition duration-300 hover:scale-105 hover:shadow-xl cursor-pointer"
        >
          <img
            src="https://emwiautomotofilesr2.sebtota.com/c20d2970-781e-4917-9865-aa10e573ad38.jpg"
            alt="Parts & Accessories"
            class="w-full h-48 object-cover rounded-lg"
          />
          <h3 class="text-xl font-semibold text-gray-800 mt-4">Części i Akcesoria</h3>
          <p class="mt-2 text-gray-600">
            Znajdź idealne części i akcesoria do personalizacji i utrzymania swojego pojazdu.
          </p>
        </router-link>
      </div>
    </div>
  </section>

  <!-- Testimonial Section -->
  <section class="bg-gray-100 py-16">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center text-gray-800">Opinie naszych klientów</h2>
      <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="bg-white p-6 shadow-md rounded-lg">
          <p class="text-gray-600 italic">
            "Polecam kontakt i zakup motocykla w firmie EMWI! Bardzo dobry kontakt! Mega szybko wysyłane fotki i filmy
            moto już z USA! Extra obsługa w Polsce! Dokumenty do rejestracji gotowe w 10 dni, wszystko kompletne i
            gotowe. POLECAM!"
          </p>
          <div class="mt-4">
            <h4 class="text-lg font-semibold text-gray-800">Andrzej Budzyński</h4>
            <a
              class="text-gray-500"
              href="https://www.facebook.com/andrzej.budzynski.359/posts/pfbid0rd6KosY6jrEJYtomHxqUqfCpEFvhVciVXGrJStoUCxgkWVgKyEyLfHc4he8KGVuWl"
              target="_blank"
              >Facebook</a
            >
          </div>
        </div>

        <div class="bg-white p-6 shadow-md rounded-lg">
          <p class="text-gray-600 italic">
            "Chyba jedyny uczciwy sprzedawca motocykli. Polecam. Kupilem od niego 2 szt wszystko ok."
          </p>
          <div class="mt-4">
            <h4 class="text-lg font-semibold text-gray-800">Gustaw</h4>
            <a class="text-gray-500" href="https://g.co/kgs/zn3B5u9" target="_blank">Google</a>
          </div>
        </div>

        <div class="bg-white p-6 shadow-md rounded-lg">
          <p class="text-gray-600 italic">
            "Ja też polecam zakup motocykla w tej firmie. Moja Yamaha sprowadzona ze Stanów jest w super stanie. Dobry
            kontakt ze sprzedającym, zdjęcia motocykla na bieżąco. Polecam!"
          </p>
          <div class="mt-4">
            <h4 class="text-lg font-semibold text-gray-800">Heniek Rzepa</h4>
            <a
              class="text-gray-500"
              href="https://www.facebook.com/permalink.php?story_fbid=pfbid02v87WyQgy9Wz4oXjyuf7xoyj1AqQgW94QhxToB7j38MQVM9pWbTRt6SpoDda9R289l&id=100010608094605"
              target="_blank"
              >Facebook</a
            >
          </div>
        </div>
      </div>

      <!-- Links to more reviews -->
      <div class="mt-12 text-center">
        <p class="text-gray-700 text-lg font-semibold">Zobacz, co mówią inni:</p>
        <div class="flex justify-center mt-6 space-x-6">
          <a
            href="https://maps.app.goo.gl/WreqLtBbyH5Cay1H9"
            target="_blank"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-full shadow-md hover:bg-indigo-500 transition"
          >
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M12 0C5.4 0 0 5.4 0 12c0 5.5 3.7 10.1 8.7 11.5.6.1.8-.3.8-.6V19c-3.5.8-4.2-1.4-4.2-1.4-.5-1.2-1.2-1.5-1.2-1.5-.9-.7.1-.7.1-.7 1 0 1.6 1 1.6 1 .9 1.6 2.3 1.1 2.9.9.1-.7.3-1.1.6-1.4-2.8-.3-5.8-1.4-5.8-6.3 0-1.4.5-2.5 1.2-3.4-.1-.3-.5-1.4.1-2.9 0 0 1-.3 3.5 1.3 1-.3 2.1-.5 3.2-.5 1.1 0 2.2.2 3.2.5 2.5-1.6 3.5-1.3 3.5-1.3.6 1.5.2 2.6.1 2.9.8.9 1.2 2 1.2 3.4 0 4.9-3 6-5.9 6.3.4.4.7 1 .7 2v2.9c0 .3.2.7.8.6C20.3 22.1 24 17.5 24 12 24 5.4 18.6 0 12 0z"
              />
            </svg>
            Opinie Google
          </a>
          <a
            href="https://www.facebook.com/emwifhu/reviews"
            target="_blank"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-full shadow-md hover:bg-indigo-500 transition"
          >
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M22.675 0H1.325C.593 0 0 .593 0 1.325v21.351C0 23.407.593 24 1.325 24H12.82v-9.294H9.692V10.82h3.128V8.413c0-3.1 1.893-4.787 4.657-4.787 1.325 0 2.462.099 2.795.143v3.24l-1.918.001c-1.503 0-1.794.715-1.794 1.763v2.312h3.587l-.467 3.886H16.56V24h6.115c.732 0 1.325-.593 1.325-1.325V1.325C24 .593 23.407 0 22.675 0z"
              />
            </svg>
            Opinie na Facebooku
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Call to Action Section -->
  <section class="bg-gray-200 py-16">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl font-bold text-gray-800">Nie możesz znaleźć motocykla lub akcesorium, o którym myślałeś?</h2>
      <p class="mt-4 text-gray-600">Skontaktuj się z nami, a upewnimy się, że otrzymasz to, czego szukasz!</p>
      <router-link
        to="/kontakt"
        class="mt-8 px-6 py-2 bg-indigo-600 text-white font-semibold rounded-full shadow-lg hover:bg-indigo-500 inline-block"
      >
        Skontaktuj się z nami
      </router-link>
    </div>
  </section>
</template>

<script setup lang="ts"></script>
