<style scoped lang="scss">
.election-details {
  max-width: 50rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5rem;
}
</style>

<template>
  <b-card class="election-details">
    <b-card-title class="d-flex w-100 justify-content-between">
      <h3>{{ election.title }}</h3>
      <b-button
        v-if="election.state !== 'CREATED' && election.did_vote"
        v-b-modal.modal-1
        variant="danger"
        @click="getVoterSeedHash()"
      >
        Show my Voter Seed Hash
      </b-button>
      <b-modal id="modal-1" title="Voter Seed Hash">
        <p class="my-4">Warning: don't share it with anybody</p>
        <code v-if="voterSeedHash">{{ voterSeedHash.user_seed_hash }}</code>
        <p v-else>Loading...</p>
        <template v-slot:modal-footer>
          <div class="w-100">
            <p class="float-left small">
              To find your vote on the Bulletin Board, decode the hash using
              <code>Base64</code> and pass it concatenated with your email
              address to <code>SHA3-256</code>.
              <br />
              In pseudocode:
              <code
                >Base64.Encode(SHA3_256(Base64.Decode(seedHash), email))</code
              >
              <br />
            </p>
          </div>
        </template>
      </b-modal>
    </b-card-title>
    <b-card-sub-title>
      {{ election.description }}
    </b-card-sub-title>
    <b-card-body>
      <b-card-text>
        <div class="d-flex w-100 align-items-center">
          <b-badge :variant="getVariant(election)" pill>{{
            election.state
          }}</b-badge>
          <b-badge variant="primary" pill
            >{{ election.questions.length }} question{{
              election.questions.length !== 1 ? "s" : ""
            }}</b-badge
          >
        </div>
      </b-card-text>
      <template v-if="election.state === 'OPENED'">
        <p v-if="canVoteInElection && !election.did_vote">
          <b-button @click="voteInElection()">Vote in this election!</b-button>
        </p>
        <p v-else-if="canVoteInElection && election.did_vote">
          <b-button disabled
            >Voting multiple times not yet implemented</b-button
          >
        </p>
        <p v-else>
          <b-button disabled variant="outline-dark"
            >You're not authorized to vote in this election</b-button
          >
        </p>
      </template>
      <template v-else-if="election.state === 'CLOSED'">
        <p>
          <b-button variant="success" @click="showElectionResults()"
            >See election results</b-button
          >
        </p>
      </template>
      <template v-if="election.state !== 'CREATED'">
        <b-button variant="info" @click="showBulletinBoard()"
          >Show bulletin board</b-button
        >
      </template>
    </b-card-body>
    <b-card-footer v-if="election.is_owned">
      <h5>Election Admin panel</h5>
      <template v-if="election.state === 'CREATED'">
        <p><b-button @click="editElection()">Edit election</b-button></p>
        <p>
          <b-button variant="warning" @click="openElection()"
            >Open election</b-button
          >
        </p>
      </template>
      <template v-else-if="election.state === 'OPENED'">
        <p>
          <b-button variant="warning" @click="closeElection()"
            >Close election and count votes</b-button
          >
        </p>
      </template>
    </b-card-footer>
  </b-card>
</template>

<script lang="ts">
import Vue from "vue";
import { ApiElection } from "@/api/elections";

export default Vue.extend({
  props: {
    election: ApiElection
  },
  data() {
    return {
      voterSeedHash: null as string | null
    };
  },
  computed: {
    canVoteInElection() {
      return (this.election?.permissions.indexOf("CAN_VOTE") ?? -1) > -1;
    }
  },
  methods: {
    editElection() {
      this.$router.push(`/edit-election/${this.election.id}/`);
    },
    openElection() {
      this.$http
        .post(`/api/elections/elections/${this.election.id}/open/`, {})
        .then(response => {
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
        .then(response => {
          this.election.state = response.data.state_string;
        });
    },
    showElectionResults() {
      this.$router.push(`/election-detail/${this.election.id}/results`);
    },
    showBulletinBoard() {
      this.$router.push(`/bulletin-board/${this.election.id}`);
    },
    getVariant(election: ApiElection): string {
      const variants: { [key: string]: string } = {
        CREATED: "info",
        OPENED: "warning",
        CLOSED: "info"
      };
      return variants[election.state];
    },
    getVoterSeedHash() {
      this.$http
        .get(`/api/elections/elections/${this.election.id}/me/`)
        .then(response => {
          this.voterSeedHash = response.data;
        });
    }
  }
});
</script>
