import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: () => ({
    dataFromGoogleSheets: {},
    faqActive: false
  }),
  mutations: {
    fetchDataFromGoogleSheets(state, payload) {
      state.dataFromGoogleSheets = payload;
    },
    toggleFaqActive(state) {
      state.faqActive = true;
    },
    toggleFaqInactive(state) {
      state.faqActive = false;
    }
  },

  actions: {
    fetchDataFromGoogleSheets(context) {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/list/1Kw3dbiK7wnQsGBSfHlTJH8JQ7SYY9rrwaC9G3zpqxBU/od6/public/values?alt=json"
        )
        .then(response =>
          context.commit("fetchDataFromGoogleSheets", response.data.feed)
        )
        .catch(error => console.log(error.message));
    },
    toggleFaqActive(context) {
      context.commit("toggleFaqActive");
    },
    toggleFaqInactive(context) {
      context.commit("toggleFaqInactive");
    }
  },
  modules: {}
});
