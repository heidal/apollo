<template>
  <form v-if="election !== null" @submit.prevent="voteInElection()">
    <h1>{{ election.title }}</h1>
    <p>{{ election.description }}</p>
    <div v-for="(question, i) in election.questions" :key="i">
      <p>Question #{{ i + 1 }}</p>
      <h3>{{ question.question }}</h3>
      <div v-for="(answer, ai) in question.answers" :key="ai">
        <input
          required
          type="radio"
          :id="`${i}.${ai}`"
          :name="`answer.${i}`"
          :value="`${question.id}.${answer.id}`"
          v-model="votes[i].selected"
        />
        <label :for="`${i}.${ai}`">{{ answer.text }}</label>
        <br />
      </div>
    </div>
    <button type="submit" class="submit">Send votes</button>
  </form>
</template>
<script lang="ts">
import Vue from "vue";

import { ApiElection } from "@/api/elections";

interface Vote {
  selected: string | null;
}

export default Vue.extend({
  data: function() {
    return {
      election: null as ApiElection | null,
      votes: [] as Array<Vote>
    };
  },
  created: function() {
    const electionId = this.$router.currentRoute.params.electionId;
    this.$http.get(`/api/elections/elections/${electionId}/`).then(response => {
      this.election = response.data;
      this.votes = response.data.questions.map(() => ({ selected: null }));
    });
  },
  methods: {
    voteInElection: function() {
      const results = this.votes.map(vote => {
        console.log(vote);
        if (vote.selected === null) {
          console.error("Vote is null");
          return Promise.reject("Vote is null");
        }

        const [question, answer] = vote.selected.split(".");

        return this.$http.post("/api/elections/votes/", { answer });
      });
      Promise.all(results).then(() => {
        this.$router.push("/");
      }, console.error);
    }
  }
});
</script>
