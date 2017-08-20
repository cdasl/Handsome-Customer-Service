<template>
  <div>
    <Card dis-hover>
      <p solt="title" class="title">用户信息</p>
      <p class="item">姓名: {{ name }}</p>
      <p class="item">性别: {{ gender }}</p>
      <p class="item">年龄: {{ age }}</p>
    </Card>
  </div>
</template>
<script>
  import global_ from './Const'
  export default {
    props: ['uid'],
    data () {
      return {
        name: '',
        age: '',
        gender: ''
      }
    },
    watch: {
      uid: function () {
        fetch('/api/customer/user_info/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'uid': this.uid})
        })
        .then((res) => res.json())
        .then((res) => {
          if (res['flag'] === global_.CONSTGET.SUCCESS) {
            let info = JSON.parse(res['message'])
            this.name = info.name
            this.age = info.age
            this.gender = info.gender
          }
        })
      }
    },
    methods: {
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
      }
    },
    created () {
      if (this.uid !== '') {
        fetch('/api/customer/user_info/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'uid': this.uid})
        })
        .then((res) => res.json())
        .then((res) => {
          if (res['flag'] === global_.CONSTGET.SUCCESS) {
            let info = JSON.parse(res['message'])
            this.name = info.name
            this.age = info.age
            this.gender = info.gender
          }
        })
      }
    }
  }
</script>
<style scoped>
  .title {
    text-align: center;
  }
  .item {
    margin: 10% 0;
  }
</style>