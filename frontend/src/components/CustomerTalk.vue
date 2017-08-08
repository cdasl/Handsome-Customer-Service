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
  import Card from './Card'
  import List from './List'
  import TextInput from './TextInput'
  import Message from './Message'
  export default {
    components: {Card, List, TextInput, Message},
    props: {
      content: {
        type: Array
      }
    },
    methods: {
      send (message) {
        this.$emit('send', message)
      }
    }
  }
</script>
<style lang="less" scoped>
#app {
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