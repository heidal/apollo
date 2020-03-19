<template>
  <div class="users">
    <h1>This is users page</h1>
    <p>Pretty useless but shouldn't work if you're not logged in.</p>
    <p>Registered users:</p>
    <ol id="users-list">
      <li v-for="user in users" :key="user.username">
        {{ user.username }}: {{ user.email }}
      </li>
    </ol>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

interface User {
  username: string;
  email: string;
}

export default Vue.extend({
  data: function() {
    return {
      users: [] as Array<User>
    };
  },
  methods: {
    loadUsers() {
      this.$http.get("/api/users/").then(
        response => {
          this.users = response.data;
        },
        () => {
          if (!this.$store.getters.isAuthenticated) {
            this.$router.push("/login");
          }
        }
      );
    }
  },
  beforeMount() {
    this.loadUsers();
  }
});
</script>
