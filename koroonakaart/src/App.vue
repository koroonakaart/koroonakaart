<template>
  <div>
    <div v-if="urlIncludesChart" id="app">
      <router-view class="router-view" />
    </div>
    <div v-else id="app">
      <Navbar />
      <router-view class="router-view" />
      <Footer />
    </div>
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";
import axios from "axios";

export default {
  name: "App",
  components: {
    Navbar,
    Footer,
  },

  created() {
    // When app loads change language to specified language suffix (ee, en or ru)
    if (this.$i18n.locale !== this.$route.params.locale)
      this.changeCurrentLanguage(this.$route.params.locale);

    // Load data
    this.loadData();
  },

  computed: {
    urlIncludesChart: function () {
      return this.$route.path.includes("chart");
    },
  },

  methods: {
    changeCurrentLanguage: function (targetLanguage) {
      if (this.$route.params.locale !== targetLanguage) {
        this.$router.push(targetLanguage);
      }
      this.$i18n.locale = targetLanguage;
    },
    loadData: function () {
      // Load data required for statsbar and charts
      axios.get('https://koroonakaart.ee/data.json')
      .then((response) => {
        // // Debug
        // alert('Data received()');
        // Save data to store
        this.$store.dispatch('setData', response.data);
        console.log('Loaded data');
        // console.log('store.data:');
        // console.log(this.$store.state.data);
      })
      .catch(function (error) {
        console.log('Error when loading data:');
        console.log(error);
      });
    },
  },
};
</script>

<style>
#app {
  font-family: "Roboto", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  text-align: center;
  /* width: 100% !important; */
}

.router-view {
  margin-top: 20px;
  flex: 1;
}
</style>
