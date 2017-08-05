import Vue from 'vue'
import CustomerActivity from './CustomerActivity'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

Vue.use(iView)

/* eslint-disable no-new */
new Vue({
  el: '#customeractive',
  components: { CustomerActivity }
})
