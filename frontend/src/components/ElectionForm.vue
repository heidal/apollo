<style lang="scss" scoped>
.election-form {
  max-width: 40em;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5em;
}

.hidden {
  visibility: hidden;
  opacity: 0;
}
</style>
<template>
  <div>
    <b-card class="election-form" header-tag="nav" title="Create election">
      <template v-slot:header>
        <b-nav card-header tabs>
          <b-nav-item :active="isCreatingElection()" @click="goToGeneralInfo"
            >General info</b-nav-item
          >
          <b-nav-item :active="isAddingQuestions()" @click="goToQuestions"
            >Questions</b-nav-item
          >
          <b-nav-item :active="isAddingVoters()" @click="goToVoters"
            >Voters</b-nav-item
          >
        </b-nav>
      </template>
      <b-card-body>
        <b-form
          v-if="isCreatingElection()"
          :validated="validated"
          @submit.prevent="goToQuestions()"
        >
          <b-form-group>
            <b-form-input
              v-model="election.title"
              required
              placeholder="Type the title of the election"
            ></b-form-input>
          </b-form-group>
          <b-form-group>
            <b-form-textarea
              v-model="election.description"
              required
              placeholder="Add a description"
            >
            </b-form-textarea>
          </b-form-group>
          <b-form-group label="Election visibility">
            <b-form-checkbox v-model="election.public" switch>
              {{ election.public ? "Public" : "Private" }}
            </b-form-checkbox>
          </b-form-group>
          <b-button type="submit" variant="primary" style="float: right;"
            >Go to questions</b-button
          >
        </b-form>

        <b-form
          v-else-if="isAddingQuestions()"
          :validated="validated"
          @submit.prevent="goToVoters()"
        >
          <b-form-group
            v-for="(e, i) in election.questions.length"
            :key="i"
            :label="`Question #${i + 1}`"
          >
            <div style="display: flex;">
              <b-button variant="outline" @click="() => toggleCollapse(i)">
                <b-icon-chevron-down
                  v-if="election.questions[i].visible"
                ></b-icon-chevron-down>
                <b-icon-chevron-right v-else></b-icon-chevron-right>
              </b-button>
              <b-button
                size="sm"
                :variant="
                  election.questions.length <= 1 ? 'outline-dark' : 'danger'
                "
                :disabled="election.questions.length <= 1"
                @click="() => deleteQuestion(i)"
                ><b-icon-trash></b-icon-trash
              ></b-button>
              <b-form-input
                v-model="election.questions[i].question"
                required
                type="text"
                placeholder="Type the question"
              ></b-form-input>
            </div>
            <b-collapse
              :id="`collapse-${i}`"
              v-model="election.questions[i].visible"
            >
              <b-form-group
                v-for="(ae, ai) in election.questions[i].answers.length"
                :key="ai"
                :label="`Answer #${i + 1}.${ai + 1}`"
                :label-for="`answer-${i + 1}-${ai + 1}`"
                style="margin-top: 2em; margin-left: 3em;"
              >
                <div style="display: flex;">
                  <b-button
                    size="sm"
                    :variant="
                      election.questions[i].answers.length <= 1
                        ? 'outline-dark'
                        : 'danger'
                    "
                    :disabled="election.questions[i].answers.length <= 1"
                    @click="() => deleteAnswer(i, ai)"
                    ><b-icon-trash></b-icon-trash
                  ></b-button>
                  <b-form-input
                    :id="`answer-${i + 1}-${ai + 1}`"
                    v-model="election.questions[i].answers[ai].text"
                    type="text"
                    required
                    placeholder="Type the answer"
                  ></b-form-input>
                </div>
                <div
                  v-if="ai === election.questions[i].answers.length - 1"
                  class="add-answer-wrapper"
                >
                  <b-button
                    variant="outline-info"
                    size="sm"
                    style="float: right;"
                    @click="addAnotherAnswer(i)"
                    ><span class="glyphicon glyphicon-plus"
                      ><b-icon-plus></b-icon-plus>Add another answer</span
                    ></b-button
                  >
                </div>
              </b-form-group>
            </b-collapse>
            <b-button
              v-if="i === election.questions.length - 1"
              style="margin-top: 2em;"
              variant="info"
              @click="addAnotherQuestion()"
              >Add another question</b-button
            >
          </b-form-group>
          <b-button type="submit" variant="primary" style="float: right;"
            >Go to voters</b-button
          >
        </b-form>
        <b-form v-else-if="isAddingVoters()" @submit.prevent="submitElection()">
          <b-form-group label="Specify voters emails">
            <b-form-textarea
              v-model="election.voters"
              placeholder="example@votifica.com"
              rows="6"
            >
            </b-form-textarea>
            <b-form-invalid-feedback :state="errors.voters === null">
              {{ errors.voters }}
            </b-form-invalid-feedback>
          </b-form-group>
          <b-button
            type="submit"
            :variant="election.voters.length ? 'primary' : 'outline-dark'"
            style="float: right;"
            :disabled="election.voters.length === 0"
            >Submit election</b-button
          >
        </b-form>
      </b-card-body>
    </b-card>
  </div>
