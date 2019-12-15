import Vue from 'vue'
import Vuex from 'vuex'
import aside from './modules/aside.js'
import header from './modules/header.js'
import user from './modules/user'
import assets from './modules/assets'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    aside, header, user, assets
  }
})
