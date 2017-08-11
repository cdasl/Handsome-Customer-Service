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
    <Select v-model="chartType" style="width:200px">
      <Option v-for="item in typeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
    </Select>
    <div>
      <schart :canvasId="canvasId"
        :type="chartType"
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
          'totalTime': 0,
          'totalMessage': 0,
          'totalDialog': 0,
          'totalServiced': 0,
          'totalOnline': 0,
          'todayDialog': 0,
          'avgDialogTime': 0,
          'avgMessages': 0
        }, // 统计信息
        chartType: 'bar', // 统计图类型
        canvasId: 'myCanvas', // 画图的id
        width: 800, // 统计图宽
        height: 400, // 统计图高
        data: [], // 统计图数据
        options: {
          title: ''
        }, // 统计图标题
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
        // 从后端获取统计图所需要的数据（欠一个）
        let urls = ['/api/enter/message_oneday/', '/api/enter/dialog_oneday/', '/api/enter/serviced_oneday/']
        let titles = ['过去24小时消息数统计', '过去24小时会话数统计', '过去24小时服务人数统计']
        let res = await this.fetchBase(urls[num - 1], {})
        if (res['flag'] === -12) {
          this.$Message.error('获取失败')
          return
        }
        this.data = []
        this.options.title = titles[num - 1]
        let currentHour = (new Date()).getHours()
        for (let i = 24; i > 0; --i) {
          let tmp = currentHour - i
          this.data.push({
            name: tmp > 0 ? tmp : tmp + 24,
            value: res['message'][23 - i]
          })
          console.log(res['message'][23 - i])
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
      // 先从后端获取需要的统计信息
      let res = await this.fetchBase('/api/enter/get_alldata/', {})
      if (res['flag'] === -12) {
        this.$Message.error('数据获取失败')
      } else {
        this.statics = res['message']
      }
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