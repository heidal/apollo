<style scoped lang="scss">
.vote-form {
  max-width: 30rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5rem;
}
</style>

<template>
  <b-card class="vote-form" :title="election.title">
    <b-card-body>
      <b-card-text>
        <p>{{ election.description }}</p>
        <hr class="my-4" />
      </b-card-text>
      <b-form v-if="election !== null" @submit.prevent="voteInElection()">
        <b-form-group
          :label="`Question #${i + 1}`"
          v-for="(question, i) in election.questions"
          :key="i"
        >
          <h3>{{ question.question }}</h3>
          <b-form-radio
            required
            v-for="(answer, ai) in question.answers"
            :key="ai"
            :name="`answer.${i}`"
            :value="`${question.id}.${answer.id}`"
            v-model="votes[i].selected"
            >{{ answer.text }}</b-form-radio
          >
        </b-form-group>
        <b-button
          type="submit"
          class="submit"
          variant="warning"
          style="float: right;"
          >Send votes</b-button
        >
        <b-form-invalid-feedback
          :state="voteError === null"
        >
          {{ voteError }}
        </b-form-invalid-feedback>
      </b-form>
    </b-card-body>
  </b-card>
</template>
<script lang="ts">
import Vue from "vue";

import { ApiElection } from "@/api/elections";

export interface Vote {
  selected: string | null;
}

export default Vue.component("vote-form", {
  props: {
    election: ApiElection,
    voteError: null as string | null,
  },
  data() {
    return {
      votes: [] as Array<Vote>,
    };
  },
  created() {
    this.votes = this.election.questions.map(() => ({ selected: null }));
  },
  methods: {
    voteInElection() {
      this.$emit("votesSubmitted", this.votes);
    },
  },
});
</script>
