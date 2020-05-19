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

.elections-list {
  max-width: 60rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5rem;
}
</style>

<template>
  <div class="overflow-auto elections-list">
    <b-pagination
      v-if="showPagination"
      v-model="currentPage"
      :total-rows="rows"
      :per-page="pageSize"
      aria-controls="elections-list"
    ></b-pagination>
    <b-list-group id="elections-list">
      <b-list-group-item
        v-for="election in getElections()"
        :key="election.id"
        :to="`/election-detail/${election.id}`"
        class="flex-column align-items-start"
      >
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">{{ election.title }}</h5>
          <small>{{ election.daysAgo }}</small>
        </div>

        <p class="mb-1">
          {{ election.description }}
        </p>
        <div class="d-flex w-100 align-items-center justify-content-between">
          <div class="d-flex w-100 align-items-center">
            <b-badge :variant="getVariant(election)" pill>{{
              election.status
            }}</b-badge>
            <b-badge variant="primary" pill
              >{{ election.questionsCount }} question{{
                election.questionsCount !== 1 ? "s" : ""
              }}</b-badge
            >
          </div>
          <small v-if="election.publicKey && verbose">{{
            election.publicKey
          }}</small>
        </div>
      </b-list-group-item>
    </b-list-group>
    <b-pagination
      v-if="showPagination"
      v-model="currentPage"
      :total-rows="rows"
      :per-page="pageSize"
      aria-controls="elections-list"
    ></b-pagination>
  </div>
</template>
<script lang="ts">
import Vue from "vue";
import { ApiElection } from "@/api/elections";

interface ElectionPreview {
  id: number;
  title: string;
  description: string;
  questionsCount: number;
  daysAgo: string;
  status: string;
  publicKey: string;
}

// TODO separate the view from the logic
export default Vue.extend({
  props: {
    pageSize: {
      type: Number,
      default: 10,
      validator: function (value) {
        return value >= 0;
      },
    },
    showPagination: {
      type: Boolean,
      default: true,
    },
    verbose: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      elections: [] as Array<ElectionPreview>,
      currentPage: 1,
    };
  },
  created() {
    this.$http.get("/api/elections/elections/").then((response) => {
      this.elections = response.data.results.map(
        (election: ApiElection): ElectionPreview => {
          const daysAgo = Math.floor(
            ((new Date()).valueOf() - Date.parse(election.created_at).valueOf()) /
              (1000 * 60 * 60 * 24)
          );
          return {
            id: election.id,
            title: election.title,
            description: election.description,
            questionsCount: election.questions.length,
            daysAgo: daysAgo > 0 ? `${daysAgo} days ago` : "today",
            status: election.state,
            publicKey: election.public_key,
          };
        }
      );
    });  // TODO no error handling
  },
  methods: {
    getElections(): Array<ElectionPreview> {
      return this.elections.slice(
        (this.currentPage - 1) * this.pageSize,
        this.currentPage * this.pageSize
      );
    },
    getVariant(election: ElectionPreview): string {
      const variants: {[key: string]: string} = {
        CREATED: "info",
        OPENED: "warning",
        CLOSED: "info",
      };
      return variants[election.status];
    },
  },
  computed: {
    rows(): number {
      return this.elections.length;
    },
  },
});
</script>
