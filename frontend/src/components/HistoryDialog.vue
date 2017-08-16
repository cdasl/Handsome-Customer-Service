<template>
  <div id="app">
    <span>按关键字排序</span>
    <Select v-model="sortKeyWord" @on-change="changeSort" style="width: 200px;">
      <Option v-for="item of sortList" :value="item" :key="item">{{ item }}</Option>
    </Select>
    <Select v-model="sortOrder" @on-change="changeSort" style="width: 200px;">
      <Option v-for="item of orderList" :value="item" :key="item">{{ item }}</Option>
    </Select>
    <Row class="table">
        <Table border :columns="dialogForm" :data="dialogDataShow" ref="table"></Table>
        <Page :total="dialogData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData()"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Modal
        v-model="show"
        title="对话框"
        @on-ok="ok"
        @on-cancel="cancel"
        width="65vw">
        <div class="record" v-if="show">
          <div class="main">
            <message :content="content"></message>
            <h4 class="customer-info">客服信息</h4>
            <Table border :columns="customerForm" :data="customerData" ref="table"></Table>
          </div>
        </div>
    </Modal>
  </div>
</template>
<script>
  import Message from './Message'
  import global_ from './Const'
  export default {
    components: {Message},
    data () {
      return {
        sortList: ['', '开始时间', '结束时间', '用户ID', '客服ID'], // 排序的所有关键字
        sortKeyWord: '', // 排序关键字
        sortOrder: '升序', // 升序或降序
        orderList: ['升序', '降序'],
        customerForm: [
          {
            'title': '姓名',
            'key': 'name'
          }, {
            'title': '邮箱',
            'key': 'email'
          }, {
            'title': '服务过的人数',
            'key': 'serviced_number'
          }, {
            'title': '最后一次登陆时间',
            'key': 'last_login'
          }
        ], // 客服表格格式
        customerData: [], // 客服数据
        show: false, // 显示会话内容
        content: [], // 会话内容
        dialogForm: [
          {
            'title': '开始时间',
            'key': 'start_time'
          }, {
            'title': '结束时间',
            'key': 'end_time'
          }, {
            'title': '用户ID',
            'key': 'uid'
          }, {
            'title': '客服ID',
            'key': 'cid_show'
          }, {
            'title': '会话评分',
            'key': 'feedback',
            render: (h, params) => {
              return h('Rate', {
                props: {
                  value: params.row['feedback'],
                  disabled: true
                }
              })
            }
          }, {
            'title': '操作',
            'key': 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.showCustomerInfo(params.index)
                    }
                  }
                }, '点击查看')
              ])
            }
          }
        ], // 会话表格格式
        dialogData: [], // 会话内容
        dialogDataShow: [], // 当前页会话内容
        current: 1, // 当前页码
        pageSize: 10 // 每页展示数据条数
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
      init (iWantToChangePage) {
        // 根据当前情况将dialogData中的数据传给dialogDataShow
        if (iWantToChangePage) {
          this.current = 1
          this.dialogDataShow = this.dialogData.slice(0, Math.min(this.pageSize, this.dialogData.length))
        } else {
          this.dialogDataShow = this.dialogData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.dialogData.length))
        }
      },
      async showCustomerInfo (index) {
        // 根据客服id获取客服信息
        let res = await this.fetchBase('/api/enter/customer_info/', {
          'cid': this.dialogDataShow[index]['cid']
        })
        if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.customerData = [{
            'name': res['message']['name'],
            'email': res['message']['email'],
            'serviced_number': res['message']['serviced_number'],
            'last_login': res['message']['last_login'],
            'icon': res['message']['icon']
          }]
          this.showDialog(index)
        } else if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.error('信息获取失败')
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        }
      },
      async showDialog (index) {
        // 根据会话id获取会话内容
        let res = await this.fetchBase('/api/enter/dialog_message/', {
          'did': this.dialogDataShow[index]['did']
        })
        if (res['flag'] === global_.CONSTGET.DIALOGID_NOT_EXIST) {
          this.$Message.warning(global_.CONSTSHOW.DIALOGID_NOT_EXIST)
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.content = []
          for (let i = 0; i < res['message'].length; ++i) {
            if (res['message'][i]['sid'] === this.dialogDataShow[index]['cid']) {
              this.content.push({
                'word': res['message'][i]['content'],
                'time': res['message'][i]['date'],
                'self': true,
                'src': this.customerData[0]['icon']
              })
            } else {
              this.content.push({
                'word': res['message'][i]['content'],
                'time': res['message'][i]['date'],
                'self': false,
                'src': '/static/img/logo.jpg'
              })
            }
          }
          this.show = true
          this.customerID = this.dialogDataShow[index]['cid']
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        }
      },
      ok () {
        this.$Message.success('ok')
      },
      cancel () {
        this.show = false
      },
      changePage (current) {
        // 改变页码和显示的数据
        this.current = current
        this.dialogDataShow = this.dialogData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.dialogData.length))
      },
      changeSort () {
        // 排序
        let key = ''
        if (this.sortKeyWord === '开始时间') {
          key = 'start_time'
        } else if (this.sortKeyWord === '结束时间') {
          key = 'end_time'
        } else if (this.sortKeyWord === '客服ID') {
          key = 'cid'
        } else if (this.sortKeyWord === '用户ID') {
          key = 'uid'
        } else if (this.sortKeyWord === '') {
          return
        }
        let num = 1
        if (this.sortOrder === '降序') {
          num = -1
        }
        this.dialogData.sort((item1, item2) => {
          if (item1[key] > item2[key]) {
            return num
          } else if (item1[key] < item2[key]) {
            return -num
          } else {
            return 0
          }
        })
        this.init(true)
      },
      exportData (type) {
        let csv = '\ufeff'
        let keys = []
        this.dialogForm.forEach(function (item) {
          csv += '"' + item['title'] + '",'
          keys.push(item['key'])
        })
        csv = csv.replace(/,$/, '\n')
        this.dialogData.forEach(function (item) {
          keys.forEach(function (key) {
            csv += '"' + item[key] + '",'
          })
          csv = csv.replace(/,$/, '\n')
        })
        csv = csv.replace(/"null"/g, '""')
        var blob = new window.Blob([csv], {
          type: 'text/csv,charset=UTF-8'
        })
        let csvUrl = window.URL.createObjectURL(blob)
        let a = document.createElement('a')
        a.download = '历史会话.csv'
        a.href = csvUrl
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
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
      // 组件装载完成之后获取历史会话列表
      let res = await this.fetchBase('/api/enter/dialogs/', {})
      if (res['flag'] === global_.CONSTGET.SUCCESS) {
        for (let i = 0; i < res['message'].length; ++i) {
          this.dialogData.push({
            'start_time': res['message'][i]['start_time'],
            'end_time': res['message'][i]['end_time'],
            'cid': res['message'][i]['cid'],
            'did': res['message'][i]['did'],
            'uid': res['message'][i]['uid'],
            'cid_show': res['message'][i]['cid'].substring(0, 5),
            'feedback': res['message'][i]['feedback']
          })
        }
        this.init(true)
      } else if (res['flag'] === global_.CONSTGET.ERROR) {
        this.$Message.error('历史会话获取失败')
      } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
        window.location.href = '/enterprise/'
      }
    }
  }
</script>
<style scoped>
.btn {
  display: block;
  width: 10%;
  margin-top: 10px;
  margin-left: auto;
  margin-right: auto;
}
.modal {
  width: 65vw;
  height: 50vh;
}
.customer-info {
  margin: 3vh auto 1vh auto;
}
.record {
  margin: 20px auto;
  width: 60vw;
  height: 50vh;
  overflow: hidden;
  border-radius: 3px;
}
.record .main {
  height: 100%;
  position: relative;
  overflow: hidden;
  background-color: white;
}
.record .text {
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
}
.record .message {
  height: calc(100% - 160px);
}
.table {
  margin-top: 2vh;
}
</style>