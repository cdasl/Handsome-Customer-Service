<template>
  <div id="app">
    <div class="sidebar">
      <card></card>
      <list></list>
    </div>
    <div class="main">
      <message :content="content"></message>
      <text-input @onKeyup="send"></text-input>
      <Button type="primary" class="btn" @click="transfer" v-show="talkToRobot">转接客服</Button>
    </div>
    <Modal v-model="modal" title="本次会话结束，请对客服进行评分" @on-ok="ok" @on-cancel="cancel">
      <Rate v-model="value"></Rate>
    </Modal>
  </div>
</template>
<script>
  import Card from '../../components/Card'
  import List from '../../components/List'
  import TextInput from '../../components/TextInput'
  import Message from '../../components/Message'
  export default {
    components: {Card, List, TextInput, Message},
    data () {
      return {
        socket: null,
        content: [],
        cid: '',
        timeout: null,
        modal: false,
        value: 0,
        did: '',
        talkToRobot: true,
        uid: 'connect'
      }
    },
    methods: {
      ok () {
        this.socket.emit('rate', {rate: this.value, did: this.did})
        this.socket.emit('disconnect request')
      },
      cancel () {
        this.socket.emit('rate', {rate: 0})
        this.socket.emit('disconnect request')
      },
      transfer () {
        this.socket.emit('connect to customer', {uid: this.uid})
        this.talkToRobot = false
      },
      send (message) {
        let data = {}
        data['word'] = message
        data['time'] = this.dateformat(new Date())
        data['self'] = true
        data['src'] = '/static/js/emojiSources/huaji/10.jpg'
        this.content.push(data)
        this.socket.emit('user message', {data: encodeURI(message), time: data['time'], cid: this.cid, uid: this.uid, src: encodeURI(data['src']), flag: this.talkToRobot})
        clearTimeout(this.timeout)
        this.timeout = setTimeout(() => {
          alert('您已超过5分钟未发送消息')
        }, 300000)
      },
      dateformat: function (date) {
        let seperator1 = '-'
        let seperator2 = ':'
        let month = date.getMonth() + 1
        let strDate = date.getDate()
        if (month >= 1 && month <= 9) {
          month = '0' + month
        }
        if (strDate >= 0 && strDate <= 9) {
          strDate = '0' + strDate
        }
        var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate + ' ' + date.getHours() + seperator2 + date.getMinutes() + seperator2 + date.getSeconds()
        return currentdate
      }
    },
    mounted: function () {
      if (this.socket === null) {
        let namespace = '/test'
        /* global location io: true */
        this.socket = io.connect('http://' + document.domain + ':' + location.port + namespace)
        /* global md5: true */
        this.uid = md5(this.dateformat(new Date()))
        this.socket.emit('a user connected', {uid: this.uid})
        this.socket.on('old data', (msg) => {
          for (let i = 0; i < msg['content'].length; ++i) {
            let data = {}
            data['word'] = decodeURI(msg['content'][i]['data'])
            data['time'] = msg['content'][i]['time']
            data['self'] = msg['content'][i]['send'] === this.uid
            data['src'] = '/static/js/emojiSources/huaji/1.jpg'
            this.content.push(data)
          }
        })
        this.socket.on('connected to customer', (msg) => {
          this.cid = msg['cid']
          /* global alert: true */
          alert('connected to customer')
          this.timeout = setTimeout(() => {
            alert('您已超过5分钟未发送消息')
          }, 300000)
        })
        this.socket.on('no customer online', (msg) => {
          alert('都下班还来干嘛！！')
        })
        this.socket.on('my response', (msg) => {
          let data = {}
          data['word'] = decodeURI(msg['data'])
          data['time'] = msg['time']
          data['self'] = false
          data['src'] = decodeURI(msg['src'])
          this.content.push(data)
        })
        this.socket.on('user disconnected', (msg) => {
          this.did = msg['did']
          this.modal = true
        })
      }
    }
  }
</script>
<style scoped>
#app {
  margin: 20px auto;
  width: 800px;
  height: 600px;
  overflow: hidden;
  border-radius: 3px;
}
#app .sidebar, #app .main {
  height: 100%;
}
#app .sidebar {
  float: left;
  width: 200px;
  color: #f4f4f4;
  background-color: #2d8cf0;
}
#app .main {
  position: relative;
  overflow: hidden;
  background-color: #eee;
}
#app .text {
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
}
#app .message {
  height: calc(100% - 160px);
}
.btn {
  position: absolute;
  bottom: 26%;
  right: 0;
}
</style>