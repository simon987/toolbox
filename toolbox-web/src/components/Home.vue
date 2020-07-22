<template>
  <div class="px-2">
    <v-row>
        <v-card class="mx-2" max-width="344" to="/tool/FlameGraph">
          <v-img :src="require('@/assets/FlameGraph.png')" height="200px"></v-img>
          <v-card-title>FlameGraph</v-card-title>
          <v-card-subtitle><i>perf</i> profiling data visualization</v-card-subtitle>
        </v-card>

        <v-card class="mx-2" max-width="344" to="/tool/Spectrograph">
          <v-img :src="require('@/assets/Spectrograph.png')" height="200px"></v-img>
          <v-card-title>Spectrograph</v-card-title>
          <v-card-subtitle>Generate spectrograph of audio files with <i>SoX</i></v-card-subtitle>
        </v-card>
    </v-row>
  </div>
</template>

<script>

export default {
  name: 'Home',
  components: {}
}
</script>
