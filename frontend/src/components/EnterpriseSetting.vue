<template>
  <div class="app">
    <div class="psw">
      <div class="title">
        <h2>修改密码</h2>
      </div>
      <Form :model="password" class="form" label-position="left" :label-width="80">
        <Form-item label="原密码">
          <Input v-model="password.old" class="enter-input" type="password"></Input>
        </Form-item>
        <Form-item label="新密码">
          <Input v-model="password.new" class="enter-input" type="password"></Input>
        </Form-item>
        <Form-item label="确认新密码">
          <Input v-model="password.newConfirm" class="enter-input" type="password"></Input>
        </Form-item>
        <Form-item>
          <Button @click="resetPassword" type="primary">修改</Button>
        </Form-item>
      </Form>
    </div>
    <img src="/static/img/split.jpg/" class="split" alt="分割线">
    <div class="pop-up">
      <div class="title">
        <h2>接入代码</h2>
        <p class="legend">请将以下代码添加到你网站的 HTML 源代码中，放在 body 标签内 </p><br>
      </div>
      <Form class="form" label-position="left" :label-width="80">
        <Form-item label="接入方式">
          <Select v-model="popType" class="enter-input" @on-change="changeTypePop">
            <Option v-for="item in types" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </Form-item>
        <Form-item>
          <textarea class="text-area" row="80" v-model="innerCode" readonly></textarea>
        </Form-item>
      </Form>
    </div>
    <img src="/static/img/split.jpg/" class="split" alt="分割线">
    <div class="robot">
      <div class="title">
        <h2>机器人设置</h2>
        <i-switch v-model="showRobot" @on-change="switchRobot" class="robot-switch">
          <span slot="open">开</span>
          <span slot="close">关</span>
        </i-switch>
      </div>
      <Form :label-width="80" class="form" v-if="showRobot" label-position="left">
        <Form-item label="机器人昵称">
          <Input v-model="robotName" class="enter-input"></Input>
        </Form-item>
        <Form-item label="选择头像">
          <Select v-model="iconSrc" @on-change="changeIcon" class="enter-input">
            <Option v-for="item in iconList1" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </Form-item>
        <Form-item>
          <img :src="imgSrc" class="preview">
        </Form-item>
        <Form-item>
          <Button type="primary" @click="submit">确认</Button>
        </Form-item>
      </Form>
    </div>
  </div>
</template>
<script>
  import global_ from './Const'
  export default {
    data () {
      return {
        showRobot: false, // 显示机器人信息
        iconList1: ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg',
          '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg'],
        imgSrc: '', // 机器人头像地址，真正地址
        iconSrc: '', // 机器人头像地址，表示上述简写
        robotName: '',
        robotIcon: '',
        innerCode: '', // 内嵌码
        popType: 1,
        types: [
          {
            value: 1,
            label: '内嵌'
          }, {
            value: 2,
            label: '弹出新窗口'
          }
        ],
        password: {
          old: '',
          new: '',
          newConfirm: ''
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
      async switchRobot () {
        // 向后端发送设置机器人开关
        let res = await this.fetchBase('/api/enter/set_robot_state/', {})
        if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.error(global_.CONSTSHOW.ERROR)
          this.showRobot = !this.showRobot
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('修改成功')
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        }
      },
      reset () {
        this.password.old = ''
        this.password.new = ''
        this.password.newConfirm = ''
      },
      changeIcon () {
        this.imgSrc = '/static/img/robot_icon/' + this.iconSrc
      },
      async resetPassword () {
        // 企业修改密码
        if (this.password.new !== this.password.newConfirm) {
          this.$Message.warning('两次输入的新密码不一致')
        } else if (this.password.new.trim().length < 8) {
          this.$Message.warning('密码长度不能小于8')
        } else {
          let res = await this.fetchBase('/api/enter/reset_password/', {
            'old': this.password.old,
            'new': this.password.new
          })
          if (res['flag'] === global_.CONSTGET.WRONG_PASSWORD) {
            this.$Message.error(global_.CONSTSHOW.WRONG_PASSWORD)
          } else if (res['flag'] === global_.CONSTGET.FAIL_MODIFY) {
            this.$Message.warning(global_.CONSTSHOW.FAIL_MODIFY)
          } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
            this.$Message.success('修改成功')
          } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
            window.location.href = '/enterprise/'
          }
        }
        this.reset()
      },
      async submit () {
        //  提交设置机器人
        if (this.robotName.trim() === '') {
          this.$Message.warning('机器人昵称不能为空')
          return
        }
        let res = await this.fetchBase('/api/enter/set_robot_message/', {
          'robot_name': this.robotName,
          'robot_icon': this.imgSrc
        })
        if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.error(global_.CONSTSHOW.ERROR)
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('修改成功')
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        }
      },
      async changeTypePop () {
        let res = await this.fetchBase('/api/enter/chattype/', {
          'chatbox_type': this.popType
        })
        if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.error(global_.CONSTSHOW.ERROR)
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.innerCode = res['message']
          this.$Message.success('修改成功')
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        }
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
    },
    async mounted () {
      // 获取机器人信息和innerCode
      let res = await this.fetchBase('/api/enter/robot_into/', {})
      if (res['flag'] === global_.CONSTGET.ERROR) {
        this.$Message.error(global_.CONSTSHOW.ERROR)
      } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
        this.imgSrc = res['message']['robot_icon']
        this.iconSrc = this.imgSrc.split('/')[this.imgSrc.split('/').length - 1]
        this.robotName = res['message']['robot_name']
        if (res['message']['robot_state'] === 1) {
          this.showRobot = true
        }
      } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
        window.location.href = '/enterprise/'
      }
      res = await this.fetchBase('/api/enter/chattype/', {
        'chatbox_type': 1
      })
      if (res['flag'] === global_.CONSTGET.ERROR) {
        this.$Message.error(global_.CONSTSHOW.ERROR)
      } else {
        this.innerCode = res['message']
      }
    }
  }
</script>
<style scoped>
.app {
  width: 100%;
  overflow: hidden;
}
h2 {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial,sans-serif;
  font-size: 16px;
}
.psw {
  display: block;
  width: 100%;
  height: 25%;
}
.pop-up {
  display: block;
  width: 100%;
  height: 30%;
}
.enter-input {
  width: 30%;
}
.text-area {
  width: 30%;
  height: 20vh;
}
.robot-name {
  width: 100%;
}
.legend {
  font-size: 12px;
  line-height: 1;
  margin-top: 2vh;
  color: #999;
  padding-bottom: 15px;
}
.title {
  font-size: 14px;
  line-height: 1;
  color: #222;
  padding: 20px 0 20px 0;
}
.sub-title {
  display: inline;
}
.icon-select {
  display: block;
  width: 70%;
  margin-bottom: 2vh;
  margin-top: 2vh;
}
.robot {
  display: block;
  width: 100%;
  height: 45%;
}
.robot-switch {
  margin-top: 2vh;
  margin-left: 30px;
}
.text-area {
  margin-top: 10px;
}
.wrap {
  display: block;
  width: 100vw;
  height: 30vh;
  margin-bottom: 4vh;
}
.left {
  display: inline-block;
  width: 20%;
  height: 100%;
}
.right {
  display: inline-block;
  width: 25%;
  height: 100%;
}
.preview {
  width: 7vw;
  height: 15vh;
}
.split {
  display: block;
  width: 100%;
  height: 5vh;
}
.form {
  margin-left: 30px;
}
</style>