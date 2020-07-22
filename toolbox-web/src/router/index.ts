import Vue from 'vue'
import VueRouter, {RouteConfig} from 'vue-router'
import Home from '../components/Home.vue'
import FlameGraph from '@/components/FlameGraph.vue'
import Spectrograph from '@/components/Spectrograph.vue';

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {path: '/', component: Home},
  {path: '/tool/FlameGraph', component: FlameGraph},
  {path: '/tool/Spectrograph', component: Spectrograph}
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
