<style lang="scss" scoped>
.election-container {
  display: flex;
  flex-direction: column;
  padding: 0.2em;
}

.election-entry {
  margin: 0.2em;
  padding: 1em;
  background-color: lighten(lightblue, 15%);
  display: flex;
  flex-direction: column;
  h1 {
    text-align: left;
    margin-bottom: -0.3em;
    margin-top: 0em;
    font-size: 1.5em;
  }

  .description {
    text-align: left;
    font-size: 0.8em;
  }

  .questions-count {
    margin-top: 0;
    text-align: right;
  }
}
</style>

<template>
  <div class="election-container">
    <div class="election-entry" v-for="election in getElections()" :key="election.id">
      <span class="election-title">
        <h1><router-link :to="'/election-detail/' + election.id">{{ election.title }}</router-link></h1>
        <p class="description">{{ election.description }}</p>
      </span>
      <p class="questions-count">{{ election.questionsCount }} questions to answer</p>
    </div>
  </div>
</template>
<script lang="ts">
import Vue from "vue";

interface ElectionPreview {
  id: number;
  title: string;
  description: string;
  questionsCount: number;
}

interface APIElection {
  id: number;
  title: string;
  description: string;
  questions: Array<any>;
}

// TODO separate the view from the logic
export default Vue.extend({
  props: {
    pageSize: {
      type: Number,
      default: 10,
      validator: function(value) {
        return value >= 0;
      }
    }
  },
  data: function() {
    return {
      elections: [] as Array<ElectionPreview>
    };
  },
  created: function() {
    this.$http.get("/api/elections/elections/").then(response => {
      this.elections = response.data.results.map(
        (election: APIElection): ElectionPreview => {
          return {
            id: election.id,
            title: election.title,
            description: election.description,
            questionsCount: election.questions.length
          };
        }
      );
    }, console.error);
  },
  methods: {
    getElections: function() {
      return this.elections.slice(0, this.pageSize);
    }
  }
});
</script>
