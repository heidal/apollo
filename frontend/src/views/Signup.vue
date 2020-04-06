<style scoped lang="scss">
.signup-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  height: 15em;
}

.submit {
  width: 10em;
}
</style>

<template>
  <div class="signup">
    <p>Login with your password</p>
    <form @submit.prevent="loginWithPassword" class="signup-form">
      <label>
        <input type="text" v-model="user.username" placeholder="Username" />
      </label>
      <label>
        <input type="email" v-model="user.email" placeholder="Email" />
      </label>
      <label>
        <input type="password" v-model="user.password1" placeholder="Password" />
      </label>
      <label>
        <input type="password" v-model="user.password2" placeholder="Confirm password" />
      </label>
      <button type="submit" class="submit">Submit</button>
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
        password1: null,
        password2: null,
        email: null
      }
    };
  },
  methods: {
    loginWithPassword() {
      this.$http.post("/api/rest-auth/registration/", this.user).then(
        () => {
          this.$router.push("/login");
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