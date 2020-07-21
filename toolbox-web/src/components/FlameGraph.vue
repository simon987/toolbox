<template>
  <v-container>

    <p>Run with <code>perf record -F997 --call-graph dwarf -q &lt;program&gt;</code></p>

    <v-file-input :loading="loading" label="perf.data" id="flamegraph-upload" @change="onUpload()"></v-file-input>

    <object v-if="key" type="image/svg+xml" :data="getGraphUrl()"></object>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import {Component} from 'vue-property-decorator'
import {namespace} from 'vuex-class'
import {toolByName} from '@/tools'
import axios from 'axios'
import {FlameGraphResult} from "@/models";
import {API_URL} from "@/config";

const def = namespace('def')

@Component
export default class FlameGraph extends Vue {
  public tool = toolByName('FlameGraph')
  public key: string | null = null
  public loading = false

  getGraphUrl() {
    return `${API_URL}/flame_graph/${this.key}`
  }

  onUpload() {
    this.loading = true;
    const formData = new FormData();
    const input = document.getElementById('flamegraph-upload') as any;

    formData.append('file', input.files[0]);
    axios.post('http://localhost:8000/flame_graph', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(resp => {
      const result = resp.data as FlameGraphResult

      this.key = result.key
      this.loading = false;
    })
  }
}
</script>
