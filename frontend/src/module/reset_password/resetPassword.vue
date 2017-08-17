<template>
  <div id="app">
    <div v-show="success">
      <p>密码已重置为12345678，请立即<a href="http://127.0.0.1:8000">登录</a>修改</p>
    </div>
    <div v-show="fail">
      <p>失败</p>
    </div>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        success: false,
        fail: false,
        url: window.location.href
      }
    },
    created: function () {
      fetch('/api/new_pwd_submit/', {
        method: 'post',
        credentials: 'same-origin',
        body: JSON.stringify({
          'active_code': this.url.split('/')[this.url.split('/').length - 1]
        })
      })
      .then((response) => response.json())
      .then((response) => {
        if (response['flag'] === 'success') {
          this.success = true
        } else {
          this.fail = true
        }
      })
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
</style>
