import "es6-promise/auto";
import Vue from "vue";
import Vuex from "vuex";
import VueCookies from "vue-cookies";
import App from "./App.vue";
import router from "./router";
import VueAxios from 'vue-axios'
import axios from 'axios';


Vue.config.productionTip = false;
Vue.use(VueAxios, axios)
Vue.use(Vuex);
Vue.use(VueCookies);


const store = new Vuex.Store({
  state: {
    sessionKey: null as string | null
  },
  mutations: {
    setSessionKey(state, sessionKey: string) {
      state.sessionKey = sessionKey;
    }
  },
  getters: {
    isAuthenticated: state => {
      return state.sessionKey !== null;
    }
  }
})

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount("#app");
