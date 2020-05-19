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
          <b-nav-item
            :active="isAddingQuestions()"
            @click="goToQuestions"
            >Questions</b-nav-item
          >
          <b-nav-item
            :active="isAddingVoters()"
            @click="goToVoters"
          >Voters</b-nav-item>
        </b-nav>
      </template>
      <b-card-body>
        <b-form @submit.prevent="goToQuestions()" v-if="isCreatingElection()" :validated="formsValidated">
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
          <b-button type="submit" variant="primary" style="float: right;" ref="generalInfoForm"
            >Go to questions</b-button
          >
        </b-form>

        <b-form
          @submit.prevent="goToVoters()"
          v-else-if="isAddingQuestions()"
          :validated="formsValidated"
        >
          <b-form-group
            v-for="(e, i) in election.questions.length"
            :key="i"
            :label="`Question #${i + 1}`"
          >
            <div style="display: flex;">
              <b-button @click="() => toggleCollapse(i)" variant="outline">
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
                v-on:click="() => deleteQuestion(i)"
                :disabled="election.questions.length <= 1"
                ><b-icon-trash></b-icon-trash
              ></b-button>
              <b-form-input
                required
                type="text"
                placeholder="Type the question"
                v-model="election.questions[i].question"
              ></b-form-input>
            </div>
            <b-collapse
              v-model="election.questions[i].visible"
              :id="`collapse-${i}`"
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
                    v-on:click="() => deleteAnswer(i, ai)"
                    :disabled="election.questions[i].answers.length <= 1"
                    ><b-icon-trash></b-icon-trash
                  ></b-button>
                  <b-form-input
                    type="text"
                    required
                    placeholder="Type the answer"
                    v-model="election.questions[i].answers[ai].text"
                    :id="`answer-${i + 1}-${ai + 1}`"
                  ></b-form-input>
                </div>
                <div
                  class="add-answer-wrapper"
                  v-if="ai === election.questions[i].answers.length - 1"
                >
                  <b-button
                    v-on:click="addAnotherAnswer(i)"
                    variant="outline-info"
                    size="sm"
                    style="float: right;"
                    ><span class="glyphicon glyphicon-plus"
                      ><b-icon-plus></b-icon-plus>Add another answer</span
                    ></b-button
                  >
                </div>
              </b-form-group>
            </b-collapse>
            <b-button
              style="margin-top: 2em;"
              variant="info"
              v-if="i === election.questions.length - 1"
              v-on:click="addAnotherQuestion()"
              >Add another question</b-button
            >
          </b-form-group>
          <b-button
            type="submit"
            variant="primary"
            style="float: right;"
            ref="questionsForm"
            >Go to voters</b-button
          >
        </b-form>
        <b-form
          @submit.prevent="submitElection()"
          v-else-if="isAddingVoters()"
          :validated="formsValidated"
        >
          <b-form-group
            v-for="(e, i) in election.authorizationRules.length"
            :key="i"
            :label="`Rule #${i + 1}`"
          >
            <b-container class="pr-0">
              <b-row align-v="stretch" align-h="start" no-gutters>
                <b-col cols="1">
                  <b-button
                    :variant="
                      election.authorizationRules.length <= 1 ? 'outline-dark' : 'danger'
                    "
                    v-on:click="() => deleteRule(i)"
                    :disabled="election.authorizationRules.length <= 1"
                    ><b-icon-trash></b-icon-trash
                  ></b-button>
                </b-col>
                <b-col cols="3">
                  <b-form-select v-model="election.authorizationRules[i].type" :options="ruleTypes"></b-form-select>
                </b-col>
                <b-col>
                  <b-form-input
                    type="text"
                    required
                    placeholder="Type the rule"
                    v-model="election.authorizationRules[i].value"
                    :id="`rule-${i+1}`"
                  >
                  </b-form-input>
                </b-col>
              </b-row>
            </b-container>

            <div
              class="add-answer-wrapper"
              v-if="i === election.authorizationRules.length - 1"
            >
              <b-button
                v-on:click="addAnotherRule()"
                variant="outline-info"
                size="sm"
                style="float: right;"
                ><span class="glyphicon glyphicon-plus"
                  ><b-icon-plus></b-icon-plus>Add another rule</span
                ></b-button
              >
            </div>
          </b-form-group>
          <b-button
            type="submit"
            :variant="election.authorizationRules[0].value ? 'primary' : 'outline-dark'"
            style="float: right;"
            :disabled="!election.authorizationRules[0].value"
            >Submit election</b-button
          >
        </b-form>
      </b-card-body>
    </b-card>
  </div>
