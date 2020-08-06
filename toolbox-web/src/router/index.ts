import Vue from 'vue'
import VueRouter, {RouteConfig} from 'vue-router'
import Home from '../components/Home.vue'
import FlameGraph from '@/components/FlameGraph.vue'
import Spectrograph from '@/components/Spectrograph.vue';
import Pev2 from '@/components/Pev2.vue';

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {path: '/', component: Home},
  {path: '/tool/FlameGraph', component: FlameGraph},
  {path: '/tool/Spectrograph', component: Spectrograph},
  {path: '/tool/pev2', component: Pev2}
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
