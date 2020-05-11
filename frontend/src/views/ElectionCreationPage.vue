<style lang="scss" scoped>
button {
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  width: 100%;
  padding: 3%;
  background: #43d1af;
  border-bottom: 2px solid #30c29e;
  border-top-style: none;
  border-right-style: none;
  border-left-style: none;
  color: #fff;
  border-radius: 1em;
}
button:hover {
  background: #2ebc99;
  cursor: pointer;
}

.election-form {
  font: 95% Arial, Helvetica, sans-serif;
  max-width: 600px;
  margin: 10px auto;
  padding: 16px;
  background: #f7f7f7;

  h1 {
    padding: 20px 0;
    font-size: 140%;
    font-weight: 300;
    text-align: left;
    width: 100%;
  }

  p {
    text-align: left;
    width: 100%;
    font-weight: 200;
    padding-left: 2em;
  }

  input[type="text"],
  textarea {
    -webkit-transition: all 0.3s ease-in-out;
    -moz-transition: all 0.3s ease-in-out;
    -ms-transition: all 0.3s ease-in-out;
    -o-transition: all 0.3s ease-in-out;
    outline: none;
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    width: 100%;
    background: #fff;
    margin-bottom: 4%;
    border: 1px solid #ccc;
    padding: 3%;
    color: #555;
    font: 95% Arial, Helvetica, sans-serif;

    border-radius: 10px;
  }

  input[type="text"]:focus,
  textarea:focus {
    box-shadow: 0 0 5px #43d1af;
    padding: 3%;
    border: 1px solid #43d1af;
  }

  .add-answer-wrapper {
    height: 2em;
    display: flex;
    width: 50%;
    float: right;

    p {
      font-size: 1em;
      margin-right: 1em;
      display: flex;
      justify-content: right;
      align-items: center;
    }

    .add-answer-button {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 1em;
      height: 1em;
      font-size: 200%;
    }
  }

  .add-question-button {
    margin-top: 10em;
  }
}

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

.hidden {
  visibility: hidden;
  opacity: 0;
}
</style>
<template>
  <div>
    <div class="election-form" v-if="isCreatingElection()">
      <form @submit.prevent="createElection()">
        <input type="text" placeholder="Type the title of the election" v-model="election.title" />
        <textarea type="text" placeholder="Add a description" v-model="election.description" />
        <button type="submit" class="submit">Submit</button>
      </form>
    </div>

    <form @submit.prevent="submitQuestions()" v-else-if="isAddingQuestions()">
      <div class="election-form">
        <div class="question-form" v-for="(e, i) in election.questions.length" :key="i">
          <h1>Question #{{ i + 1 }}</h1>
          <input
            type="text"
            placeholder="Type the question"
            v-model="election.questions[i].question"
          />
          <div v-for="(ae, ai) in election.questions[i].answers.length" :key="ai">
            <p>Answer #{{ i + 1 }}.{{ ai + 1 }}</p>
            <input
              class="answer-text"
              type="text"
              placeholder="Type the answer"
              v-model="election.questions[i].answers[ai].text"
            />
            <div class="add-answer-wrapper" v-if="ai === election.questions[i].answers.length - 1">
              <p>Add another answer</p>
              <button v-on:click="addAnotherAnswer(i)" class="add-answer-button">+</button>
            </div>
          </div>

          <button
            class="add-question-button"
            v-if="i === election.questions.length - 1"
            v-on:click="addAnotherQuestion()"
          >Add another question</button>
        </div>
      </div>
      <button
        type="submit"
        class="questions-submit"
        v-bind:class="questionsSubmitButton()"
      >Submit the questions!</button>
    </form>
  </div>
</template>
<script lang="ts">
import Vue from "vue";
import {ElGamal, KeyGenerator} from "apollo-crypto";

enum Flow {
  Election,
  Questions
}

interface Answer {
  text: string | null;
}

interface Question {
  id: number | null;
  question: string | null;
  answers: Array<Answer>;
}

export default Vue.extend({
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
            answers: [{ text: null }]
          }
        ] as Array<Question>
      },
      flow: Flow.Election
    };
  },
  created: function() {
    this.$store.getters.isAuthenticated;
  },
  methods: {
    createElection: function() {
      this.$http
        .post("/api/elections/elections/", this.election)
        .then(response => {
          this.election.id = response.data.id;
          this.flow = Flow.Questions;
        }, console.error);
    },
    isCreatingElection: function(): boolean {
      return this.flow === Flow.Election;
    },
    isAddingQuestions: function(): boolean {
      return this.flow === Flow.Questions;
    },
    addAnotherQuestion: function() {
      this.election.questions.push({
        id: null,
        question: null,
        answers: [{ text: null }]
      });
    },
    addAnotherAnswer: function(questionId: number) {
      this.election.questions[questionId].answers.push({
        text: null
      });
    },
    submitQuestions: function() {
      const questionResponses = this.election.questions.map(question =>
        this.$http.post("/api/elections/questions/", {
          question: question.question,
          election: this.election.id
        })
      );
      Promise.all(questionResponses).then(createdQuestions => {
        const answerResponses = createdQuestions
          .flatMap((question, i) =>
            this.election.questions[i].answers.map(answer => ({
              text: answer.text,
              question: question.data.id
            }))
          )
          .map(answerData =>
            this.$http.post("/api/elections/answers/", answerData)
          );

        Promise.all(answerResponses).then(() => {
          this.$router.push("/");
        }, console.error);
      });
    },
    questionsSubmitButton: function() {
      return {
        hidden:
          this.election.questions[0].question === null ||
          this.election.questions[0].question.length === 0
      };
    }
  }
});
</script>
