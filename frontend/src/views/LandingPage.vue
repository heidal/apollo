<style lang="scss" scoped>
.landing-page {
  padding-top: 2em;
}

.description {
  padding-top: 4em;
  width: 60%;
  float: left;
  font-size: 1.5em;
  text-align: center;
  background-color: white;
}

.elections-container {
  padding: 3em 3em 3em 3em;
  float: right;
}
</style>

<template>
  <div class="landing-page">
    <b-jumbotron class="description">
      <template v-slot:header>Votifica</template>
      <template v-slot:lead>
        Lorem ipsum secure voting service for dolor sit amet
      </template>

      <hr class="my-4" />

      <b-button variant="outline-primary" size="lg" @click="goToCreateElection"
        >Create your own election!</b-button
      >
      <p>or</p>
      <b-button variant="outline-primary">Learn more</b-button>
    </b-jumbotron>
    <div class="elections-container">
      See what what other users are voting for:
      <ElectionsList
        class="elections-list"
        :show-pagination="false"
        :verbose="false"
        :page-size="3"
      />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ElectionsList from "@/components/ElectionsList.vue";

export default {
  name: "Home",
  components: {
    ElectionsList
  },
  methods: {
    goToCreateElection: function() {
      this.$router.push("/create-election");
    }
  }
};
</script>
