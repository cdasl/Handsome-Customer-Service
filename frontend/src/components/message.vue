<template>
<div class="message">
  <ul>
    <li v-for="(item,index) in content">
      <p class="time">
        <span>{{ dateformat(item.time) }}</span>
      </p>
      <div class="main" :class="{self: item.self}">
        <img class="avatar" width="30" height="30">
        <div class="text" v-html="explain(item.word)"></div>
      </div>
    </li>
  </ul>
</div>
</template>
<script>
  export default {
    props: {
      content: {
        type: Array
      }
    },
    data () {
      return {
        /* global wantEmoji: true */
        we: null
      }
    },
    methods: {
      explain: function (content) {
        return this.we.explain(content)
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
      // 由于在created和data中dom尚未渲染，所以无法在created和data中进行初始化
      if (this.we === null) {
        this.we = new wantEmoji({
          wrapper: '.wrapper1',
          callback: function (emojiCode) {
          },
          autoInit: false
        })
      }
    }
  }
</script>
<style scoped>
  .message {
    z-index: 0;
    padding: 10px 15px;
    overflow-y: scroll;
  }
  .message li {
    margin-bottom: 15px;
  }
  .message .time {
    margin: 7px 0;
    text-align: center;
  }
  .message .time > span {
    display: inline-block;
    padding: 0 18px;
    font-size: 12px;
    color: #fff;
    border-radius: 2px;
    background-color: #dcdcdc;
  }
  .message .avatar {
    float: left;
    margin: 0 10px 0 0;
    border-radius: 3px;
  }
  .message .text {
    display: inline-block;
    position: relative;
    padding: 0 10px;
    max-width: calc(100% - 40px);
    min-height: 30px;
    line-height: 2.5;
    font-size: 12px;
    text-align: left;
    word-break: break-all;
    background-color: #fafafa;
    border-radius: 4px;
  }
  .message .text:before {
    content: " ";
    position: absolute;
    top: 9px;
    right: 100%;
    border: 6px solid transparent;
    border-right-color: #fafafa;
  }
  .message .self {
    text-align: right;
  }
  .message .self .avatar {
    float: right;
    margin: 0 0 0 10px;
  }
  .message .self .text {
    background-color: #b2e281;
  }
  .message .self .text:before {
    right: inherit;
    left: 100%;
    border-right-color: transparent;
    border-left-color: #b2e281;
  }
</style>