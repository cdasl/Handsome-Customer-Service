<template>
  <div class="customertalk">
    <div id="app">
      <div class="sidebar">
        <card></card>
        <list :lists="lists" @swit="swit"></list>
      </div>
      <div class="main">
        <message :content="content"></message>
        <text-input @onKeyup="send"></text-input>
      </div>
    </div>
    <div class="userinfo">
      <user-info></user-info>
      <div class="buttongroup">
        <Button type="primary" class="button">转接</Button>
        <Button type="primary" class="button">结束会话</Button>
      </div>
    </div>
  </div>
</template>
<script>
  import Card from './Card'
  import List from './List'
  import TextInput from './TextInput'
  import Message from './Message'
  import UserInfo from './UserInfo'
  export default {
    components: {Card, List, TextInput, Message, UserInfo},
    props: {
      content: {
        type: Array
      },
      lists: {
        type: Array
      }
    },
    methods: {
      send (message) {
        this.$emit('send', message)
      },
      swit (item) {
        this.$emit('swit', item)
      }
    }
  }
</script>
<style scoped>
.customertalk {
  display: flex;
}
#app {
  width: 70%;
  height: 90vh;
  overflow: hidden;
  border-radius: 3px;
}
#app .sidebar, #app .main {
  height: 100%;
}
#app .sidebar {
  float: left;
  width: 20%;
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
.userinfo {
  width: 30%;
}
.buttongroup {
  margin-top: 20%;
}
.button {
  margin-left: 10%;
}
</style>