<template>
  <div class="app">
    <div class="wrap">
      <h3 class="title">设置初始信息</h3>
      <Input v-model="formItem.password" placeholder="输入密码，长度不小于8" type="password" class="customer-input"></Input>
      <Input v-model="formItem.password2" placeholder="请再次输入密码" type="password" class="customer-input"></Input>
      <Input v-model="formItem.name" placeholder="请输入名称" class="customer-input"></Input>
      <Button type="primary" @click="submit" class="btn">提交</Button>
    </div>
  </div>
</template>
<script>
  import global_ from '../../components/Const'
  export default {
    data () {
      return {
        formItem: {
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
      submit () {
        if (this.formItem.name === '' || this.formItem.password === '' || this.formItem.password2 === '') {
          /* global alert: true */
          this.$Message.warning('请填写所有信息并上传头像')
          return
        }
        if (this.formItem.password !== this.formItem.password2) {
          this.$Message.warning('两次密码不相同')
          return
        }
        if (this.formItem.password.length < 8) {
          this.$Message.warning('密码长度不能小于8')
          return
        }
        /* global FormData: true */
        fetch('/validate/customer/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'password': this.formItem.password,
            'name': this.formItem.name,
            'active_code': this.geturl(),
            'icon': '/static/img/customer_icon/uh_1.gif'
          })
        })
        .then((res) => res.json())
        .then((res) => {
          if (res === global_.CONSTGET.INVALID) {
            this.$Message.error(global_.CONSTSHOW.INVALID)
          } else if (res['flag'] === global_.CONSTGET.EXPIRED) {
            this.$Message.error(gloab_.CONSTGET.EXPIRED)
          } else if (res['flag'] === global_.CONSTGET.ACCOUNT_ACTIVITED) {
            this.$Message.error(gloab_.CONSTGET.ACCOUNT_ACTIVITED)
          } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
            this.$Message.error(gloab_.CONSTGET.SUCCESS)
            window.location.href = '/customer_login/'
          } else if (res['flag'] === global_.CONSTGET.ERROR) {
            this.$Message.error(gloab_.CONSTGET.ERROR)
          }
        })
      },
      geturl () {
        let url = window.location.href
        let code = url.split('/')
        return code[code.length - 1]
      }
    }
  }
</script>
<style scoped>
.app {
  width: 100%;
}
.wrap {
  display: block;
  width: 30vw;
  height: 35vh;
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
  height: 4vh;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 2vh;
  border-color: blue;
}
.line {
  display: block;
  width: 20vw;
  margin-left: auto;
  margin-right: auto;
}
.upload {
  display: inline-block;
  width: 6vw;
  margin: auto;
}
.show-src {
  display: inline-block;
  width: 14vw;
  text-align: right;
}
.btn {
  display: block;
  width: 20vw;
  height: 5vh;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 2vh;
  border-color: blue;
  font-size: 1.4em;
}
</style>