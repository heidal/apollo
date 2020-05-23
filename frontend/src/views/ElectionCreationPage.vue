<template>
  <div>
    <election-form
      :voters="election.voters"
      :validated="validated"
      :election="election"
      :step="step"
      :errors="errors"
      @electionSubmitted="onElectionSubmitted"
      @goToGeneralInfo="goToGeneralInfo"
      @goToQuestions="goToQuestions"
      @goToVoters="goToVoters"
    ></election-form>
  </div>
</template>
<script lang="ts">
/* eslint-disable @typescript-eslint/camelcase */

import Vue from "vue";
import ElectionForm from "@/components/ElectionForm.vue";
import {
  Flow,
  ElectionFormData,
  Question
} from "@/components/ElectionForm.vue";

export default Vue.extend({
  components: {
    ElectionForm
  },
  data: function() {
    return {
      election: {
        id: null,
        title: null,
        description: null,
        questions: [
          {
            id: null,
            question: null,
            answers: [{ text: null }],
            visible: true
          }
        ] as Array<Question>,
        voters: "",
        public: false
      },
      errors: {
        voters: null as string | null
      },
      validated: false,
      ruleTypes: ["EXACT"],
      step: Flow.Election
    };
  },
  methods: {
    onElectionSubmitted(election: ElectionFormData) {
      const requestMethod = election.id ? this.$http.patch : this.$http.post;
      requestMethod("/api/elections/elections/", election).then(
        response => {
          this.election = response.data;
          this.$router.push(`/election-detail/${this.election.id}`);
        },
        error => {
          const errors = error.response.data;
          this.validated = true;
          if (errors.description || errors.title) {
            this.goToGeneralInfo();
          } else if (errors.questions) {
            this.goToQuestions();
          }
          if (errors["authorization_rules"] !== undefined) {
            this.errors.voters =
              errors["authorization_rules"][0] + " is not an email address";
          } else {
            this.errors.voters = null;
          }
        }
      );
    },
    getErrorString(errorKey: string) {
      const errorMap = {
        INVALID_REGEX: "Invalid regex"
      } as { [key: string]: string };
      return errorMap[errorKey] || "Unknown error";
    },
    goToGeneralInfo() {
      this.step = Flow.Election;
    },
    goToQuestions() {
      this.step = Flow.Questions;
    },
    goToVoters() {
      this.step = Flow.Voters;
    }
  }
});
</script>
