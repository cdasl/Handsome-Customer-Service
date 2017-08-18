<template>
  <div id="app">
    <div class="container">
      <h3 class="title">企业登录</h3>
      <Input v-model="formItem.email" placeholder="邮箱" type="text" class="enter-input"></Input>
      <Input v-model="formItem.password" placeholder="密码" type="password" class="enter-input" @on-enter="submit"></Input>
      <Button type="primary" @click="submit" class="btn">登录</Button><br>
      <p class="signup">没有账户?<a @click="trans">创建一个!</a></p>
      <p class="find-password"><a @click="findEmail">找回密码</a></p>
    </div>
    <Modal
      v-model="findback.modal"
      title="找回密码"
      @on-ok="ok"
      @on-cancel="cancel">
      <p>请输入企业邮箱</p>
      <Input v-model="findback.email"></Input>
    </Modal>
  </div>
</template>
<script>
  import global_ from './Const'
  export default {
    data () {
      return {
        formItem: {
          email: '',
          password: ''
        }, // 登陆用输入账号密码
        findback: {
          modal: false,
          email: ''
        } // 找回密码
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
        // 向父组件发送切换到注册界面消息
        this.$emit('transfer', 'enterprise-signup')
      },
      findEmail () {
        this.findback.modal = !this.findback.modal
      },
      async ok () {
        // 提交找回密码
        this.trimItem()
        let res = await this.fetchBase('/api/reset_password/', {
          'email': this.findback.email
        })
        this.findback.email = ''
        if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.warning('已发送一封邮件给您，请注意查看')
        } else if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.error(global_.CONSTSHOW.ERROR)
        } else if (res['flag'] === global_.CONSTGET.INVALID) {
          this.$Message.warning(global_.CONSTSHOW.INVALID)
        }
      },
      cancel () {},
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
        this.findback.email = ''
      },
      trimItem () {
        this.formItem.email = this.formItem.email.trim()
        this.formItem.password = this.formItem.password.trim()
        this.findback.email = this.findback.email.trim()
      },
      async submit () {
        // 提交登陆信息
        this.trimItem()
        if (this.formItem.email === '' || this.formItem.password === '') {
          this.$Message.warning('不能有内容为空')
          return
        }
        let res = await this.fetchBase('/api/enter/login/', {
          'email': this.formItem.email,
          'password': this.formItem.password
        })
        this.reset()
        if (res['flag'] === global_.CONSTGET.ACCOUNT_NOT_ACTIVETED) {
          this.$Message.warning(global_.CONSTSHOW.ACCOUNT_NOT_ACTIVETED)
        } else if (res['flag'] === global_.CONSTGET.ACCOUNT_LOGGED_OFF) {
          this.$Message.warning(global_.CONSTSHOW.ACCOUNT_LOGGED_OFF)
        } else if (res['flag'] === global_.CONSTGET.WRONG_PASSWORD) {
          this.$Message.error(global_.CONSTSHOW.WRONG_PASSWORD)
        } else if (res['flag'] === global_.CONSTGET.WRONG_ACCOUNT) {
          this.$Message.error(global_.CONSTSHOW.WRONG_ACCOUNT)
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('登陆成功')
          window.location.href = '/enter_manage/'
        }
      }
    }
  }
</script>
<style scoped>
#app {
  width: 100%;
}
.container {
  display: block;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  padding-top: 2vh;
}
.title {
  margin-left: 9%;
  margin-bottom: 2vh;
  margin-top: 2vh;
  font-size: 1.5em;
}
.enter-input {
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
.signup {
  display: inline-block;
  width: 50%;
  font-size: 1.2em;
  margin: 0;
  margin-bottom: 2vh;
  padding-left: 9%;
}
.find-password {
  display: inline-block;
  width: 40%;
  font-size: 1.2em;
  text-align: right;
  margin: 0;
  margin-bottom: 2vh;
  text-align: right;
}
</style>