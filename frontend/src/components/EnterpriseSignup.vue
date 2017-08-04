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
          <Input v-model="formItem.password" placeholder="输入密码，长度不小于8" type="password"></Input>
      </Form-item>
      <Form-item label="密码确认">
          <Input v-model="formItem.password2" placeholder="请输入密码再确认一遍" type="password"></Input>
      </Form-item>
      <Form-item label="企业名称">
        <Input v-model="formItem.name" placeholder="企业名称"></Input>
      </Form-item>
      <Form-item style="margin-top:30px;">
          <Button type="primary" @click="submit">注册</Button>
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
          password: '',
          password2: '',
          name: ''
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
      checkEmail (email) {
        var ePattern = /^([A-Za-z0-9])+@([A-Za-z0-9])+\.([A-Za-z]{2,4})$/g
        return ePattern.test(email)
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
        if (this.formItem.email === '' || this.formItem.password === '' || this.formItem.password2 === '' || this.formItem.name === '') {
          this.warning('不能有内容为空')
          return
        }
        // 检查邮箱格式
        if (this.checkEmail(this.formItem.email) === false) {
          this.warning('邮箱格式错误')
          return
        }
        // 检查两次密码输入是否一致
        if (this.formItem.password !== this.formItem.password2) {
          this.warning('两次密码不同')
          return
        }
        fetch('/api/enter/signup/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'email': this.formItem.email,
            'password': this.formItem.password,
            'name': this.formItem.name
          })
        })
        .then((res) => res.json())
        .then((res) => {
          this.warning(res['message'])
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