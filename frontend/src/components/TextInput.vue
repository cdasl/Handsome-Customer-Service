<template>
  <div class="text">
    <div class="wrapper"></div>
    <div class="wrapper2"></div>
    <textarea placeholder="按 Ctrl + Enter 发送"></textarea>
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
<style lang="less" scoped>
.text {
  height: 160px;
  border-top: solid 1px #ddd;
  textarea {
    padding: 10px;
    height: 100%;
    width: 100%;
    border: none;
    outline: none;
    font-family: "Micrsofot Yahei";
    resize: none;
  }
}
</style>
