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
  text-align: center;
  color: #2c3e50;
  padding-top: 1em;
  padding-left: 5em;
  padding-right: 5em;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script lang="ts">
import Vue from 'vue';
import NavBar from "@/components/NavBar.vue";
export default Vue.extend({
  components: {
    NavBar
  }
})
</script>
