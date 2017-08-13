<template>
  <div class="app">
    <div class="wrap">
      <img src="/static/img/logo.jpg" alt="logo.jpg" class="image">
      <div :is="type" @transfer="transfer"></div>
    </div>
  </div>
</template>
<script>
  import EnterpriseSignup from '../../components/EnterpriseSignup'
  import EnterpriseLogin from '../../components/EnterpriseLogin'
  export default {
    components: {EnterpriseLogin, EnterpriseSignup},
    data () {
      return {
        type: 'enterprise-login'
      }
    },
    methods: {
      transfer (newType) {
        this.type = newType
      }
    }
  }
</script>
<style lang="">
.app {
  display: block;
  width: 100vw;
  height: 100vh;
}
.wrap {
  display: block;
  width: 40vw;
  margin-left: auto;
  margin-right: auto;
  margin-top: 20vh;
  background-color: white;
  border: 1px solid black;
}
.image {
  display: block;
  margin-left: 5vw;
  margin-bottom: 2vh;
  margin-top: 2vh;
  width: 7vw;
  height: 5vh;
}
</style>