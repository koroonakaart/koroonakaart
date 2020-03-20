import "@babel/polyfill";
import "mutationobserver-shim";
import Vue from "vue";
import "./plugins/bootstrap-vue";
import i18n from "./i18n";
import HighchartsVue from "highcharts-vue";
import Highcharts from "highcharts";
import mapInit from "highcharts/modules/map";
import VueAnalytics from 'vue-analytics';

import App from "./App.vue";
import router from "./router";
import store from "./store";

import "vue-material-design-icons/styles.css";

mapInit(Highcharts);

Vue.use(HighchartsVue);

Vue.config.productionTip = false;

// Configuration VueAnalytics
Vue.use(VueAnalytics, {
  id: 'UA-86124786-3',
  router
});


new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount("#app");
