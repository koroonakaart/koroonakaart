<template>
  <div v-if="urlIncludesChart" id="app">
    <router-view class="router-view" />
  </div>

  <div v-else id="app">
    <!-- <DisclaimerModal /> -->
    <Navbar />
    <router-view class="router-view" />
    <Footer />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    Navbar,
    Footer
  },

  // When app loads change language to specified language suffix (ee, en or ru)
  created() {
    if (this.$i18n.locale !== this.$route.params.locale)
      this.changeCurrentLanguage(this.$route.params.locale);
  },

  computed: {
    urlIncludesChart: function() {
      return this.$route.path.includes("chart");
    }
  },

  methods: {
    changeCurrentLanguage: function(targetLanguage) {
      if (this.$route.params.locale !== targetLanguage) {
        this.$router.push(targetLanguage);
      }
      this.$i18n.locale = targetLanguage;
    }
  }
};
</script>

<style>
#app {
  font-family: "Roboto", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.router-view {
  flex: 1;
}
</style>
