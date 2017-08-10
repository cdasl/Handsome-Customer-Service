<template>
  <div id="app">
    <Row>
        <Table border :columns="dialogForm" :data="dialogDataShow" ref="table"></Table>
        <Page :total="dialogData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
    <Button @click="add">添加数据</Button>
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
  export default {
    components: {Message},
    data () {
      return {
        show: false,
        content: '',
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
        dialogDataShow: [{
          startTime: new Date(),
          endTime: new Date(),
          uid: 'uid1',
          cid: 'cid',
          did: 'did1'
        }],
        current: 1,
        pageSize: 10
      }
    },
    methods: {
      showDialog (index) {
        this.$Message.success('fuck you')
        this.content = [
          {
            word: '你好',
            time: new Date(),
            self: true
          }, {
            word: '你好呀',
            time: new Date(),
            self: false
          }, {
            word: '请问能帮您吗',
            time: new Date(),
            self: true
          }, {
            word: '没有，快滚',
            time: new Date(),
            self: false
          }, {
            word: '你好',
            time: new Date(),
            self: true
          }, {
            word: '你好呀',
            time: new Date(),
            self: false
          }, {
            word: '请问能帮您吗',
            time: new Date(),
            self: true
          }, {
            word: '没有，快滚',
            time: new Date(),
            self: false
          }, {
            word: '你好',
            time: new Date(),
            self: true
          }, {
            word: '你好呀',
            time: new Date(),
            self: false
          }, {
            word: '请问能帮您吗',
            time: new Date(),
            self: true
          }, {
            word: '没有，快滚',
            time: new Date(),
            self: false
          }, {
            word: '你好',
            time: new Date(),
            self: true
          }, {
            word: '你好呀',
            time: new Date(),
            self: false
          }, {
            word: '请问能帮您吗',
            time: new Date(),
            self: true
          }, {
            word: '没有，快滚',
            time: new Date(),
            self: false
          }
        ]
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
      add () {
        let x = {
          startTime: String(Math.random()),
          endTime: new Date(),
          uid: 'uid' + Math.round(Math.random() * 100),
          did: 'did' + Math.round(Math.random() * 100)
        }
        console.log(x)
        this.dialogData.push(x)
        this.dialogDataShow = this.dialogData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.dialogData.length))
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