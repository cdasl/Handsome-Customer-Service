<template>
  <div id="app">
    <div class="menu">
      <Menu mode="horizontal" theme="light" active-name="enterprise-signup" @on-select="select" class="nav">
        <Menu-item name="enterprise-signup">注册</Menu-item>
        <Menu-item name="enterprise-login">登录</Menu-item>
      </Menu>
    </div>
    <div :is="type" class="content"></div>
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
        type: 'enterprise-signup'
      }
    },
    methods: {
      select (name) {
        this.type = name
      }
    }
  }
</script>
<style scoped>
.menu {
  display: block;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  background-color: #CEF6F5;
}
.content {
  display: block;
  width: 20%;
  margin-left: auto;
  margin-right: auto;
}
.nav {
  display: block;
  width: 20%;
  margin-left: auto;
  margin-right: auto;
  background-color: #CEF6F5;
}
</style>