</template>
<script lang="ts">
import Vue from "vue";

enum Flow {
  Election,
  Questions,
  Voters,
}

interface Answer {
  text: string | null;
}

interface Question {
  id: number | null;
  question: string | null;
  answers: Array<Answer>;
  visible: boolean;
}

interface AuthorizationRule {
  id: number | null;
  type: "REGEX" | "EXACT";
  value: string | null;
}

export default Vue.extend({
  data: function () {
    return {
      formsValidated: false,
      ruleTypes: ["REGEX", "EXACT"],
      election: {
        id: null,
        title: null,
        description: null,
        questions: [
          {
            id: null,
            question: null,
            answers: [{ text: null }],
            visible: true,
          },
        ] as Array<Question>,
        authorizationRules: [
          {
            id: null,
            type: "EXACT",
            value: null,
          }
        ] as Array<AuthorizationRule>
      },
      flow: Flow.Election,
    };
  },
  methods: {
    submitElection() {
      const electionForm = this.buildElectionForm();
      const requestMethod = this.election.id ? this.$http.patch : this.$http.post;
      requestMethod("/api/elections/elections/", electionForm)
        .then((response) => {
          this.election = response.data;
          this.$router.push(`/election-detail/${this.election.id}`);
        }, error => {
          const errors = error.response.data;
          this.formsValidated = true;
          if (errors.description || error.title) {
            this.goToGeneralInfo();
          } else if (errors.questions) {
            this.goToQuestions();
          }
        });
    },
    isCreatingElection(): boolean {
      return this.flow === Flow.Election;
    },
    isAddingQuestions(): boolean {
      return this.flow === Flow.Questions;
    },
    isAddingVoters(): boolean {
      return this.flow === Flow.Voters;
    },
    addAnotherQuestion() {
      this.election.questions.push({
        id: null,
        question: null,
        answers: [{ text: null }],
        visible: true,
      });
    },
    addAnotherRule() {
      this.election.authorizationRules.push({
        id: null,
        type: "EXACT",
        value: null,
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
    deleteRule(ruleId: number) {
      const rules = this.election.authorizationRules;
      if (rules.length <= 1) {
        return;
      } else {
        rules.splice(ruleId, 1);
      }
    },
    toggleCollapse(questionId: number) {
      this.election.questions[questionId].visible = !this.election.questions[
        questionId
      ].visible;
    },
    addAnotherAnswer(questionId: number) {
      this.election.questions[questionId].answers.push({
        text: null,
      });
    },
    buildElectionForm() {
      return {
        id: this.election.id,
        title: this.election.title,
        description: this.election.description,
        "authorization_rules": this.election.authorizationRules,
        questions: this.election.questions.map(q => ({
          id: q.id,
          question: q.question,
          answers: q.answers,
        }))
      };
    },
    questionsSubmitButton() {
      return {
        hidden:
          this.election.questions.length === 0 ||
          this.election.questions[0].question === null ||
          this.election.questions[0].question.length === 0,
      };
    },
    goToGeneralInfo() {
      this.flow = Flow.Election;
    },
    goToQuestions() {
      this.flow = Flow.Questions;
    },
    goToVoters() {
      this.flow = Flow.Voters;
    }
  },
});
</script>
