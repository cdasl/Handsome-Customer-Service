import Vue from 'vue'
import EnterpriseManage from './EnterpriseManage'
import iView from 'iview'
import 'iview/dist/styles/iview.css'

Vue.use(iView)

/* eslint-disable no-new */
new Vue({
  el: '#enterprisemanage',
  components: { EnterpriseManage }
})
