<template>
  <ElectionsList v-bind:pageSize="20" />
</template>
<script lang="ts">
import Vue from "vue";

import ElectionsList from "@/components/ElectionsList.vue";

export default Vue.extend({
  components: {
    ElectionsList,
  },
});
</script>
