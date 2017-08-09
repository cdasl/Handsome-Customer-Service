<template>
  <div id="app">
    <div class="sidebar">
      <card></card>
      <list></list>
    </div>
    <div class="main">
      <message :content="content"></message>
      <text-input @onKeyup="send"></text-input>
    </div>
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
        sid: ''
      }
    },
    methods: {
      send (message) {
        let data = {}
        data['word'] = message
        data['time'] = this.dateformat(new Date())
        data['self'] = true
        data['src'] = '/static/js/emojiSources/huaji/10.jpg'
        this.content.push(data)
        this.socket.emit('user message', {data: encodeURI(message), time: data['time'], sid: this.sid, src: encodeURI(data['src'])})
      },
      dateformat: function (date) {
        let seperator1 = '/'
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
        this.socket.emit('a user connected', {uid: 'connect to customer'})
        this.socket.on('connect to customer', (msg) => {
          this.sid = msg['sid']
          /* global alert: true */
          alert('connect to customer')
        })
        this.socket.on('my response', (msg) => {
          let data = {}
          data['word'] = decodeURI(msg['data'])
          data['time'] = msg['time']
          data['self'] = false
          data['src'] = decodeURI(msg['src'])
          this.content.push(data)
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
#app .sidebar,
#app .main {
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

</style>