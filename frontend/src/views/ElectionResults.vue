<style scoped lang="scss">
.election-results {
  max-width: 30rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5rem;
}
</style>
<template>
  <b-card v-if="election" class="election-results" :title="election.title">
    <b-card-body>
      <b-card-text>
        <p>{{ election.description }}</p>
        <div v-for="(question, i) in election.questions" :key="i">
          <hr class="my-4" />
          <p>Question #{{ i + 1 }}</p>
          <h3>{{ question.question }}</h3>
          <b-table
            striped
            hover
            :items="question.answers"
            :fields="fields"
          ></b-table>
        </div>
      </b-card-text>
    </b-card-body>
  </b-card>
</template>
<script lang="ts">
import Vue from "vue";
import { ApiElectionSummary } from "@/api/elections";

export default Vue.extend({
  data: function() {
    return {
      election: null as ApiElectionSummary | null,
      fields: [
        {
          key: "votes",
          sortable: true
        },
        {
          key: "text",
          label: "Answer",
          sortable: true
        }
      ]
    };
  },
  created: function() {
    const electionId = this.$router.currentRoute.params.electionId;
    this.$http
      .get(`/api/elections/elections/${electionId}/summary`)
      .then(response => {
        this.election = response.data;
      });
  }
});
</script>
