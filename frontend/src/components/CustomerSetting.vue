<template>
  <div>
    <h2>个人信息</h2>
    <hr class="hr">
    <Form :model="formItem" class="form" label-position="left" :label-width="80">
      <Form-item label="邮箱">
        <Input v-model="formItem.mail" class="input" disabled>
      </Form-item>
      <Form-item label="名称">
        <Input v-model="formItem.name" class="input">
      </Form-item>
      <Form-item label="头像">
        <img :src="formItem.image" class="image">
        <Upload action="" :before-upload="handleUpload" >
          <Button type="ghost" icon="ios-cloud-upload-outline" >更换头像</Button>
        </Upload>
      </Form-item>
      <Form-item>
        <img :src="upload" class="image" v-show="show">
      </Form-item>
      <Form-item>
        <Button type="primary" @click="save">保存</Button>
      </Form-item>
    </Form>
    <h2>密码设置</h2>
    <hr class="hr">
    <Form :model="passwordItem" class="form" label-position="left" :label-width="80">
      <Form-item label="原密码">
        <Input v-model="passwordItem.oldpassword" class="input" placeholder="请输入原密码">
      </Form-item>
      <Form-item label="新密码">
        <Input v-model="passwordItem.newpassword" class="input" placeholder="请输入新密码">
      </Form-item>
      <Form-item label="确认新密码">
        <Input v-model="passwordItem.confirm" class="input" placeholder="确认新密码">
      </Form-item>
      <Form-item>
        <Button type="primary" @click="submit">提交</Button>
      </Form-item>
    </Form>
  </div>
</template>
<script>
  import global_ from './Const'
  export default {
    data () {
      return {
        formItem: {
          mail: '123456@qq.com',
          name: '张三',
          image: '/static/img/logo.jpg'
        },
        passwordItem: {
          oldpassword: '',
          newpassword: '',
          confirm: ''
        },
        upload: '',
        show: false
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
      handleUpload (file) {
        /* global FormData: true */
        let image = new FormData()
        image.append('image', file)
        fetch('/storeimage/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json'
          },
          body: image
        }).then((res) => res.json()).then((res) => {
          this.upload = res['url']
          this.show = true
        })
        return false
      },
      save () {
        if (this.formItem['name'] === '') {
          console.log('名称不可为空')
          return
        }
        fetch('/api/customer/modify/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({icon: this.upload, name: this.formItem['name']})
        }).then((res) => res.json()).then((res) => {
          if (res['flag'] === global_.CONSTGET.CID_NOT_EXIST) {
            this.$Message.error(global_.CONSTSHOW.CID_NOT_EXIST)
            window.location.replace('/customer_login/')
          } else if (res['flag'] === global_.CONSTGET.ERROR) {
            this.$Message.error(global_.CONSTSHOW.ERROR)
          } else {
            this.$Message.success('保存成功')
          }
        })
      },
      reset () {
        this.passwordItem.oldpassword = ''
        this.passwordItem.newpassword = ''
        this.passwordItem.confirm = ''
      },
      submit () {
        if (this.passwordItem.newpassword !== this.passwordItem.confirm) {
          this.$Message.warning('两次输入的密码不一致')
        } else if (this.passwordItem.newpassword.trim().length < 8) {
          this.$Message.warning('密码长度不能小于8')
        } else {
          fetch('/api/customer/modify_password/', {
            method: 'post',
            credentials: 'same-origin',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken'),
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({old: this.passwordItem.oldpassword, new: this.passwordItem.newpassword})
          }).then((res) => res.json()).then((res) => {
            if (res['flag'] === global_.CONSTGET.WRONG_PASSWORD) {
              this.$Message.error(global_.CONSTSHOW.WRONG_PASSWORD)
            } else if (res['flag'] === global_.CONSTGET.FAIL_MODIFY) {
              this.$Message.error(global_.CONSTSHOW.FAIL_MODIFY)
            } else {
              this.$Message.success('修改成功')
            }
          })
        }
        this.reset()
      }
    },
    created: function () {
      fetch('/api/customer/get_info/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then((res) => res.json()).then((res) => {
        if (res['flag'] === global_.CONSTGET.CID_NOT_EXIST) {
          this.$Message.error(global_.CONSTSHOW.CID_NOT_EXIST)
          window.location.replace('/customer_login/')
        }
        this.formItem['mail'] = res['message']['email']
        this.formItem['name'] = res['message']['name']
        this.formItem['image'] = res['message']['icon']
        this.upload = this.formItem['image']
      })
    }
  }
</script>
<style scoped>
  h2 {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial,sans-serif;
    font-size: 16px;
  }
  .form {
    margin-left: 30px;
  }
  .hr {
    filter: alpha(opacity = 100,finishopacity = 0,style = 3);
    width: 80%;
    color: #987cb9;
    size: 3;
    margin-bottom: 40px;
    margin-top: 20px;
  }
  .image {
    width: 75px;
    height: 75px;
  }
  .input {
    width: 300px;
  }
</style>