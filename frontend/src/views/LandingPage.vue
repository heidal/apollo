<style lang="scss" scoped>
.landing-page {
  padding-top: 2em;
}

.description {
  padding-top: 4em;
  width: 60%;
  float: left;
  font-size: 1.5em;
}

.elections-container {
  padding: 3em 3em 3em 3em;
  float: right;
}
</style>

<template>
  <div class="landing-page">
    <div class="description">
      <h1>What is Apollo Voting?</h1>
      <p>Lorem ipsum secure voting service for dolor sit amet.</p>
      <button class="new-election-button" v-on:click="goToCreateElection">Create your own election!</button>
      <p>or</p>
      <button>Learn more</button>
    </div>
    <div class="elections-container">
      See what what other users are voting for:
      <ElectionsList class="elections-list" v-bind:pageSize="3" />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ElectionsList from "@/components/ElectionsList.vue";
import { ElGamal, KeyGenerator, Test } from "apollo-crypto";

export default {
  name: "Home",
  components: {
    ElectionsList
  },
  methods: {
    goToCreateElection: function() {
      this.$router.push("/create-election");
    }
  },
  mounted() {
    const keyGenerator = KeyGenerator.new();
    const elGamal = ElGamal.new();
    const keyPair = keyGenerator.generate();
    const test = Test.new();
    console.log(test.field2);
    console.log(keyPair.secret_key());
    console.log(keyPair.public_key());
  }
};
</script>
