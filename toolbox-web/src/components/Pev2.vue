<template>
  <div>
    <span>Use with <code>EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)</code></span>
    <v-row>
      <v-col cols="12" md="6">
        <v-textarea v-model="plan" dense rows="2" label="Plan" outlined></v-textarea>
      </v-col>
      <v-col cols="12" md="6">
        <v-textarea v-model="query" dense rows="2" label="Query" outlined></v-textarea>
      </v-col>
    </v-row>
    <pev2 class="pev2" ref="pev2" v-if="!loading && plan" :plan-source="plan" :plan-query="query"></pev2>
  </div>
</template>

<script>
import pev2 from 'pev2'
import { Watch, Component } from 'vue-property-decorator'
import Vue from 'vue'


@Component({
  components: {
    pev2: pev2
  }
})
export default class Pev2 extends Vue {
  plan = ""
  query = ""
  loading = false

  @Watch("plan")
  onPlanChange() {
    if (this.plan) {
      this.loading = true
      window.setTimeout(() => this.loading = false, 10)
    }
  }

  @Watch("query")
  onQueryChange() {
    if (this.query) {
      this.loading = true
      window.setTimeout(() => this.loading = false, 10)
    }
  }
}

</script>

<style scoped>
.plan-container {
  margin-left: -15px;
  margin-right: -15px;
  margin-top: -12px;
}
</style>

<style>
/* Undo bootstrap fuckery */
*:hover {
  text-decoration: none !important;
}
</style>
