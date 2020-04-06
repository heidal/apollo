<template>
  <div v-if="election !== null">
    <h1>{{ election.title }}</h1>
    <p>{{ election.description }}</p>
    <p>A total of {{ election.questions.length }} questions</p>
    <p>and {{ election.questions.flatMap(q => q.answers).length }} answers</p>
    <button v-on:click="voteInElection()">Vote in this election!</button>
  </div>
</template>
<script lang="ts">
import Vue from "vue";

import { ApiElection } from "@/api/elections";

export default Vue.extend({
  data: function() {
    return {
      election: null as ApiElection | null
    };
  },
  created: function() {
    const electionId = this.$router.currentRoute.params.electionId;
    this.$http.get(`/api/elections/elections/${electionId}`).then(response => {
      this.election = response.data;
    });
  },
  methods: {
    voteInElection: function() {
      if (this.election === null) {
        return;
      }
      this.$router.push(`/vote/${this.election.id}`)
    }
  }
});
</script>
