import Vue from 'vue'
import Vuex from 'vuex'
import DefaultModule from '@/store/DefaultModule'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    def: DefaultModule
  }
})
