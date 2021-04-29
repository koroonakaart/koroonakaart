import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: () => ({
    faqActive: false,
    currentChartName: null,
  }),

  mutations: {
    toggleFaqActive(state) {
      state.faqActive = true;
    },
    toggleFaqInactive(state) {
      state.faqActive = false;
    },
    setCurrentChartName(state, payload) {
      state.currentChartName = payload;
    },
  },

  actions: {
    toggleFaqActive(context) {
      context.commit("toggleFaqActive");
    },
    toggleFaqInactive(context) {
      context.commit("toggleFaqInactive");
    },
    setCurrentChartName(context, name) {
      context.commit("setCurrentChartName", name);
    },
  },
  modules: {},
});
