<style scoped lang="scss">

.signup-form-wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding-top: 5em;
}

.signup-form {
  max-width: 20em;
}
</style>

<template>
  <div class="signup-form-wrapper">
    <b-card class="signup-form mb-2"
      title="Signup"
    >
      <b-form @submit.prevent="signupWithPassword">
        <b-form-group
          id="username-input-group"
          label="Username"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="user.username"
            required
            placeholder="Enter username"
          ></b-form-input>
          <b-form-invalid-feedback
            id="invalid-username"
            :state="noErrors('username')"
          >
          {{ errors.username[0] }}
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group
          id="email-input-group"
          label="Email"
          label-for="input-1"
        >
          <b-form-input
            id="email-input"
            v-model="user.email"
            type="email"
            required
            placeholder="Enter email"
          ></b-form-input>
          <b-form-invalid-feedback
            id="invalid-email"
            :state="noErrors('email')"
          >
          {{ errors.email[0] }}
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group id="password-input-group" label="Password" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="user.password1"
            type="password"
            required
            placeholder="Enter password"
          ></b-form-input>
          <b-form-invalid-feedback
            id="invalid-password1"
            :state="noErrors('password1')"
          >
              {{ errors.password1[0] }}
          </b-form-invalid-feedback>

          <b-form-input
            id="input-2"
            v-model="user.password2"
            type="password"
            required
            placeholder="Confirm password"
          ></b-form-input>
        </b-form-group>
      <b-form-invalid-feedback
            id="invalid-password2"
            :state="noErrors('password2')"
          >
              {{ errors.password2[0] }}
          </b-form-invalid-feedback>
        <b-button type="submit" variant="primary">Submit</b-button>


        <b-form-invalid-feedback
          id="invalid-feedback"
          :state="noErrors()"
        >
          {{ errors.nonFieldErrors[0] }}
        </b-form-invalid-feedback>
      </b-form>
    </b-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      user: {
        username: null,
        password1: null,
        password2: null,
        email: null
      },
      errors: {
        username: [],
        password1: [],
        password2: [],
        email: [],
        nonFieldErrors: []
      } as { [key: string]: Array<string> }
    };
  },
  methods: {
    signupWithPassword() {
      this.$http.post("/api/rest-auth/registration/", this.user).then(
        () => {
          this.$router.push("/login");
        },
        error => {
          const newErrors = error.response.data;
          this.errors = {
            username: newErrors.username ?? [],
            password1: newErrors.password1 ?? [],
            password2: newErrors.password2 ?? [],
            email: newErrors.email ?? [],
            nonFieldErrors: newErrors.non_field_errors ?? []
          };
        }
      );
    },
    noErrors(label?: string) {
      return this.errors[label ?? "nonFieldErrors"].length === 0;
    }
  },
  computed: {
    isLogged() {
      return this.$store.state.sessionKey === null;
    },
  }
});
</script>
