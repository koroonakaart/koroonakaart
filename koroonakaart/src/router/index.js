import Vue from "vue";
import VueRouter from "vue-router";

import Home from "../views/Home.vue";
import FrequentlyAskedQuestions from "../views/FrequentlyAskedQuestions.vue";

Vue.use(VueRouter);

/* const defaultLocale = this.$i18n.locale; */

const routes = [
  {
    path: "/",
    name: "root",
    beforeEnter(to, from, next) {
      next(localStorage.getItem("koroonaLang") ?? "et");
    },
  },
  {
    path: "/:locale/faq",
    name: "FrequentlyAskedQuestions",
    component: FrequentlyAskedQuestions,
  },
  {
    path: "/:locale",
    name: "Home",
    component: Home,
    children: [
      {
        path: "*",
        redirect: "/:locale",
      },
    ],
  },
];

const router = new VueRouter({
  routes,
  mode: "history",
});

export default router;
