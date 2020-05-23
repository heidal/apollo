<template>
  <election-detail v-if="election" :election="election"></election-detail>
</template>
<script lang="ts">
import Vue from "vue";

import ElectionDetail from "@/components/ElectionDetail.vue";
import { ApiElection } from "@/api/elections";

export default Vue.extend({
  components: {
    ElectionDetail
  },
  data: function() {
    return {
      election: null as ApiElection | null
    };
  },
  created: function() {
    const electionId = this.$router.currentRoute.params.electionId;
    this.$http.get(`/api/elections/elections/${electionId}`).then(response => {
      this.election = response.data;
    });
  }
});
</script>
