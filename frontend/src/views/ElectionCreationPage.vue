<style lang="scss" scoped>
.questions-submit {
  position: -webkit-sticky; /* Safari */
  position: fixed;
  bottom: 100px;
  right: 100px;

  width: 15em;
  padding: 1em;
  opacity: 1;
  transition: visibility 0s opacity 0.5s linear;
  visibility: visible;
}

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
            disabled
            :active="isAddingQuestions()"
            @click="goToQuestions"
            >Questions</b-nav-item
          >
        </b-nav>
      </template>
      <b-card-body>
        <b-form @submit.prevent="goToQuestions()" v-if="isCreatingElection()">
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
          <b-button type="submit" variant="primary" style="float: right;"
            >Go to questions</b-button
          >
        </b-form>

        <b-form
          @submit.prevent="createElection()"
          v-else-if="isAddingQuestions()"
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
                    variant="outline-primary"
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
              variant="primary"
              v-if="i === election.questions.length - 1"
              v-on:click="addAnotherQuestion()"
              >Add another question</b-button
            >
          </b-form-group>
          <b-button
            type="submit"
            class="questions-submit"
            variant="primary"
            size="lg"
            v-bind:class="questionsSubmitButton()"
            >Create election!</b-button
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

export default Vue.extend({
  data: function () {
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
            visible: true,
          },
        ] as Array<Question>,
      },
      flow: Flow.Election,
    };
  },
  created: function () {
    this.$store.getters.isAuthenticated;
  },
  methods: {
    createElection() {
      this.$http
        .post("/api/elections/elections/", this.election)
        .then((response) => {
          this.election.id = response.data.id;
          this.submitQuestions();
        }, console.error);
    },
    isCreatingElection(): boolean {
      return this.flow === Flow.Election;
    },
    isAddingQuestions(): boolean {
      return this.flow === Flow.Questions;
    },
    addAnotherQuestion() {
      this.election.questions.push({
        id: null,
        question: null,
        answers: [{ text: null }],
        visible: true,
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
        text: null,
      });
    },
    submitQuestions() {
      const questionResponses = this.election.questions.map((question) =>
        this.$http.post("/api/elections/questions/", {
          question: question.question,
          election: this.election.id,
        })
      );
      Promise.all(questionResponses).then((createdQuestions) => {
        const answerResponses = createdQuestions
          .flatMap((question, i) =>
            this.election.questions[i].answers.map((answer) => ({
              text: answer.text,
              question: question.data.id,
            }))
          )
          .map((answerData) =>
            this.$http.post("/api/elections/answers/", answerData)
          );

        Promise.all(answerResponses).then(() => {
          this.$router.push(`/election-detail/${this.election.id}`);
        }, console.error);
      });
    },
    questionsSubmitButton() {
      return {
        hidden:
          this.election.questions.length === 0 ||
          this.election.questions[0].question === null ||
          this.election.questions[0].question.length === 0,
      };
    },
    goToQuestions() {
      this.flow = Flow.Questions;
    },
    goToGeneralInfo() {
      this.flow = Flow.Election;
    },
  },
});
</script>
