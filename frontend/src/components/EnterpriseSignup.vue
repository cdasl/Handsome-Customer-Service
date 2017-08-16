<template>
  <div id="app">
    <div class="container">
      <h3 class="title">企业注册</h3>
      <Input v-model="formItem.email" placeholder="请输入邮箱" type="text" class="my-input"></Input>
      <Input v-model="formItem.password" placeholder="请输入密码，长度不小于8" type="password" class="my-input"></Input>
      <Input v-model="formItem.password2" placeholder="请确认密码" type="password" class="my-input"></Input>
      <Input v-model="formItem.name" placeholder="请输入企业名称" class="my-input" @on-enter="submit"></Input>
      <Button type="primary" @click="submit" class="btn">立即注册</Button><br>
      <p class="login">已有账号?<a @click="trans">点击登录!</a></p>
      <p class="clause">点击立即注册即表示你已阅读并同意<a href="">汉森服务条款</a></p>  
    </div>
  </div>
</template>
<script>
  import global_ from './Const'
  export default {
    data () {
      return {
        formItem: {
          email: '',
          password: '',
          password2: '',
          name: ''
        } // 注册信息
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
        // 向父组件发送切换到登录界面消息
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
        // 检查数据格式，并提交注册信息
        if (this.formItem.email === '' || this.formItem.password === '' || this.formItem.password2 === '' || this.formItem.name === '') {
          this.$Message.warning('邮箱不能为空')
          return
        }
        if (this.checkEmail(this.formItem.email) === false) {
          this.$Message.warning('邮箱格式错误')
          return
        }
        if (this.formItem.password !== this.formItem.password2) {
          this.$Message.warning('两次密码不同')
          return
        }
        if (this.formItem.password.length < 8) {
          this.$Message.warning('密码长度至少为8位')
          return
        }
        let res = await this.fetchBase('/api/enter/signup/', {
          'email': this.formItem.email,
          'password': this.formItem.password,
          'name': this.formItem.name
        })
        this.reset()
        if (res['flag'] === global_.CONSTGET.EMAIL_REGISTERED) {
          this.$Message.error(global_.CONSTSHOW.EMAIL_REGISTERED)
        } else if (res['flag'] === global_.CONSTGET.FAIL_SIGN_UP) {
          this.$Message.error(global_.CONSTSHOW.FAIL_SIGN_UP)
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('注册成功')
          this.trans()
        }
      }
    }
  }
</script>
<style scoped>
#app {
  width: 100%;
}
.title {
  margin-left: 9%;
  margin-bottom: 2vh;
  font-size: 1.5em;
}
.container {
  display: block;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  padding-top: 2vh;
}
.my-input {
  display: block;
  width: 20vw;
  height: 30%;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 2vh;
  border-color: blue;
}
.btn {
  display: block;
  width: 20vw;
  height: 30%;
  margin-left: auto;
  margin-right: auto;
  border-color: blue;
  font-size: 1.4em;
}
.clause {
  width: 90%;
  height: 15%;
  font-size: 1em;
  margin: 0;
  padding-left: 9%;
}
.login {
  display: inline-block;
  width: 50%;
  font-size: 1.2em;
  margin: 0;
  margin-bottom: 2vh;
  padding-left: 9%;
}
</style>