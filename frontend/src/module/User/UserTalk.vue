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
        this.socket.emit('my broadcast event', {data: encodeURI(message)})
      }
    },
    mounted: function () {
      if (this.socket === null) {
        let namespace = '/test'
        /* global location io: true */
        this.socket = io.connect('http://' + document.domain + ':' + location.port + namespace)
        this.socket.on('connected', (msg) => {
          this.sid = msg['sid']
        })
        this.socket.on('my response', (msg) => {
          let data = {}
          data['word'] = decodeURI(msg['data'])
          data['time'] = new Date()
          data['self'] = msg['sid'] === this.sid
          this.content.push(data)
        })
      }
    }
  }
</script>
<style lang="less" scoped>
#app {
  margin: 20px auto;
  width: 800px;
  height: 600px;
  overflow: hidden;
  border-radius: 3px;
  .sidebar, .main {
    height: 100%;
  }
  .sidebar {
    float: left;
    width: 200px;
    color: #f4f4f4;
    background-color: #2e3238;
  }
  .main {
    position: relative;
    overflow: hidden;
    background-color: #eee;
  }
  .text {
    position: absolute;
    width: 100%;
    bottom: 0;
    left: 0;
  }
  .message {
    height: ~'calc(100% - 160px)';
  }
}
</style>