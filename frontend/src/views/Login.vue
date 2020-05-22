<style scoped lang="scss">
.login-form-wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding-top: 5em;
}

.login-form {
  max-width: 20em;
}
</style>

<template>
  <div class="login-form-wrapper">
    <b-card class="mb-2 login-form" title="Login">
      <b-form @submit.prevent="loginWithPassword">
        <b-form-group
          id="input-group-1"
          label="Email"
          label-for="input-1"
          type="email"
        >
          <b-form-input
            id="input-1"
            v-model="user.email"
            required
            placeholder="Enter email"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Password" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="user.password"
            type="password"
            required
            placeholder="Enter password"
          ></b-form-input>
        </b-form-group>
        <b-form-invalid-feedback id="invalid-feedback" :state="noErrors">
          {{ errors.nonFieldErrors[0] }}
        </b-form-invalid-feedback>
        <b-button type="submit" variant="primary">Submit</b-button>
        <p>
          Or
          <router-link to="/signup">signup</router-link>
        </p>
      </b-form>
    </b-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Dictionary } from "vue-router/types/router";

interface Errors {
  nonFieldErrors: Array<string>;
}

export default Vue.extend({
  data() {
    return {
      user: {
        password: null,
        email: null
      },
      errors: {
        nonFieldErrors: []
      } as Errors
    };
  },
  computed: {
    isLogged(): boolean {
      return this.$store.state.sessionKey === null;
    },
    noErrors(): boolean {
      return this.errors.nonFieldErrors.length === 0;
    }
  },
  methods: {
    loginWithPassword() {
      this.$http.post("/api/rest-auth/login/", this.user).then(
        response => {
          // the TS error below is due to some bug in vue-router
          /* eslint-disable @typescript-eslint/ban-ts-ignore */
          // @ts-ignore
          const query: Dictionary<string> = this.$route.query;
          this.$store.commit("setSessionKey", response.data.key);
          this.$router.push(query.next || "/");
        },
        error => {
          this.errors.nonFieldErrors =
            error.response.data["non_field_errors"] ?? [];
        }
      );
    }
  }
});
</script>
