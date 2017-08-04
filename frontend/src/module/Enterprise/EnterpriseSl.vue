<template>
  <div id="app">
      <Button type="info" @click="trans" class="btn">{{ type }}</Button>
      <div v-show="signup">
        <enterprise-signup></enterprise-signup>
      </div>
      <div v-show="login">
        <enterprise-login></enterprise-login>
      </div>
  </div>
</template>
<script>
  import EnterpriseLogin from '../../components/EnterpriseLogin'
  import EnterpriseSignup from '../../components/EnterpriseSignup'
  export default {
    components: {
      EnterpriseSignup,
      EnterpriseLogin
    },
    data () {
      return {
        signup: false,
        login: true,
        type: '注册'
      }
    },
    methods: {
      trans () {
        if (this.signup === true) {
          this.signup = false
          this.login = true
          this.type = '注册'
        } else {
          this.signup = true
          this.login = false
          this.type = '登录'
        }
      }
    }
  }
</script>
<style scoped>
.btn {
  display: block;
  width: 200px;
  height: 50px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 50px;
  background-color: #D8D8D8;
}
.btn:hover {
  background-color: #2d8cf0;
}
</style>