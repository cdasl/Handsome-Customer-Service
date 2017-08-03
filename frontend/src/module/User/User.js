import Vue from 'vue'
import UserTalk from './UserTalk'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

Vue.use(iView)

/* eslint-disable no-new */
new Vue({
  el: '#user',
  components: { UserTalk }
})
