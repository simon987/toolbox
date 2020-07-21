<template>
  <v-app>
    <v-navigation-drawer app>
      <v-list dense>
        <v-list-item link to="/">
          <v-list-item-action>
            <v-icon>mdi-apps</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item link v-for="tool in tools" :key="tool.name" :to="`/tool/${tool.name}`">
          <v-list-item-action>
            <v-icon>{{ tool.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ tool.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="lime" app>
      <v-toolbar-title>Toolbox</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
    <v-footer app>
      <span class="monospace">{{ status }}</span>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
import {Component} from 'vue-property-decorator'
import {namespace} from 'vuex-class'
import {Tool} from '@/models';
import {tools} from "@/tools";

const def = namespace('def')

@Component
export default class App extends Vue {
  @def.State
  public status!: string

  public tools: Tool[] = tools;
}
</script>

<style>
html, body {
  padding: 0;
  margin: 0;
  overflow: hidden !important;
}

.monospace {
  font-family: monospace;
}
</style>
