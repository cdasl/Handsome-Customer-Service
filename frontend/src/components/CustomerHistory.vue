<template>
  <div id="app">
    <Row>
        <Table border :columns="dialogForm" :data="dialogDataShow" ref="table"></Table>
        <Page :total="dialogData.length" @on-change="changePage" :page-size="pageSize" style="margin-top:1vh;"></Page>
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
    props: {
      icon: {
        type: String
      }
    },
    data () {
      return {
        show: false,
        content: [],
        dialogForm: [
          {
            title: '开始时间',
            key: 'start_time'
          }, {
            title: '结束时间',
            key: 'end_time'
          }, {
            title: '用户ID',
            key: 'uid'
          }, {
            title: '操作',
            key: 'action',
            width: 200,
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
                      this.showDialog(params.index)
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
      showDialog (index) {
        fetch('/api/customer/dialog_msg/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({did: this.dialogDataShow[index]['did']})
        }).then((res) => res.json()).then((res) => {
          if (res['flag'] === global_.CONSTGET.DIALOGID_NOT_EXIST) {
            this.$Message.error(global_.CONSTSHOW.DIALOGID_NOT_EXIST)
            return
          }
          this.content.splice(0, this.content.length)
          for (let i = 0; i < res['message'].length; ++i) {
            let data = {}
            data['word'] = decodeURI(res['message'][i]['content'])
            // 判断消息是谁发送的
            data['self'] = res['message'][i]['isCustomer']
            data['time'] = res['message'][i]['date']
            data['src'] = data['self'] ? this.icon : '/static/js/emojiSources/huaji/1.jpg'
            this.content.push(data)
          }
          this.show = true
        })
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
      ok () {
        // pass
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
      }
    },
    mounted: function () {
      fetch('/api/customer/dialog_list/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then((res) => res.json()).then((res) => {
        if (res['flag'] === global_.CONSTGET.CID_NOT_EXIST) {
          this.$Message.error(global_.CONSTSHOW.CID_NOT_EXIST)
          window.location.replace('/customer_login/')
          return
        }
        for (let i = 0; i < res['message'].length; ++i) {
          this.dialogData.push({
            'start_time': res['message'][i]['start_time'].substring(0, 10) + ' ' + res['message'][i]['start_time'].substring(11, 16),
            'end_time': res['message'][i]['end_time'].substring(0, 10) + ' ' + res['message'][i]['end_time'].substring(11, 16),
            'uid': res['message'][i]['uid'],
            'did': res['message'][i]['did']
          })
        }
        this.dialogDataShow = this.dialogData.slice(0, Math.min(this.pageSize, this.dialogData.length))
      })
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
  height: calc(100% - 20px);
}
</style>