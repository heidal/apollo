<style scoped lang="scss">
.logout-form-wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding-top: 5em;
}
</style>

<template>
  <div class="logout-form-wrapper">
    <h3>Are you sure you want to logout?</h3>
    <b-form @submit.prevent="logout">
      <b-button type="submit" size="lg" variant="primary">Logout</b-button>
    </b-form>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  methods: {
    logout() {
      this.$http.post("/api/rest-auth/logout/").then(
        () => {
          this.$store.commit("setSessionKey", null);
          this.$router.push("/");
        },
        (error) => {
          if (error.response.status === 403) {
            this.$store.commit("setSessionKey", null);
            this.$router.push("/");
          }
        }
      );
    },
  },
});
</script>
