<template>
  <form @submit.prevent="createElection">
    <input type="text" placeholder="Type the title of the election" v-model="election.title" />
    <input type="text" placeholder="Add a description" v-model="election.description" />
    <button type="submit" class="submit">Submit</button>
  </form>
</template>
<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  data: function() {
    return {
      election: {
        title: null,
        description: null
      }
    };
  },
  created: function() {
    this.$store.getters.isAuthenticated;
  },
  methods: {
    createElection: function() {
      this.$http
        .post("/api/elections/elections/", this.election, {
          headers: {
            "X-CSRFToken": this.$cookies.get("csrftoken")
          }
        })
        .then(response => {
          console.log(response);
        });
    }
  }
});
</script>
