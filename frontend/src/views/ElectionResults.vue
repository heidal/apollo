<template>
    <div>Test</div>
</template>
<script lang="ts">
    import Vue from "vue";

    export default Vue.extend({
        data: function() {
            return {
                election: null
            };
        },
        created: function() {
            const electionId = this.$router.currentRoute.params.electionId;
            this.$http.get(`/api/elections/elections/${electionId}`).then(response => {
                this.election = response.data;
            });
        },
    });
</script>
