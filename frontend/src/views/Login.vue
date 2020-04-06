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
  <div class="login">
    <p>Login with your password</p>
    <form @submit.prevent="loginWithPassword" class="login-form">
      <label>
        <input type="text" v-model="user.username" placeholder="Username" />
      </label>
      <label>
        <input type="password" v-model="user.password" placeholder="Password" />
      </label>
      <button type="submit" class="submit">Submit</button>
      <p>
        Or
        <router-link to="/signup">signup</router-link>
      </p>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data: function() {
    return {
      user: {
        username: null,
        password: null
      }
    };
  },
  methods: {
    loginWithPassword() {
      this.$http.post("/api/rest-auth/login/", this.user).then(
        response => {
          this.$store.commit("setSessionKey", response.data.key);
          this.$router.push("/");
        },
        error => {
          console.error(error);
        }
      );
    }
  },
  computed: {
    isLogged() {
      return this.$store.state.sessionKey === null;
    }
  }
});
</script>