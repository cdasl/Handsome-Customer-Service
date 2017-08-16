<template>
  <div class="app">
    <div class="wrap">
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
<style scoped>
.app {
  display: block;
  width: 100vw;
  height: 80vh;
}
.wrap {
  display: block;
  width: 30vw;
  margin-left: auto;
  margin-right: auto;
  margin-top: 20vh;
  background-color: rgba(255, 255, 255, 1);
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