<template>
  <div>
    <div v-if="isCreatingElection()">
      <form @submit.prevent="createElection()">
        <input type="text" placeholder="Type the title of the election" v-model="election.title" />
        <input type="text" placeholder="Add a description" v-model="election.description" />
        <button type="submit" class="submit">Submit</button>
      </form>
    </div>
    <div v-else-if="isAddingQuestions()">
      <form @submit.prevent="submitQuestions()">
        <div v-for="(e, i) in election.questions.length" :key="i">
          <p>Question #{{ i + 1 }}</p>
          <input
            type="text"
            placeholder="Title of the question"
            v-model="election.questions[i].question"
          />
          <div v-for="(ae, ai) in election.questions[i].answers.length" :key="ai">
            <p>Answer #{{ i + 1 }}.{{ ai + 1 }}</p>
            <input
              type="text"
              placeholder="Title of the answer"
              v-model="election.questions[i].answers[ai].text"
            />
            <button
              v-if="ai === election.questions[i].answers.length - 1"
              v-on:click="addAnotherAnswer(i)"
            >Add another answer</button>
          </div>

          <button
            v-if="i === election.questions.length - 1"
            v-on:click="addAnotherQuestion()"
          >Add another question</button>
        </div>
        <button type="submit" class="submit">Submit</button>
      </form>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from "vue";

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
        .post("/api/elections/elections/", this.election, {
          headers: {
            "X-CSRFToken": this.$cookies.get("csrftoken")
          }
        })
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
      this.election.questions.map(question =>
        this.$http
          .post(
            "/api/elections/questions/",
            { question: question.question, election: this.election.id },
            {
              headers: { "X-CSRFToken": this.$cookies.get("csrftoken") }
            }
          )
          .then(response => {
            const questionId = response.data.id;
            question.answers.map(answer =>
              this.$http.post(
                "/api/elections/answers/",
                { text: answer.text, question: questionId },
                {
                  headers: { "X-CSRFToken": this.$cookies.get("csrftoken") }
                }
              )
            );
          })
      );
    }
  },
});
</script>
