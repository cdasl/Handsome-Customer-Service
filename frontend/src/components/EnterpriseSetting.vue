<template>
  <div class="app">
    <script type="text/javascript" src="https://github.com/10Web/10WEB/blob/master/10web/assets/js/jquery.min.js"></script>
	    <script type="text/javascript" src="https://github.com/10Web/10WEB/blob/master/10web/assets/js/picture-uploader/uploader.js"></script>
    <div class="psw">
      <h4 class="title">1.修改密码</h4>
      <Form v-model="password" :label-width="80">
        <Form-item label="原密码">
          <Input v-model="password.old" class="my-input"></Input>
        </Form-item>
        <Form-item label="新密码">
          <Input v-model="password.new" class="my-input"></Input>
        </Form-item>
          <Button @click="resetPassword" type="primary" class="btn">修改</Button>
        <Form-item>
        </Form-item>
      </Form>
    </div>
    <div class="pop-up">
      <h4 class="title">2.接入代码</h4>
      <p class="legend">请将以下代码添加到你网站的 HTML 源代码中，放在&lt;/body&gt;标签之前 </p><br>
      <Select v-model="model" style="width:200px" @on-change="changeTypePop">
        <Option v-for="item in types" :value="item.value" :key="item.value">{{ item.label }}</Option>
      </Select><br>
      <textarea cols="60" rows="5" v-model="innerCode" readonly class="text-area"></textarea>
    </div>
    <div class="robot">
      <h4 class="title">3.机器人设置</h4>
      <Form :label-width="80" class="left">
        <Form-item label="机器人昵称">
          <Input v-model="robotName" class="my-input"></Input>
        </Form-item>
        <a href="javascript:;" class="a-upload">
          <input type="file" id="file">选择图片
        </a>
        <Button size="large" @click="uploadImg">上传图片</Button><br><br>
        <Button type="primary" @click="submit" class="btn">确认</Button>
      </Form>
      <div class="right">
          <img :src="imgSrc" class="preview">
        </div>
    </div>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        imgSrc: 'http://123.206.94.77:3980/rkJfLkwPZ.jpg',
        robotName: '小机',
        robotIcon: '',
        innerCode: '内嵌',
        model: '',
        types: [
          {
            value: 1,
            label: '内嵌'
          },
          {
            value: 2,
            label: '弹出新窗口'
          }
        ],
        password: {
          old: '',
          new: ''
        }
      }
    },
    methods: {
      submit () {
        fetch('', {
          method: 'post'
        })
      },
      uploadImg () {
        let input = document.querySelector('#file')
        /* global FormData: true */
        let data = new FormData()
        data.append('file', input.files[0])
        fetch('http://123.206.94.77:3980/picture', {
          method: 'post',
          body: data
        })
        .then((res) => res.json())
        .then((res) => {
          let data = res.data
          this.imgSrc = data[0]
        })
      },
      resetPassword () {
        if (this.password.old.trim() === '' || this.password.new.trim() === '') {
          this.$Message.warning('密码不能为空')
          this.password.old = ''
          this.password.new = ''
          return
        }
      },
      changeTypePop () {
        fetch('/api/enter/chattype/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'chatbox_type': this.model,
            'eid': 'c56b178639436b776adc1235a29512ca'
          })
        })
        .then((res) => res.json())
        .then((res) => {
          console.log(res['message'])
          if (this.model === 1) {
            this.innerCode = '内嵌'
          } else {
            this.innerCode = '新窗口'
          }
        })
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
      }
    }
  }
</script>
<style lang="">
.app {
  width: 100%;
  height: 100%;
  background-color: white;
}
.psw {
  display: block;
  width: 100%;
  height: 30%;
}
.pop-up {
  display: block;
  width: 100%;
  height: 30%;
}
.my-input {
  width: 30%;
}
.legend {
  font-size: 12px;
  line-height: 1;
  color: #999;
  padding-bottom: 15px;
}
.title {
  font-size: 14px;
  line-height: 1;
  color: #222;
  padding: 20px 0 20px 0;
}
.robot {
  display: block;
  width: 100%;
  height: 40%;
}
.btn {
  margin-left: 30px;
}
.text-area {
  margin-top: 10px;
}
.left {
  display: inline;
  width: 60%;
}
.right {
  display: inline;
  width: 40%;
}
.preview {
  width: 100px;
  height: 100px;
}
.a-upload {
  padding: 4px 10px;
  height: 50px;
  line-height: 30px;
  position: relative;
  cursor: pointer;
  color: #888;
  background: #fafafa;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  display: inline-block;
  *display: inline;
  *zoom: 1
}
.a-upload  input {
  position: absolute;
  font-size: 100px;
  right: 0;
  top: 0;
  opacity: 0;
  filter: alpha(opacity = 0);
  cursor: pointer
}
.a-upload:hover {
  color: #444;
  background: #eee;
  border-color: #ccc;
  text-decoration: none
}
</style>