import "es6-promise/auto";
import Vue from "vue";
import Vuex from "vuex";
import VueCookies from "vue-cookies";
import App from "./App.vue";
import router from "./router";
import VueAxios from 'vue-axios'
import axios from 'axios';

import { makeServer } from "./server";

Vue.config.productionTip = false;

if (process.env.NODE_ENV === "development") {
  makeServer();
}

Vue.use(VueCookies);
Vue.use(VueAxios, axios);
Vue.use(Vuex);


const store = new Vuex.Store({
  state: {
    sessionKey: null as string | null
  },
  mutations: {
    setSessionKey(state, sessionKey: string) {
      Vue.$cookies.set("sessionKey", sessionKey);
      state.sessionKey = sessionKey;
    }
  },
  getters: {
    isAuthenticated: state => {
      if (state.sessionKey === null) {
        const sessionKey = Vue.$cookies.get("sessionKey");
        if (sessionKey === null) {
          return false;
        }
        state.sessionKey = sessionKey;
        return true;
      }
      return true;
    }
  }
})

new Vue({
  router,
  store,
  render: h => h(App),
  mounted () {
    axios.interceptors.request.use(
      config => {
        // TODO make sure that the CSRFToken is not included in any requests going to external services.
        config.headers["X-CSRFToken"] = this.$cookies.get("csrftoken");
        return config;
      },
      error => Promise.reject(error)
    )
  }
}).$mount("#app");