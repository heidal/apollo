<style lang="scss" scoped>
    table {
        margin: 0 auto;
        border-collapse: collapse;
    }

    td, th {
        text-align: left;
        padding: 8px;
        border-bottom: 1px solid #dddddd;
    }

    tr:hover {
        background-color: #41b883;
    }
</style>
<template>
    <div v-if="election !== null">
        <h1>{{ election.title }}</h1>
        <p>{{ election.description }}</p>
        <div v-for="(question, i) in election.questions" :key="i">
            <p>Question #{{ i + 1 }}</p>
            <h3>{{ question.question }}</h3>
            <table style="margin: 0 auto">
                <tr>
                    <th>Answer</th>
                    <th>Votes</th>
                </tr>
                <tr v-for="(answer, ai) in question.answers" :key="ai">
                    <td>{{ answer.text }}</td>
                    <td>{{ answer.votes }}</td>
                </tr>
            </table>
        </div>
    </div>
</template>
<script lang="ts">
    import Vue from "vue";
    import {ApiElection, ApiElectionSummary} from "@/api/elections";

    export default Vue.extend({
        data: function() {
            return {
                election: null as ApiElectionSummary | null
            };
        },
        created: function() {
            const electionId = this.$router.currentRoute.params.electionId;
            this.$http.get(`/api/elections/elections/${electionId}/summary`).then(response => {
                this.election = response.data;
            });
        },
    });
</script>
