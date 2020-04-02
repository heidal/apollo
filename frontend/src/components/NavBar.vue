<style lang="scss" scoped>
.container {
  display: flex;
  justify-content: space-between;
}

.logo {
  height: 50px;
}

.logo-container:hover {
  cursor: pointer;
}

.logo-container {
  display: flex;

  h1 {
    margin: 0;
  }
}

.login-link {
  display: flex;
  padding-right: 3em;
  align-items: center;
}
</style>

<template>
  <div class="container">
    <div class="logo-container" v-on:click="goToHomePage">
      <img class="logo" src="@/assets/logo.png" />
      <h1>Apollo</h1>
    </div>
    <div class="login-link">
      <router-link v-if="!this.$store.getters.isAuthenticated" to="/login">Login</router-link>
      <router-link v-else to="/logout">Logout</router-link>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  methods: {
    goToHomePage: function() {
      this.$router.push("/");
    }
  }
});
</script>
