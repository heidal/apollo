import "es6-promise/auto";
import Vue from "vue";
import VueCookies from "vue-cookies";
import App from "./App.vue";
import router from "./router";
import VueAxios from "vue-axios";
import { BootstrapVue, IconsPlugin } from "bootstrap-vue";
import axios from "axios";

import { makeServer } from "./server";
import store from "@/store";

Vue.config.productionTip = false;

if (process.env.NODE_ENV === "development") {
  makeServer();
}

Vue.use(VueCookies);
Vue.use(VueAxios, axios);
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

import "./custom.scss";

new Vue({
  router,
  store,
  render: (h) => h(App),
  mounted() {
    axios.interceptors.request.use(
      (config) => {
        // TODO make sure that the CSRFToken is not included in any requests going to external services.
        config.headers["X-CSRFToken"] = this.$cookies.get("csrftoken");
        return config;
      },
      (error) => Promise.reject(error)
    );
  },
}).$mount("#app");
