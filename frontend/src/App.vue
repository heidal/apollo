<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

<script lang="ts">
import Vue from "vue";
import NavBar from "@/components/NavBar.vue";
export default Vue.extend({
  components: {
    NavBar
  }
});
</script>
