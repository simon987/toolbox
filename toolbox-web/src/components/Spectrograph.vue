<template>
  <v-container>

    <v-form v-model="valid" id="spectrograph-form">
      <v-row>
        <v-col>
          <v-text-field :rules="[x => x < 20000 && x > 100]" label="Width" type="number" value="5000"
                        name="x"></v-text-field>
        </v-col>
        <v-col>
          <v-text-field :rules="[y => y < 20000 && y > 100]" label="Height" type="number" value="1100"
                        name="y"></v-text-field>
        </v-col>
        <v-col>
          <v-text-field :rules="[z => z < 120 && z > 20]" label="Z" type="number" value="100"
                        name="z"></v-text-field>
        </v-col>
      </v-row>
      <v-text-field label="Label" name="label"></v-text-field>
      <v-select label="Window" :items="windows" value="Kaiser" name="window"></v-select>

      <v-file-input name="file" :disabled="!valid || loading" :loading="loading" label="Audio file" id="spectrograph"
                    @change="onUpload()"></v-file-input>
    </v-form>

    <a v-if="key" :href="getImageUrl()" target="_blank"><img width="100%" type="image/png" :src="getImageUrl()" id="img"></a>

  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import {Component} from 'vue-property-decorator'
import {toolByName} from '@/tools'
import axios from 'axios'
import {API_URL} from '@/config';

@Component
export default class Spectrograph extends Vue {
  public tool = toolByName('Spectrograph')
  public key: string | null = null
  public loading = false
  public apiUrl = API_URL

  public valid = true

  public windows = [
    "Hann",
    "Hamming",
    "Bartlett",
    "Rectangular",
    "Kaiser",
    "Dolph"
  ]

  getImageUrl() {
    return `${API_URL}/data/${this.key}?type=image/png`
  }

  onUpload() {
    this.loading = true;
    const formData = new FormData(document.getElementById("spectrograph-form") as any);
    const input = document.getElementById("spectrograph") as any;

    if (!formData.get("label")) {
      formData.set("label", " ")
    }

    formData.set("type", input.value.split(".").slice(-1)[0])

    axios.post(API_URL + '/spectrograph', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(resp => {
      const result = resp.data

      this.key = result.key
      this.loading = false;
    })
  }
}
</script>

<style>
.img-zoom-result {
  width: 325px;
  height: 325px;
}
</style>
