<template>
  <div class="app">
    <div class="wrap">
      <h3 class="title">客服登录</h3>
      <Input v-model="formItem.email" placeholder="邮箱" type="text" class="customer-input"></Input>
      <Input v-model="formItem.password" placeholder="密码" type="password" class="customer-input"></Input>
      <Button type="primary" @click="submit" class="btn">登录</Button><br>
      <p class="signup"><a></a></p>
      <p class="find-password"><a @click="findEmail">找回密码</a></p>
      <Modal
       v-model="findback.modal"
       title="找回密码"
        @on-ok="ok"
        @on-cancel="cancel">
        <p>请输入邮箱</p>
        <Input v-model="findback.email"></Input>
      </Modal>
    </div>
  </div>
</template>
<script>
  import global_ from '../../components/Const'
  export default {
    data () {
      return {
        formItem: {
          email: '',
          password: ''
        },
        findback: {
          modal: false,
          email: ''
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
      findEmail () {
        this.findback.modal = !this.findback.modal
      },
      async ok () {
        let res = await this.fetchBase('/api/reset_password/', {
          'email': this.findback.email
        })
        this.findback.email = ''
        if (res['message'] === 'enterprise_reset') {
          this.$Message.warning('已发送一封邮件给您，请注意查看')
        } else {
          this.$Message.warning('发生错误')
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
        this.formItem.password2 = ''
        this.formItem.name = ''
      },
      async submit () {
        // 检查是否为空
        if (this.formItem.email === '' || this.formItem.password === '') {
          this.$Message.warning('不能有内容为空')
          return
        }
        let res = await this.fetchBase('/api/customer/login/', {
          'email': this.formItem.email,
          'password': this.formItem.password
        })
        this.reset()
        if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('登陆成功')
          window.location.href = '/customer_manage'
        } else if (res['flag'] === global_.CONSTGET.ACCOUNT_NOT_ACTIVETED) {
          this.$Message.warning('账号未激活')
        } else if (res['flag'] === global_.CONSTGET.ACCOUNT_LOGGED_OFF) {
          this.$Message.warning('账号已被注销')
        } else if (res['flag'] === global_.CONSTGET.WRONG_PASSWORD) {
          this.$Message.error('密码错误')
        } else if (res['flag'] === global_.CONSTGET.WRONG_ACCOUNT) {
          this.$Message.error('账号不存在')
        }
      }
    }
  }
</script>
<style lang="" scoped>
.app {
  width: 100%;
}
.wrap {
  display: block;
  width: 30vw;
  margin-left: auto;
  margin-right: auto;
  padding-top: 2vh;
  margin-top: 20vh;
  background-color: rgba(255, 255, 255, 1);
}
.title {
  margin-left: 17%;
  margin-bottom: 2vh;
  margin-top: 2vh;
  font-size: 1.5em;
}
.customer-input {
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
  width: 45%;
  font-size: 1.2em;
  text-align: right;
  padding-right: 3.6vw;
  margin: 0;
  margin-bottom: 2vh;
  text-align: right;
}
</style>