<template>
  <div id="app">
      <div v-show="success">
        <p>注册成功！</p>
      </div>
      <div v-show="invalid">
        <p>链接无效！</p>
      </div>
      <div v-show="expired">
        <p>链接过期！</p>
      </div>
      <div v-show="succeeded">
        <p>已经激活！</p>
      </div>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        success: false,
        invalid: false,
        expired: false,
        succeeded: false,
        url: window.location.href
      }
    },
    created: function () {
      fetch('/api/active/', {
        method: 'post',
        credentials: 'same-origin',
        body: JSON.stringify({
          'active_code': this.url.split('/')[this.url.split('/').length - 1]
        })
      })
      .then((response) => response.json())
      .then((response) => {
        if (response['message'] === 'success') {
          this.success = true
        }
        if (response['message'] === 'expired') {
          this.expired = true
        }
        if (response['message'] === 'invalid') {
          this.invalid = true
        }
        if (response['message'] === 'succeeded') {
          this.succeeded = true
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