</template>
<script lang="ts">
/* eslint-disable @typescript-eslint/camelcase */

import Vue from "vue";

export enum Flow {
  Election,
  Questions,
  Voters
}

export interface Answer {
  text: string | null;
}

export interface Question {
  id: number | null;
  question: string | null;
  answers: Array<Answer>;
  visible: boolean;
}

export interface AuthorizationRule {
  id: number | null;
  type: "EXACT";
  value: string | null;
}

export interface ElectionFormData {
  id: number | null;
  title: string;
  description: string;
  questions: Array<Question>;
  authorization_rules: Array<AuthorizationRule>;
  visibility: "PUBLIC" | "PRIVATE";
}

export default Vue.component("election-form", {
  props: {
    election: {
      type: Object,
      default: () => ({
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
      })
    },
    errors: {
      type: Object,
      default: () => ({
        voters: null
      })
    },
    step: {
      type: Number,
      default: Flow.Election
    },
    validated: {
      type: Boolean,
      default: false
    }
  },
  data: function() {
    return {
      ruleTypes: ["EXACT"]
    };
  },
  methods: {
    submitElection() {
      const [success, voters] = this.validateVoters();
      if (!success) {
        this.errors.voters = voters;
      } else {
        const electionForm = this.buildElectionForm(voters);
        this.$emit("electionSubmitted", electionForm);
      }
    },
    isCreatingElection(): boolean {
      return this.step === Flow.Election;
    },
    isAddingQuestions(): boolean {
      return this.step === Flow.Questions;
    },
    isAddingVoters(): boolean {
      return this.step === Flow.Voters;
    },
    addAnotherQuestion() {
      this.election.questions.push({
        id: null,
        question: null,
        answers: [{ text: null }],
        visible: true
      });
    },
    deleteQuestion(questionId: number) {
      if (this.election.questions.length <= 1) {
        return;
      } else {
        this.election.questions.splice(questionId, 1);
      }
    },
    deleteAnswer(questionId: number, answerId: number) {
      const answers = this.election.questions[questionId].answers;
      if (answers.length <= 1) {
        return;
      } else {
        answers.splice(answerId, 1);
      }
    },
    toggleCollapse(questionId: number) {
      this.election.questions[questionId].visible = !this.election.questions[
        questionId
      ].visible;
    },
    addAnotherAnswer(questionId: number) {
      this.election.questions[questionId].answers.push({
        text: null
      });
    },
    buildElectionForm(voters: Array<AuthorizationRule>): ElectionFormData {
      return {
        id: this.election.id,
        title: this.election.title,
        description: this.election.description,
        authorization_rules: voters,
        questions: this.election.questions.map((q: Question) => ({
          id: q.id,
          question: q.question,
          answers: q.answers
        })),
        visibility: this.election.public ? "PUBLIC" : "PRIVATE"
      };
    },
    questionsSubmitButton() {
      return {
        hidden:
          this.election.questions.length === 0 ||
          this.election.questions[0].question === null ||
          this.election.questions[0].question.length === 0
      };
    },
    validateVoters() {
      const voters = this.election.voters
        .split("\n")
        .map((line: string) => line.trim())
        .filter((line: string) => line.length > 0);
      for (const voter of voters) {
        if (!this.validateEmail(voter)) {
          return [false, voter + " is not an email address"];
        }
      }
      return [
        true,
        voters.map((voter: string) => ({ type: "EXACT", value: voter }))
      ];
    },
    goToGeneralInfo() {
      this.$emit("goToGeneralInfo");
    },
    goToQuestions() {
      this.$emit("goToQuestions");
    },
    goToVoters() {
      this.$emit("goToVoters");
    },
    validateEmail(value: string): boolean {
      return /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(
        value
      );
    }
  }
});
</script>
