import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

/* const defaultLocale = this.$i18n.locale; */

const routes = [
  {
    path: "/",
    redirect: `/${navigator?.language?.split("-")[0] ?? "et"}`
  },
  {
    path: "/api"
  },
  {
    path: "/:locale",
    name: "Home",
    component: Home
  },
  {
    path: "/:locale/*",
    redirect: "/"
  }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

export default router;
