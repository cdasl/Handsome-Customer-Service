<template>
<div class="message">
  <ul>
    <li>
      <p class="time">
        <span>2017/8/1</span>
      </p>
      <div class="main self">
        <img class="avatar" width="30" height="30">
        <div class="text">内容</div>
      </div>
    </li>
  </ul>
  <div class="wrapper"></div>
</div>
</template>
<script>
  export default {
    data () {
      return {
        /* global wantEmoji: true */
        we: null
      }
    },
    mounted: function () {
      // 由于在created和data中dom尚未渲染，所以无法在created和data中进行初始化
      this.we = new wantEmoji({
        wrapper: '.wrapper',
        callback: function (emojiCode) {
          console.log(emojiCode)
        },
        autoInit: true
      })
    }
  }
</script>
<style type="text/css" scoped>
  .wrapper {
    position: absolute;
    bottom: 20%;
    height: 200px;
  }
</style>
<style lang="less" scoped>
.message {
  padding: 10px 15px;
  overflow-y: scroll;
  li {
    margin-bottom: 15px;
  }
  .time {
    margin: 7px 0;
    text-align: center;
    > span {
      display: inline-block;
      padding: 0 18px;
      font-size: 12px;
      color: #fff;
      border-radius: 2px;
      background-color: #dcdcdc;
    }
  }
  .avatar {
    float: left;
    margin: 0 10px 0 0;
    border-radius: 3px;
  }
  .text {
    display: inline-block;
    position: relative;
    padding: 0 10px;
    max-width: ~'calc(100% - 40px)';
    min-height: 30px;
    line-height: 2.5;
    font-size: 12px;
    text-align: left;
    word-break: break-all;
    background-color: #fafafa;
    border-radius: 4px;
    &:before {
      content: " ";
      position: absolute;
      top: 9px;
      right: 100%;
      border: 6px solid transparent;
      border-right-color: #fafafa;
    }
  }
  .self {
    text-align: right;
    .avatar {
      float: right;
      margin: 0 0 0 10px;
    }
    .text {
      background-color: #b2e281;
      &:before {
        right: inherit;
        left: 100%;
        border-right-color: transparent;
        border-left-color: #b2e281;
      }
    }
  }
}
</style>