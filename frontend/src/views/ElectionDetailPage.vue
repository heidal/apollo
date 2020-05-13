<template>
  <div v-if="election !== null">
    <h1>{{ election.title }}</h1>
    <p>{{ election.description }}</p>
    <p>A total of {{ election.questions.length }} questions</p>
    <p>and {{ election.questions.flatMap(q => q.answers).length }} answers</p>

    <div v-if="election.is_owned">
      <template v-if="election.state == 'CREATED'">
        <h4>Election is not yet opened, you can edit or open it</h4>
        <p><button v-on:click="editElection()">Edit election</button></p>
        <p><button v-on:click="openElection()">Open election</button></p>
      </template>
      <template v-else-if="election.state == 'OPENED'">
        <h4>Election is opened</h4>
        <p><button v-on:click="voteInElection()">Vote in this election!</button></p>
        <p><button v-on:click="closeElection()">Close election and count votes</button></p>
      </template>
      <template v-else-if="election.state == 'CLOSED'">
        <h4>Election is closed</h4>
        <p><button v-on:click="showElectionResults()">See election results</button></p>
      </template>
    </div>
    <div v-else>
      <template v-if="election.state == 'CREATED'">
        <h4>Election is not yet opened</h4>
      </template>
      <template v-else-if="election.state == 'OPENED'">
        <p><button v-on:click="voteInElection()">Vote in this election!</button></p>
      </template>
      <template v-else-if="election.state == 'CLOSED'">
        <h4>Election is closed</h4>
        <p><button v-on:click="showElectionResults()">See election results</button></p>
      </template>
    </div>
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
    editElection: function() {
      alert("Editing election not implemented yet");
    },
    openElection: function() {
      if (this.election === null) {
        return;
      }
      this.$http.post(`/api/elections/elections/${this.election.id}/open/`, {})
        .then(response => {
          if (this.election !== null) {
            this.election.state = response.data.state_string;
          }
        });
    },
    voteInElection: function() {
      if (this.election === null) {
        return;
      }
      this.$router.push(`/vote/${this.election.id}`)
    },
    closeElection: function() {
      if (this.election === null) {
        return;
      }
      this.$http.post(`/api/elections/elections/${this.election.id}/close/`, {})
        .then(response => {
          if (this.election !== null) {
            this.election.state = response.data.state_string;
          }
        });
    },
    showElectionResults: function() {
      if (this.election === null) {
        return;
      }
      this.$router.push(`/election-detail/${this.election.id}/results`);
    }
  }
});
</script>
