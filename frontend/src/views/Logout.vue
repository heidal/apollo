<style scoped lang="scss">
.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  height: 10em;
}

.submit {
  width: 10em;
}
</style>

<template>
  <div class="logout">
    <p>Are you sure you want to logout?</p>
    <form @submit.prevent="logout" class="logout-form">
      <button type="submit" class="submit">Logout</button>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  methods: {
    logout() {
      this.$http
        .post(
          "/api/rest-auth/logout/",
          {},
          {
            headers: {
              "X-CSRFToken": this.$cookies.get("csrftoken")
            }
          }
        )
        .then(
          () => {
            this.$store.commit("setSessionKey", null);
            this.$router.push("/");
          },
          error => {
            if (error.response.status === 403) {
              this.$store.commit("setSessionKey", null);
              this.$router.push("/");
            }
          }
        );
    }
  }
});
</script>
