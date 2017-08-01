// polyfill
import 'babel-polyfill'
import Vue from 'vue'
import User from './User'
import store from './store'

Vue.config.devtools = true

new Vue({
  el: 'body',
  components: { User },
  store: store
})
