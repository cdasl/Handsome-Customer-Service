<template>
  <div>
    <div class="wrapper" v-show="emoji"></div>
    <div class="text">
      <textarea placeholder="按 Ctrl + Enter 发送" v-model="content" @keyup="onKeyup"></textarea>
    </div>
    <div class="icon">
      <Button type="ghost" icon="social-octocat" @click="toggle"></Button>
      <Button type="ghost" icon="cube" @click="screenshot"></Button>
      <Upload :before-upload="handleUpload" action="/" class="upload">
          <Button type="ghost" icon="image"></Button>
      </Upload>
    </div>
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
      },
      screenshot () {
        /* global html2canvas: true */
        html2canvas(document.body, {
          allowTaint: true,
          taintTest: false,
          onrendered: (canvas) => {
            // 生成base64图片数据 然后将base64转换成图像文件
            let file = this.dataURLtoFile(canvas.toDataURL(), 'aa.png')
            /* global FormData: true */
            let image = new FormData()
            image.append('image', file)
            fetch('/storeimage/', {
              method: 'post',
              credentials: 'same-origin',
              headers: {
                'X-CSRFToken': this.getCookie('csrftoken'),
                'Accept': 'application/json'
              },
              body: image
            }).then((res) => res.json()).then((res) => {
              console.log(res)
              this.$emit('onKeyup', res['url'])
            })
          }
        })
      },
      dataURLtoFile (dataurl, filename) {
        /* global File, atob: true */
        let arr = dataurl.split(',')
        let mime = arr[0].match(/:(.*?);/)[1]
        let bstr = atob(arr[1])
        let n = bstr.length
        let u8arr = new Uint8Array(n)
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n)
        }
        return new File([u8arr], filename, {type: mime})
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
      },
      handleUpload (file) {
        let image = new FormData()
        image.append('image', file)
        fetch('/storeimage/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json'
          },
          body: image
        }).then((res) => res.json()).then((res) => {
          console.log(res)
          this.$emit('onKeyup', res['url'])
        })
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
  border-bottom: 1px solid #2e3238;
  border-right: 1px solid #243238;
  outline: none;
  font-family: "Micrsofot Yahei";
  resize: none;
}
.wrapper {
  position: absolute;
  bottom: 33%;
  height: 200px;
  left: 0;
}
.icon {
  position: absolute;
  bottom: 25%;
  left: 0;
  z-index: 10;
}
.upload {
  display: inline-block;
}
</style>