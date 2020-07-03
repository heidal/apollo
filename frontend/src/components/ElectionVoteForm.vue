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

      <b-form v-if="isOnVoteForm()" @submit.prevent="goToConfirmForm($event)">
        <b-form-group
          v-for="(question, i) in election.questions"
          :key="i"
          :label="`Question #${i + 1}`"
        >
          <h3>{{ question.question }}</h3>
          <b-form-radio
            v-for="(answer, ai) in question.answers"
            :key="ai"
            v-model="votes[i]"
            required
            :name="`answer.${i}`"
            :value="{ question: question.id, answer: answer.id }"
            >{{ answer.text }}</b-form-radio
          >
        </b-form-group>
        <b-button
          type="submit"
          class="submit"
          variant="warning"
          style="float: right;"
          >Go to confirm page</b-button
        >
        <b-form-invalid-feedback :state="voteError === null">
          {{ voteError }}
        </b-form-invalid-feedback>
      </b-form>

      <b-form
        v-if="isOnConfirmForm()"
        @submit.prevent="voteInElection()">
        <h2>
          Your votes:
        </h2>

        <b-form-group
          v-for="(question, i) in election.questions"
          :key="i"
          :label="`Question #${i + 1}`"
        >
          <h3>{{ question.question }}</h3>
          <ul>
            <li>{{ question.answers.find(answer => answer.id === votes[i].answer).text }}</li>
          </ul>
        </b-form-group>

        <b-button
          type="submit"
          class="submit"
          variant="warning"
          style="float: right;"
        >
          Send votes
        </b-button>
        <b-button
          variant="outline-secondary"
          style="float: right;"
          @click="goToVoteForm($event)"
        >
          Go back
        </b-button>
        <b-form-invalid-feedback :state="voteError === null">
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
  question: number | null,
  answer: number | null
}

export enum Flow {
  Vote,
  Confirm
}

export default Vue.component("vote-form", {
  props: {
    election: ApiElection,
    voteError: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      votes: [] as Array<Vote>,
      step: Flow.Vote as Flow
    };
  },
  created() {
    this.votes = this.election.questions.map(() => ({ question: null, answer: null } as Vote));
  },
  methods: {
    voteInElection() {
      this.$emit("votesSubmitted", this.votes);
    },
    goToVoteForm(event) {
      this.step = Flow.Vote;
      event.preventDefault();
    },
    goToConfirmForm(event) {
      event.preventDefault();
      this.step = Flow.Confirm;
    },
    isOnVoteForm(): boolean {
      return this.step === Flow.Vote;
    },
    isOnConfirmForm(): boolean {
      return this.step === Flow.Confirm;
    }
  }
});
</script>
