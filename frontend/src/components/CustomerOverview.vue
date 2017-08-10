<template>
  <div class="app">
    <div class="item">
      <div class="title">
        <p>总服务时间</p>
      </div><hr>
      <div class="data">
        <span>89min</span>
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
    <h3>选择统计图形状<h3>
    <Select v-model="chartType" style="width:200px" @on-change="changeType">
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
        servicedTime: 45,
        messages: 998,
        dialogs: 56,
        servicedPeople: 34,
        onlineCustomers: 7,
        todayDialogs: 5,
        timePerDialog: 6,
        messagesPerDialog: 9,
        chartType: 'bar',
        canvasId: 'myCanvas',
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
      getChart (num) {
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