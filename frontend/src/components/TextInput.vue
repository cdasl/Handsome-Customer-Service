<template>
  <div class="container">
    <div class="wrapper" v-show="emoji"></div>
    <div class="text">
      <textarea placeholder="按 Ctrl + Enter 发送" v-model="content" @keyup="onKeyup"></textarea>
    </div>
    <div class="icon">
      <Button type="ghost" icon="happy-outline" @click="toggle" class="no-margin"></Button>
      <Button type="ghost" icon="scissors" @click="screenshot" class="no-margin"></Button>
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
          this.$emit('onKeyup', this.html2Escape(this.content))
          this.content = ''
        }
      },
      toggle () {
        this.emoji = !this.emoji
      },
      html2Escape (sHtml) {
        // 将html字符转义
        return sHtml.replace(/[<>&"]/g, function (c) {
          return {
            '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'
          }[c]
        })
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
        return false
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
        this.emoji = false
      }
    }
  }
</script>
<style type="text/css" scoped>
.container {
  position: relative;
}
.text {
  height: 160px;
  border-top: solid 1px #ddd;
  padding-top: 3vh;
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
  top: -150%;
  height: 200px;
  left: 0;
  background-color: whitesmoke;
}
.icon {
  position: absolute;
  width: 100%;
  top: -5%;
  left: 0;
  border-right: 1px solid black;
  border-top: 1px solid lightgray;
  background-color: white;
  z-index: 10;
}
 .no-margin {
   margin-left: -0.3vw;
 }
.upload {
  display: inline-block;
  margin-left: -0.3vw;
}
</style>