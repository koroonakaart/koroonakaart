<template>
  <div id="app">
    <DisclaimerModal />

    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

import DisclaimerModal from "./components/DisclaimerModal";

export default {
  name: "App",
  components: {
    Navbar,
    Footer,
    DisclaimerModal
  },

  // When app loads change language to specified language suffix (ee, en or ru)
  created() {
    if (this.$i18n.locale !== this.$route.params.locale)
      this.changeCurrentLanguage(this.$route.params.locale);
  },
  mounted() {
    this.$bvModal.show("disclaimer-modal");
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
  min-height: 100vh;
}
</style>
