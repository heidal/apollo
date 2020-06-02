<style lang="scss" scoped>
.election-container {
  display: flex;
  flex-direction: column;
  padding: 0.2em;
}

.bulletin-board-entry {
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

.bulletin-board {
  max-width: 60rem;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5rem;
}
</style>

<template>
  <div class="overflow-auto bulletin-board">
    <b-pagination
      v-if="showPagination"
      v-model="currentPage"
      :total-rows="rows"
      :per-page="pageSize"
      aria-controls="bulletin-board"
    ></b-pagination>
    <b-list-group id="bulletin-board">
      <b-list-group-item
        v-for="entry in value"
        :key="entry.id"
        class="flex-column align-items-start"
      >
        <div class="d-flex w-100 justify-content-between">
          <p>
            Pseudonym: <code>{{ entry.pseudonym }}</code>
          </p>
          <small>{{ entry.createdAt }}</small>
        </div>
        <div class="d-flex w-100 justify-content-between">
          <pre><code>{{ entry.message }}</code></pre>
          <small>Question #{{ entry.questionId }}</small>
        </div>
      </b-list-group-item>
    </b-list-group>
    <b-pagination
      v-if="showPagination"
      v-model="currentPage"
      :total-rows="rows"
      :per-page="pageSize"
      aria-controls="bulletin-board"
    ></b-pagination>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export interface BulletinBoardEntry {
  pseudonym: string;
  createdAt: Date;
  message: string;
  question: number;
}

export default Vue.extend({
  props: {
    pageSize: {
      type: Number,
      default: 10,
      validator: function(value) {
        return value >= 0;
      }
    },
    showPagination: {
      type: Boolean,
      default: true
    },
    verbose: {
      type: Boolean,
      default: true
    },
    value: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      currentPage: 1
    };
  },
  computed: {
    rows(): number {
      return this.value.length;
    }
  }
});
</script>
