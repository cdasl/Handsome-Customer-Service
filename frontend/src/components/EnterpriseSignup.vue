<template>
  <div id="app">
    <h3 class="title">注册</h3>
    <Input v-model="formItem.email" placeholder="请输入邮箱" type="text" class="my-input"></Input>
    <Input v-model="formItem.password" placeholder="请输入密码，长度不小于8" type="password" class="my-input"></Input>
    <Input v-model="formItem.password2" placeholder="请确认密码" type="password" class="my-input"></Input>
    <Input v-model="formItem.name" placeholder="请输入企业名称" class="my-input"></Input>
    <Button type="primary" @click="submit" class="my-input">立即注册</Button>
    <p class="clause">点击立即注册即表示你已阅读并同意<a href="">汉森服务条款</a></p>
    <p class="login">已有账号?<a @click="trans">点击登陆!</a></p>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        formItem: {
          email: '',
          password: '',
          password2: '',
          name: ''
        }
      }
    },
    methods: {
      fetchBase (url, body) {
        return fetch(url, {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(body)
        })
        .then((res) => res.json())
      },
      trans () {
        this.$emit('transfer', 'enterprise-login')
      },
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
      async submit () {
        // 检查是否为空
        if (this.formItem.email === '' || this.formItem.password === '' || this.formItem.password2 === '' || this.formItem.name === '') {
          this.$Message.warning('邮箱不能为空')
          return
        }
        // 检查邮箱格式
        if (this.checkEmail(this.formItem.email) === false) {
          this.$Message.warning('邮箱格式错误')
          return
        }
        // 检查两次密码输入是否一致
        if (this.formItem.password !== this.formItem.password2) {
          this.$Message.warning('两次密码不同')
          return
        }
        let res = await this.fetchBase('/api/enter/signup/', {
          'email': this.formItem.email,
          'password': this.formItem.password,
          'name': this.formItem.name
        })
        this.reset()
        if (res['flag'] > 0) {
          this.$Message.success('注册成功')
          this.trans()
        } else if (res['flag'] === -3) {
          this.$Message.error('该邮箱已被注册')
        } else if (res['flag'] === -4) {
          this.$Message.error('注册失败')
        }
      }
    }
  }
</script>
<style scoped>
.app {
  width: 100%;
}
.title {
  margin-left: 5vw;
  margin-bottom: 2vh;
  font-size: 1.5em;
}
.my-input {
  width: 75%;
  height: 30%;
  margin-left: 5vw;
  margin-bottom: 2vh;
}
.clause {
  width: 45%;
  height: 15%;
  font-size: 1em;
  margin-left: auto;
  margin-right: auto;
}
.login {
  width: 32%;
  height: 15%;
  font-size: 1.4em;
  margin-left: auto;
  margin-right: auto;
}
</style>