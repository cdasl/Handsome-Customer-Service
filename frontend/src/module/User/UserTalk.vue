<template>
  <div id="app" :class="userTalk">
    <div class="sidebar">
      <card :icon="icon" :name="name"></card>
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
  import global_ from '../../components/Const'
  export default {
    components: {Card, List, TextInput, Message},
    data () {
      return {
        userTalk: '',
        socket: null,
        content: [],
        cid: '',
        timeout: null,
        disconnect: null,
        modal: false,
        value: 0,
        did: '',
        talkToRobot: true,
        uid: 'connect',
        eid: 'eeid',
        name: '',
        icon: ''
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
      ok () {
        this.socket.emit('rate', {rate: this.value, did: this.did})
        this.socket.emit('disconnect request')
      },
      cancel () {
        this.socket.emit('rate', {rate: 0})
        this.socket.emit('disconnect request')
      },
      transfer () {
        this.socket.emit('connect to customer', {uid: this.uid, eid: this.eid})
        this.talkToRobot = false
      },
      send (message) {
        let data = {}
        data['word'] = message
        data['time'] = this.dateformat(new Date())
        data['self'] = true
        data['src'] = '/static/js/emojiSources/huaji/10.jpg'
        this.content.push(data)
        this.socket.emit('user message', {data: encodeURI(message), time: data['time'], cid: this.cid, uid: this.uid, eid: this.eid, src: encodeURI(data['src']), flag: this.talkToRobot})
        if (!this.talkToRobot) {
          clearTimeout(this.timeout)
          clearTimeout(this.disconnect)
          this.timeout = setTimeout(() => {
            alert('您已超过5分钟未发送消息')
          }, 300000)
          this.disconnect = setTimeout(() => {
            alert('您已经断开连接')
            this.socket.emit('user disconnect', {cid: this.cid, uid: this.uid})
          }, 420000)
        }
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
      },
      oldData () {
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
      },
      customerOffline () {
        this.socket.on('customer offline', (msg) => {
          alert('为您服务的客服已掉线')
        })
      },
      async connectedToCustomer () {
        this.socket.on('connected to customer', (msg) => {
          this.cid = msg['cid']
          /* global alert: true */
          alert('connected to customer')
          this.timeout = setTimeout(() => {
            alert('您已超过5分钟未发送消息')
          }, 300000)
          this.disconnect = setTimeout(() => {
            alert('您已经断开连接')
            this.socket.emit('user disconnect', {cid: this.cid, uid: this.uid})
          }, 420000)
        })
      },
      myResponse () {
        this.socket.on('my response', (msg) => {
          let data = {}
          data['word'] = decodeURI(msg['data'])
          data['time'] = msg['time']
          data['self'] = false
          data['src'] = decodeURI(msg['src'])
          this.content.push(data)
        })
      },
      beTransfered () {
        this.socket.on('transfer customer', (msg) => {
          this.cid = msg['cid']
          alert('您已被转接')
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
    },
    mounted: function () {
      if (this.uid[3] === '1') {
        this.userTalk = 'user-talk'
      } else {
        this.userTalk = ''
      }
      if (this.socket === null) {
        let namespace = '/test'
        /* global location io: true */
        this.socket = io.connect('http://' + document.domain + ':' + location.port + namespace)
        this.socket.emit('a user connected', {uid: this.uid})
        this.oldData()
        this.connectedToCustomer()
        this.myResponse()
        this.beTransfered()
        this.customerOffline()
        this.socket.on('no customer online', (msg) => {
          alert('都下班还来干嘛！！')
        })
        this.socket.on('user disconnected', (msg) => {
          this.did = msg['did']
          clearTimeout(this.timeout)
          clearTimeout(this.disconnect)
          this.modal = true
        })
      }
    },
    created () {
      let href = window.location.href
      this.uid = href.split('/')[href.split('/').length - 1]
      this.eid = href.split('/')[href.split('/').length - 2]
      fetch('/api/enter/get_name/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'eid': this.eid})
      })
      .then((res) => res.json())
      .then((res) => {
        if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.name = res['message'] + '客服'
        } else {
          this.name = '汉森客服'
        }
        this.icon = '/static/img/customer_icon/uh_7.gif'
      })
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
.user-talk {
  margin: -20px auto!important;
  width: 100vw!important;
  height: 100vh!important;
  overflow: hidden!important;
  border-radius: 3px!important;
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