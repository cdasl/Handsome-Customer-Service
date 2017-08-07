  <template>
    <div>
      <div class="wrapper" v-show="emoji"></div>
      <div class="text">
        <textarea placeholder="按 Ctrl + Enter 发送" v-model="content" @keyup="onKeyup"></textarea>
      </div>
      <Button type="ghost" icon="social-octocat" class="icon" @click="toggle"></Button>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        content: '',
        emoji: true,
        we: null
      }
    },
    methods: {
      onKeyup (e) {
        if (e.ctrlKey && e.keyCode === 13 && this.content.length) {
          this.$emit('onKeyup', this.content)
          this.content = ''
        }
      },
      toggle () {
        this.emoji = !this.emoji
      }
    },
    mounted: function () {
      // 由于在created和data中dom尚未渲染，所以无法在created和data中进行初始化
      /* global wantEmoji: true */
      if (this.we === null) {
        this.we = new wantEmoji({
          wrapper: '.wrapper',
          callback: (emojiCode) => {
            this.content += emojiCode
          },
          autoInit: true
        })
      }
    }
  }
</script>
<style type="text/css" scoped>
  .text {
  height: 160px;
  border-top: solid 1px #ddd;
  }
  .text textarea {
    padding: 10px;
    height: 100%;
    width: 100%;
    border: none;
    outline: none;
    font-family: "Micrsofot Yahei";
    resize: none;
  }
  .wrapper {
    position: absolute;
    bottom: 35%;
    height: 200px;
    left: 0;
  }
  .icon {
    position: absolute;
    bottom: 27%;
    left: 0;
    z-index: 10;
  }
</style>