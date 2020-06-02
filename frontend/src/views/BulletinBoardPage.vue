<style>
.bulletin-board {
  max-width: 60rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5rem;
}
</style>

<template>
  <div class="bulletin-board">
    <h1>
      Bulletin board for
      <b-button size="lg" variant="info" :to="`/election-detail/${electionId}`"
        >#{{ electionId }}</b-button
      >
    </h1>
    <BulletinBoard
      :value="bulletinBoard"
      :show-pagination="true"
      :page-size="10"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import BulletinBoard, {
  BulletinBoardEntry
} from "@/components/BulletinBoard.vue";

interface ApiBulletinBoardEntry {
  pseudonym: string;
  message: string;
  created_at: Date;
  question: number;
}

export default Vue.extend({
  components: {
    BulletinBoard
  },
  data() {
    return {
      bulletinBoard: [] as Array<BulletinBoardEntry>,
      electionId: 0
    };
  },
  created() {
    this.electionId = Number.parseInt(this.$route.params.electionId);
    this.$http
      .get(`/api/elections/elections/${this.electionId}/bulletin-board/`)
      .then(response => {
        this.bulletinBoard = response.data.map(
          (entry: ApiBulletinBoardEntry) => ({
            pseudonym: entry.pseudonym,
            message: entry.message,
            createdAt: entry.created_at,
            questionId: entry.question
          })
        );
      });
  }
});
</script>
