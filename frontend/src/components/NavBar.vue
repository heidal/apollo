<style lang="scss" scoped>
.logo {
  max-height: 50px;
}
</style>

<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand to="/">
      <img class="logo" src="@/assets/logo.svg" />
      Votifica
    </b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <b-nav-item to="/elections">Elections</b-nav-item>
      <b-nav-item v-if="!this.$store.getters.isAuthenticated" to="/login"
        >Login</b-nav-item
      >
      <b-nav-item v-else to="/logout" href="/logout#">Logout</b-nav-item>
    </b-navbar-nav>
  </b-navbar>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({});
</script>
