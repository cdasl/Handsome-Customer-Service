<template>
  <div id="app">
    <Row>
        <Table border :columns="dialogForm" :data="dialogDataShow" ref="table"></Table>
        <Page :total="dialogData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
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
  export default {
    components: {Message},
    data () {
      return {
        customerForm: [
          {
            title: '姓名',
            key: 'name'
          }, {
            title: '邮箱',
            key: 'email'
          }, {
            title: '服务过的人数',
            key: 'serviced_number'
          }, {
            title: '最后一次登陆时间',
            key: 'last_login'
          }
        ],
        customerData: [],
        show: false,
        content: [],
        dialogForm: [
          {
            title: '开始时间',
            key: 'startTime'
          }, {
            title: '结束时间',
            key: 'endTime'
          }, {
            title: '用户ID',
            key: 'uid'
          }, {
            title: '客服ID',
            key: 'cid'
          }, {
            title: '操作',
            key: 'action',
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
        ],
        dialogData: [],
        dialogDataShow: [],
        current: 1,
        pageSize: 10
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
      async test2 () {
        let x = await this.test1('/api/enter/dialogs/', {})
        console.log('2')
        console.log(x)
      },
      async showCustomerInfo (index) {
        let res = await this.fetchBase('/api/enter/customer_info/', {
          'cid': this.dialogDataShow[index].cid
        })
        if (res['flag'] > 0) {
          this.customerData = [{
            name: res['message']['name'],
            email: res['message']['email'],
            serviced_number: res['message']['serviced_number'],
            last_login: res['message']['last_login'],
            icon: res['message']['icon']
          }]
          this.showDialog(index)
        } else {
          this.$Message.error('信息获取失败')
        }
      },
      async showDialog (index) {
        let res = await this.fetchBase('/api/enter/dialog_message/', {
          'did': this.dialogDataShow[index].did
        })
        if (res['flag'] === -16) {
          this.$Message.warning('会话不存在')
        } else if (res['flag'] > 0) {
          this.content = []
          for (let i = 0; i < res['message'].length; ++i) {
            if (res['message'][i]['sid'] === this.dialogDataShow[index].cid) {
              console.log(res['message'][i]['icon'])
              this.content.push({
                'word': res['message'][i]['content'],
                'time': res['message'][i]['date'],
                'self': true,
                'src': this.customerData[0].icon
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
        }
        this.customerID = this.dialogDataShow[index].cid
        this.show = true
      },
      ok () {
        this.$Message.success('ok')
      },
      cancel () {
        this.show = false
      },
      changePage (current) {
        this.current = current
        this.dialogDataShow = this.dialogData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.dialogData.length))
      },
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: '原始数据'
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: '排序和过滤后的数据',
            original: false
          })
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
      let res = await this.fetchBase('/api/enter/dialogs/', {})
      if (res['flag'] > 0) {
        for (let i = 0; i < res['message'].length; ++i) {
          this.dialogData.push({
            startTime: res['message'][i]['start_time'],
            endTime: res['message'][i]['end_time'],
            uid: 'test_uid',
            cid: 'test_cid',
            did: res['message'][i]['did']
          })
        }
        this.current = 1
        this.pageSize = 10
        this.dialogDataShow = this.dialogData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.dialogData.length))
      } else if (res['flag'] === -12) {
        this.$Message.error('历史会话获取失败')
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
</style>