<template>
  <div class="app">
    <div class="item">
      <div class="title">
        <p>总服务时间</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['totalTime'] }}min</span>
      </div>
    </div>
    <div class="item" @click="getChart(1)">
      <div class="title">
        <p>总消息数</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['totalMessage'] }}条</span>
      </div>
    </div>
    <div class="item" @click="getChart(2)">
      <div class="title">
        <p>总会话数</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['totalDialog'] }}次</span>
      </div>
    </div>
    <div class="item" @click="getChart(3)">
      <div class="title">
        <p>总服务人数</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['totalServiced'] }}人</span>
      </div>
    </div>
    <div class="item">
      <div class="title">
        <p>在线客服人数</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['totalOnline'] }}人</span>
      </div>
    </div>
    <div class="item">
      <div class="title">
        <p>今日会话数</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['todayDialog'] }}次</span>
      </div>
    </div>
    <div class="item">
      <div class="title">
        <p>平均会话时长</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['avgDialogTime'] }}min/次</span>
      </div>
    </div>
    <div class="item">
      <div class="title">
        <p>会话平均消息数</p>
      </div><hr>
      <div class="data">
        <span>{{ statics['avgMessages'] }}条/次</span>
      </div>
    </div>
    <h3>选择统计图形状<h3>
    <Select v-model="chartType" style="width:200px" @on-change="changeType">
      <Option v-for="item in typeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
    </Select>
    <div>
      <schart :canvasId="canvasId"
        :type="type"
        :width="width"
        :height="height"
        :data="data"
        :options="options"
        class="chart"
      ></schart>
    </div>
  </div>
</template>
<script>
  import Schart from 'vue-schart'
  export default {
    components: {Schart},
    data () {
      return {
        statics: {
          'totalTime': 45,
          'totalMessage': 998,
          'totalDialog': 56,
          'totalServiced': 34,
          'totalOnline': 7,
          'todayDialog': 5,
          'avgDialogTime': 6,
          'avgMessages': 9
        },
        chartType: 'bar',
        canvasId: 'myCanvas',
        type: 'bar',
        width: 800,
        height: 400,
        data: [],
        options: {
          title: ''
        },
        typeList: [
          {
            label: '柱状图',
            value: 'bar'
          }, {
            label: '折线图',
            value: 'line'
          }
        ]
      }
    },
    methods: {
      fetchBase (url, body) {
        return fetch(url, {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(body)
        })
        .then((res) => res.json())
      },
      async getChart (num) {
        // let res = await this.fetchBase()
        this.data = []
        let currentHour = (new Date()).getHours()
        for (let i = 24; i > 0; --i) {
          let tmp = currentHour - i
          this.data.push({
            name: tmp > 0 ? tmp : tmp + 24,
            value: Math.round(Math.random() * 100)
          })
        }
        if (num === 1) {
          this.options.title = '过去24小时消息数统计'
        } else if (num === 2) {
          this.options.title = '过去24小时会话数统计'
        } else if (num === 3) {
          this.options.title = '过去24小时服务人数统计'
        }
      },
      changeType () {
        if (this.chartType === 'bar') {
          this.type = 'bar'
        } else {
          this.type = 'line'
        }
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
      }
    },
    async mounted () {
      let res = await this.fetchBase('/api/enter/get_alldata/', {})
      if (res['flag'] === -12) {
        this.$Message.error('数据获取失败')
        return
      }
      this.statics = res['message']
    }
  }
</script>
<style lang="">
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