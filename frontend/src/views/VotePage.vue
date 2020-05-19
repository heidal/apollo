<template>
  <election-vote-form
    v-if="election"
    :election="election"
    :vote-error="voteError"
    @votesSubmitted="voteInElection"
  ></election-vote-form>
</template>
<script lang="ts">
import Vue from "vue";
import { ApiElection } from "@/api/elections";
import ElectionVoteForm, { Vote } from "@/components/ElectionVoteForm.vue";
import { AxiosError } from "axios";

export default Vue.extend({
  components: {
    ElectionVoteForm,
  },
  data: function () {
    return {
      election: null as ApiElection | null,
      voteError: null as string | null,
    };
  },
  created: function () {
    const electionId = this.$router.currentRoute.params.electionId;
    this.$http
      .get(`/api/elections/elections/${electionId}/`)
      .then((response) => {
        this.election = response.data;
      });
  },
  methods: {
    voteInElection: function (votes: Array<Vote>) {
      const results = votes.map((vote) => {
        if (vote.selected === null) {
          return Promise.reject("Vote is null");
        }

        const [question, answer] = vote.selected.split(".");

        return this.$http.post("/api/elections/votes/", { answer });
      });
      Promise.all(results).then(
        () => {
          this.$router.push("/");
        },
        (error) => {
          this.handleErrors(error);
        }
      );
    },
    handleErrors(error: AxiosError) {
      if (error.response?.status === 403) {
        this.voteError = "You're not authorized to vote in this election.";
      } else {
        this.voteError = `Unknown error: ${error.response?.data}`;
      }
    },
  },
});
</script>
