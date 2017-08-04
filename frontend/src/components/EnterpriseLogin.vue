<template>
  <div id="app">
    <Alert v-show="warn">
        <template slot="desc">{{ warnMes }}</template>
    </Alert>
    <Form :model="formItem" label-width="80" label-position="left">
      <Form-item label="邮箱">
          <Input v-model="formItem.email" placeholder="邮箱" type="text"></Input>
      </Form-item>
      <Form-item label="密码">
          <Input v-model="formItem.password" placeholder="密码" type="password" ></Input>
      </Form-item>
      <Form-item style="margin-top:30px;">
          <Button type="primary" @click="submit">登录</Button>
      </Form-item>
    </Form>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        warn: false,
        warnMes: '',
        formItem: {
          email: '',
          password: ''
        }
      }
    },
    methods: {
      getCookie (cName) {
        if (document.cookie.length > 0) {
          let cStart = document.cookie.indexOf(cName + '=')
          if (cStart !== -1) {
            cStart = cStart + cName.length + 1
            let cEnd = document.cookie.indexOf(';', cStart)
            if (cEnd === -1) {
              cEnd = document.cookie.length
            }
            return unescape(document.cookie.substring(cStart, cEnd))
          }
        }
        return ''
      },
      reset () {
        this.formItem.email = ''
        this.formItem.password = ''
        this.formItem.password2 = ''
        this.formItem.name = ''
      },
      warning (s) {
        this.warnMes = s
        this.warn = true
        setTimeout(() => { this.warn = false }, 2000)
        this.reset()
      },
      submit () {
        // 检查是否为空
        if (this.formItem.email === '' || this.formItem.password === '') {
          this.warning('不能有内容为空')
          return
        }
        fetch('/api/enter/login/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'email': this.formItem.email,
            'password': this.formItem.password
          })
        })
        .then((res) => res.json())
        .then((res) => {
          this.warning(res['message'])
          this.reset()
        })
      }
    }
  }
</script>
<style scoped>
.form {
   width: 200px;
   margin-left: auto;
   margin-right: auto;
   margin-top:100px;
}
.title {
  text-align: center;
  margin-top: 100px;
  margin-bottom: -100px;
}
</style>