<template>
<div class="message">
  <ul>
    <li v-for="(item,index) in content">
      <p class="time">
        <span>{{ item.time }}</span>
      </p>
      <div class="main" :class="{self: item.self}">
        <img class="avatar" width="30" height="30" :src="item.src">
        <div v-if="checktype(item.word)"class="text" v-html="explain(item.word)"></div>
        <ImageShow v-else :address="item.word"></ImageShow>
      </div>
    </li>
  </ul>
</div>
</template>
<script>
  import ImageShow from './ImageShow'
  export default {
    components: {ImageShow},
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
    watch: {
      content (curVal, oldVal) {
        this.$nextTick(() => {
          let div = document.querySelector('.message')
          div.scrollTop = div.scrollHeight
        })
      }
    },
    methods: {
      explain: function (content) {
        return this.we.explain(content)
      },
      checktype (word) {
        let pattern = /\/static\/upload\/*/
        return !pattern.test(word)
      }
    },
    created: function () {
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
    padding-bottom: 3vh;
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