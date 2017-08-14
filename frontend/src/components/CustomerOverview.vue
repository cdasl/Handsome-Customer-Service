<template>
  <div class="app">
    <div class="item">
      <div class="title">
        <p>总服务时间</p>
      </div><hr>
      <div class="data">
        <span>{{ servicedTime }}min</span>
      </div>
    </div>
    <div class="item" @click="getChart(1)">
      <div class="title">
        <p>总消息数</p>
      </div><hr>
      <div class="data">
        <span>{{ messages }}条</span>
      </div>
    </div>
    <div class="item" @click="getChart(2)">
      <div class="title">
        <p>总会话数</p>
      </div><hr>
      <div class="data">
        <span>{{ dialogs }}次</span>
      </div>
    </div>
    <div class="item" @click="getChart(3)">
      <div class="title">
        <p>总服务人数</p>
      </div><hr>
      <div class="data">
        <span>{{ servicedPeople }}人</span>
      </div>
    </div>
    <div class="item">
      <div class="title">
        <p>今日会话数</p>
      </div><hr>
      <div class="data">
        <span>{{ todayDialogs }}次</span>
      </div>
    </div>
    <div class="item">
      <div class="title">
        <p>平均会话时长</p>
      </div><hr>
      <div class="data">
        <span>{{ timePerDialog }}min/次</span>
      </div>
    </div>
    <div class="item">
      <div class="title">
        <p>会话平均消息数</p>
      </div><hr>
      <div class="data">
        <span>{{ messagesPerDialog }}条/次</span>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        servicedTime: 0,
        messages: 0,
        dialogs: 0,
        servicedPeople: 0,
        onlineCustomers: 0,
        todayDialogs: 0,
        timePerDialog: 0,
        messagesPerDialog: 0
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
      },
      changeType (current) {
      }
    },
    mounted: function () {
      fetch('/api/customer/get_alldata/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'data': ''})
      }).then((res) => res.json()).then((res) => {
        this.servicedTime = res['message']['totalTime']
        this.messages = res['message']['totalMessage']
        this.dialogs = res['message']['totalDialog']
        this.servicedPeople = res['message']['totalServiced']
        this.todayDialogs = res['message']['todayDialog']
        this.timePerDialog = res['message']['avgDialogTime']
        this.messagesPerDialog = res['message']['avgMessages']
      })
    }
  }
</script>
<style scoped>
.app {
  width: 100%;
  overflow: auto;
}
.item {
  display: inline-block;
  width: 200px;
  height: 200px;
  margin-right: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 20px;
  box-shadow: 5px 5px 2px #888888;
}
.title {
  width: 200px;
  height: 80px;
}
.data {
  width: 200px;
  height: 120px;
}
.title p {
  width: 150px;
  font-size: 1.4em;
  line-height: 80px;
  margin-left: auto;
  margin-right: auto;
}
.item:hover {
  background-color: #ccc;
  cursor: pointer;
}
.data span {
  display: block;
  width: 120px;
  font-size: 1.8em;
  font-weight: bold;
  line-height: 100px;
  margin-left: auto;
  margin-right: auto;
  color: rgb(52, 101, 255);
}
</style>