import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: () => ({
    faqActive: false,
    data: {},
    loaded: false
  }),

  getters: {
    cases: state => {
      return state.data.dataCumulativeCasesChart.cases;
    },
    caseDates: state => {
      return state.data.dates2;
    },
    vaccinationDates: state => {
      return state.data.dates3;
    },
    confirmedCasesByCounty: state => {
      return state.data.dataConfirmedCasesByCounty;
    },
    countyByDayNew: state => {
      return state.data.countyByDay.countyByDayNew;
    },
    activeMap100kPlayback: state => {
      return state.data.dataCountyDailyActive.activeMap100kPlayback;
    },
    dataActiveInfectionsByCounty: state => {
      return state.data.dataActiveInfectionsByCounty;
    },
    dataCumulativeCasesChart: state => {
      return state.data.dataCumulativeCasesChart;
    },
    dataCumulativeTestsChart: state => {
      return state.data.dataCumulativeTestsChart;
    },
    countyByDay: state => {
      return state.data.countyByDay.countyByDay;
    },
    // mapPlayback: state => {
    //   return state.data.countyByDay.mapPlayback;
    // },
    // mapPlayback10k: state => {
    //   return state.data.countyByDay.mapPlayback10k;
    // },
    newCountyByDay: state => {
      return state.data.countyByDay.newCountyByDay;
    },
    chartData: state => {
      return state.data;
    },
    // dataPositiveTestsByAgeChart: state => {
    //   return state.data.dataPositiveTestsByAgeChart;
    // },
    // countyByDay: state => {
    //   return state.data.countyByDay;
    // },
  },

  mutations: {
    toggleFaqActive(state) {
      state.faqActive = true;
    },
    toggleFaqInactive(state) {
      state.faqActive = false;
    },
    setData(state, payload) {
      state.data = payload;
      state.loaded = true;
    },
  },

  actions: {
    toggleFaqActive(context) {
      context.commit("toggleFaqActive");
    },
    toggleFaqInactive(context) {
      context.commit("toggleFaqInactive");
    },
    setData(context, data) {
      context.commit("setData", Object.freeze(data));
    },
  },
  modules: {},
});
