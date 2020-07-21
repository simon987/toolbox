<template>
  <div>
    <v-row>
      <v-col>
        <v-card max-width="344" to="/tool/FlameGraph">
          <v-img :src="require('@/assets/FlameGraph.png')" height="200px"></v-img>
          <v-card-title>FlameGraph</v-card-title>
          <v-card-subtitle><i>perf</i> profiling data visualization</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>

export default {
  name: 'Home',
  components: {}
}
</script>
