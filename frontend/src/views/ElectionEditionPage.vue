<template>
  <div>
    <election-form
      v-if="election.id !== null"
      :errors="errors"
      :validated="validated"
      :election="election"
      :step="step"
      @electionSubmitted="onElectionSubmitted"
      @goToGeneralInfo="goToGeneralInfo"
      @goToQuestions="goToQuestions"
      @goToVoters="goToVoters"
    ></election-form>
  </div>
</template>
<script lang="ts">
/* eslint-disable @typescript-eslint/camelcase */
// TODO use a mixin or something to reuse the common logic.

import Vue from "vue";
import ElectionForm from "@/components/ElectionForm.vue";
import {
  Flow,
  AuthorizationRuleError,
  AuthorizationRuleApiError,
  ElectionFormData,
  AuthorizationRule,
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
        authorizationRules: [
          {
            id: null,
            type: "EXACT",
            value: null
          }
        ] as Array<AuthorizationRule>
      },
      validated: false,
      ruleTypes: ["REGEX", "EXACT"],
      errors: {
        rules: [{ value: null }] as Array<AuthorizationRuleError>
      },
      step: Flow.Election
    };
  },
  created() {
    const electionId = this.$router.currentRoute.params.electionId;
    this.$http.get(`/api/elections/elections/${electionId}`).then(response => {
      this.election = response.data;
      this.election.authorizationRules = response.data["authorization_rules"];
      this.errors.rules = this.election.authorizationRules.map(() => ({
        value: null
      }));
    });
    console.log(electionId);
  },
  methods: {
    onElectionSubmitted(election: ElectionFormData) {
      this.$http
        .patch(`/api/elections/elections/${election.id}/`, election)
        .then(
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
              errors["authorization_rules"].forEach(
                (e: AuthorizationRuleApiError, i: number) => {
                  this.errors.rules[i].value = this.getErrorString(e.value[0]);
                }
              );
            } else {
              this.errors.rules = this.errors.rules.map(() => ({
                value: null
              }));
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
