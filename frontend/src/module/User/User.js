// polyfill
import 'babel-polyfill'
import Vue from 'vue'
import App from './App'
import Store from './Store/Store'

Vue.config.devtools = true

/* eslint-disable no-new */
new Vue({
  el: 'body',
  components: { App },
  store: Store
})
