<template>
  <div class="app">
    <div class="psw">
      <h4 class="title">1.修改密码</h4>
      <Form v-model="password" :label-width="80">
        <Form-item label="原密码">
          <Input v-model="password.old" class="my-input" type="password"></Input>
        </Form-item>
        <Form-item label="新密码">
          <Input v-model="password.new" class="my-input" type="password"></Input>
        </Form-item>
        <Form-item label="确认新密码">
          <Input v-model="password.newConfirm" class="my-input" type="password"></Input>
        </Form-item>
          <Button @click="resetPassword" type="primary" class="btn">修改</Button>
        <Form-item>
        </Form-item>
      </Form>
    </div>
    <img src="/static/img/split.jpg/" class="split" alt="分割线">
    <div class="pop-up">
      <h4 class="title">2.接入代码</h4>
      <p class="legend">请将以下代码添加到你网站的 HTML 源代码中，放在&lt;/body&gt;标签之前 </p><br>
      <Select v-model="popType" style="width:200px" @on-change="changeTypePop">
        <Option v-for="item in types" :value="item.value" :key="item.value">{{ item.label }}</Option>
      </Select><br>
      <textarea cols="60" rows="5" v-model="innerCode" readonly class="text-area"></textarea>
    </div>
    <img src="/static/img/split.jpg/" class="split" alt="分割线">
    <div class="robot">
      <div class="title">
        <h4>3.机器人设置</h4>
        <i-switch v-model="showRobot" @on-change="switchRobot" class="robot-switch">
          <span slot="open">开</span>
          <span slot="close">关</span>
        </i-switch>
      </div>
      <Form :label-width="80" class="left" v-if="showRobot">
        <Form-item label="机器人昵称">
          <Input v-model="robotName" class="robot-name"></Input>
        </Form-item>
        <div class="wrap">
          <div class="left">
            <h4 class="sub-title">头像系列1</h4>
            <Select v-model="iconSrc" @on-change="changeIcon" class="icon-select">
              <Option v-for="item in iconList1" :value="item" :key="item">{{ item }}</Option>
            </Select>
            <h4 class="sub-title">头像系列2</h4>
            <Select v-model="iconSrc" @on-change="changeIcon" class="icon-select">
              <Option v-for="item in iconList2" :value="item" :key="item">{{ item }}</Option>
            </Select>
          </div>
          <div class="right">
            <img :src="imgSrc" class="preview">
          </div>
        </div>
        <Button type="primary" @click="submit" class="btn">确认</Button>
      </Form>
    </div>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        showRobot: false, // 显示机器人信息
        iconList1: ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg'],
        iconList2: ['10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg'],
        imgSrc: '', // 机器人头像地址，真正地址
        iconSrc: '', // 机器人头像地址，表示上述简写
        robotName: '',
        robotIcon: '',
        innerCode: '', // 内嵌码
        popType: '',
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
        if (res['flag'] === -12) {
          this.$Message.error('设置错误')
          this.showRobot = !this.showRobot
        } else {
          this.$Message.success('修改成功')
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
          if (res['flag'] === -1) {
            this.$Message.error('旧密码错误')
          } else if (res['flag'] === -2) {
            this.$Message.warning('修改失败')
          } else {
            this.$Message.success('修改成功')
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
        if (res['flag'] === -12) {
          this.$Message.error('修改失败')
        } else {
          this.$Message.success('修改成功')
        }
      },
      async changeTypePop () {
        let res = await this.fetchBase('/api/enter/chattype/', {
          'chatbox_type': this.popType
        })
        if (res['flag'] === -12) {
          this.$Message.error('发生错误')
        } else {
          this.innerCode = res['message']
          this.$Message.success('修改成功')
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
      if (res['flag'] === -12) {
        this.$Message.error('机器人信息获取失败')
      } else {
        this.imgSrc = res['message']['robot_icon']
        this.robotName = res['message']['robot_name']
        if (res['message']['robot_state'] === 1) {
          this.showRobot = true
        }
      }
      res = await this.fetchBase('/api/enter/chattype/', {
        'chatbox_type': 1
      })
      if (res['flag'] === -12) {
        this.$Message.error('弹窗方式获取失败')
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
.my-input {
  width: 30%;
}
.robot-name {
  width: 100%;
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
}
.btn {
  margin-left: 30px;
}
.text-area {
  margin-top: 10px;
}
.wrap {
  display: block;
  width: 100vw;
  height: 20vh;
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
  width: 40%;
  height: 100%;
}
.split {
  display: block;
  width: 100%;
  height: 5vh;
}
</style>