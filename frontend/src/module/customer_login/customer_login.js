import Vue from 'vue'
import CustomerLogin from './CustomerLogin'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

Vue.use(iView)

/* eslint-disable no-new */
new Vue({
  el: '#customerlogin',
  components: { CustomerLogin }
})
