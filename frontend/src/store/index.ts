import Vuex from "vuex";
import Vue from "vue";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    sessionKey: null as string | null,
  },
  mutations: {
    setSessionKey(state, sessionKey: string | null) {
      if (sessionKey === null) {
        Vue.$cookies.remove("sessionKey");
      } else {
        Vue.$cookies.set("sessionKey", sessionKey);
      }
      state.sessionKey = sessionKey;
    },
  },
  getters: {
    isAuthenticated: (state) => {
      if (state.sessionKey === null) {
        const sessionKey = Vue.$cookies.get("sessionKey");
        if (sessionKey == null) {
          return false;
        }
        state.sessionKey = sessionKey;
        return true;
      }
      return true;
    },
  },
});
