<style scoped lang="scss">
.election-details {
  text-align: center;
  max-width: 30rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5rem;
}
</style>

<template>
  <b-card class="election-details" :title="election.title">
    <b-card-body>
      <b-card-text>
        <p>{{ election.description }}</p>
        <p>A total of {{ election.questions.length }} questions</p>
        <p>
          and {{ election.questions.flatMap((q) => q.answers).length }} answers
        </p>
      </b-card-text>
      <div v-if="election.is_owned">
        <template v-if="election.state === 'CREATED'">
          <h4>Election is not yet opened, you can edit or open it</h4>
          <p><b-button v-on:click="editElection()">Edit election</b-button></p>
          <p>
            <b-button v-on:click="openElection()" variant="warning"
              >Open election</b-button
            >
          </p>
        </template>
        <template v-else-if="election.state === 'OPENED'">
          <h4>Election is opened</h4>
          <p v-if="canVoteInElection">
            <b-button v-on:click="voteInElection()"
              >Vote in this election!</b-button
            >
          </p>
          <p v-else>
            <b-button
              disabled
              variant="outline-dark"
              >You're not authorized to vote in this election</b-button
            >
          </p>
          <p>
            <b-button v-on:click="closeElection()" variant="warning"
              >Close election and count votes</b-button
            >
          </p>
        </template>
        <template v-else-if="election.state === 'CLOSED'">
          <h4>Election is closed</h4>
          <p>
            <b-button v-on:click="showElectionResults()"
              >See election results</b-button
            >
          </p>
        </template>
      </div>
      <div v-else>
        <template v-if="election.state === 'CREATED'">
          <h4>Election is not yet opened</h4>
        </template>
        <template v-else-if="election.state === 'OPENED'">
          <p v-if="canVoteInElection">
            <b-button v-on:click="voteInElection()"
              >Vote in this election!</b-button>
          </p>
          <p v-else>
            <b-button
              disabled
              variant="outline-dark"
              >You're not authorized to vote in this election</b-button
            >
          </p>
        </template>
        <template v-else-if="election.state === 'CLOSED'">
          <h4>Election is closed</h4>
          <p>
            <b-button v-on:click="showElectionResults()" variant="success"
              >See election results</b-button
            >
          </p>
        </template>
      </div>
    </b-card-body>
  </b-card>
</template>

<script>
import Vue from "vue";
import { ApiElection } from "@/api/elections";

export default Vue.extend({
  props: {
    election: ApiElection,
  },
  methods: {
    editElection() {
      alert("Editing election not implemented yet");
    },
    openElection() {
      this.$http
        .post(`/api/elections/elections/${this.election.id}/open/`, {})
        .then((response) => {
          if (this.election !== null) {
            this.election.state = response.data.state_string;
          }
        });
    },
    voteInElection() {
      this.$router.push(`/vote/${this.election.id}`);
    },
    closeElection() {
      this.$http
        .post(`/api/elections/elections/${this.election.id}/close/`, {})
        .then((response) => {
          this.election.state = response.data.state_string;
        });
    },
    showElectionResults() {
      this.$router.push(`/election-detail/${this.election.id}/results`);
    },

  },
  computed: {
    canVoteInElection() {
      return (this.election?.permissions.indexOf("CAN_VOTE") ?? -1) > -1;
    }
  }
});
</script>
