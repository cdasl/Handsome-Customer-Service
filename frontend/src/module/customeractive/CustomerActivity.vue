<template>
  <div id="app">
    <h1>客服人员激活信息完善</h1>
    <Form :model="formItem" class="form">
      <Form-item label="密码" class="input">
        <Input v-model="formItem.password" placeholder="输入密码，长度不小于8" type="password" ></Input>
      </Form-item>
      <Form-item label="再次输入密码" class="input">
        <Input v-model="formItem.password2" placeholder="请再次输入密码" type="password"></Input>
      </Form-item>
      <Form-item label="名称" class="input">
        <Input v-model="formItem.name" placeholder="请输入名称"></Input>
      </Form-item>
      <Form-item class="upload">
        <Upload action="/" :before-upload="handleUpload" >
          <Button type="ghost" icon="ios-cloud-upload-outline" >上传头像</Button>
        </Upload>
        <div v-if="file !== null" >待上传文件：{{ file.name }}</div>
      </Form-item>
      <Form-item>
        <Button type="primary" @click="submit" class="submit">提交</Button>
      </Form-item>
    </Form>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        formItem: {
          password: '',
          password2: '',
          name: ''
        },
        file: null
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
        if (this.formItem.name === '' || this.formItem.password === '' || this.formItem.password2 === '' || this.file === null) {
          /* global alert: true */
          alert('请填写所有信息并上传头像')
          return
        }
        if (this.formItem.password !== this.formItem.password2) {
          alert('两次密码不相同')
          return
        }
        /* global FormData: true */
        let image = new FormData()
        image.append('image', this.file)
        image.append('user', 'com')
        fetch('/validate/customer/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json'
          },
          body: image
        }).then((res) => res.json()).then((res) => {
          console.log(res)
        })
      },
      geturl () {
        let url = window.location.href
        let code = url.split('/')
        return code
      },
      handleUpload (file) {
        this.file = file
        return false
      }
    }
  }
</script>
<style scoped>
h1 {
  text-align: center;
  margin-bottom: 50px;
  margin-top: 100px;
}
#app {
  margin: auto;
  width: 50%;
}
.input {
  display: block;
  width: 200px;
  margin-left: auto;
  margin-right: auto;
}
.upload {
  display: block;
  margin-left: 37%;
  margin-right: auto;
}
.submit {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>