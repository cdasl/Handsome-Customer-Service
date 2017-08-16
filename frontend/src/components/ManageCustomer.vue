<template>
  <div id="app">
    <div class="head">
      <Input v-model="customerEmail" class="email-input" placeholder="输入邮箱邀请客服" @on-enter="invite"></Input>
      <Button @click="invite">邀请客服</Button>
      <Input v-model="searchWord" @on-enter="search" placeholder="输入ID,邮箱,姓名查找客服" class="search-input"></Input>
      <Button @click="search">查询</Button>
      <div class="head-right">
        <Select v-model="sortKeyWord" @on-change="changeSort" style="width:150px;text-align:left;">
          <Option v-for="item of sortList" :value="item" :key="item">{{ item }}</Option>
        </Select>
        <Select v-model="sortOrder" @on-change="changeSort" style="width:150px;text-align:left;">
          <Option v-for="item of orderList" :value="item" :key="item">{{ item }}</Option>
        </Select>
      </div>
    </div>
    <Row class="table">
        <Table border :columns="customerForm" :data="customerDataShow" ref="table"></Table>
        <Page :total="customerData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
    </div>
</template>
<script>
  import global_ from './Const'
  export default {
    data () {
      return {
        stateMap: {
          '-1': '已被注销',
          '0': '未激活',
          '1': '不在线',
          '2': '休息中',
          '3': '工作中'
        },
        sortList: ['按关键字排序', '状态', '服务总人数', '当前服务人数'], // 排序的所有关键字
        sortKeyWord: '按关键字排序', // 排序关键字
        sortOrder: '升序', // 升序或降序
        orderList: ['升序', '降序'],
        searchWord: '', // 搜索客服的关键词
        customerEmail: '', // 邀请客服输入的邮箱
        customerForm: [
          {
            'title': '客服ID',
            'key': 'cid_show'
          }, {
            'title': '姓名',
            'key': 'name'
          }, {
            'title': '邮箱',
            'key': 'email'
          }, {
            'title': '状态',
            'key': 'state'
          }, {
            'title': '用户平均评分',
            'key': 'avg_feedback',
            render: (h, params) => {
              return h('Rate', {
                props: {
                  value: params.row['avg_feedback'],
                  disabled: true,
                  showText: true
                }
              })
            }
          }, {
            'title': '服务总人数',
            'key': 'serviced_number'
          }, {
            'title': '当前服务人数',
            'key': 'service_number'
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
                      this.logoff(params.index)
                    }
                  }
                }, '注销/激活')
              ])
            }
          }
        ], // 客服表格格式
        customerDataAll: [], // 所有客服数据
        customerData: [], // 所有页面数据
        customerDataShow: [], // 当前页的客服数据
        current: 1, // 当前页码
        pageSize: 10 // 煤业数据条数
      }
    },
    methods: {
      init (iWantToChangePage) {
        // 根据当前情况将customerDataAll中的数据传给customerData和customerDataShow
        this.customerData = []
        if (this.searchWord.trim() === '') {
          this.customerData = this.customerDataAll
        } else {
          for (let i = 0; i < this.customerDataAll.length; ++i) {
            if (this.customerDataAll[i]['cid_show'].indexOf(this.searchWord) !== -1 ||
                this.customerDataAll[i]['name'].indexOf(this.searchWord) !== -1 ||
                this.customerDataAll[i]['email'].indexOf(this.searchWord) !== -1) {
              this.customerData.push(this.customerDataAll[i])
            }
          }
        }
        if (iWantToChangePage) {
          this.customerDataShow = this.customerData.slice(0, Math.min(this.pageSize, this.customerData.length))
          this.current = 1
        } else {
          this.customerDataShow = this.customerData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.customerData.length))
        }
      },
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
      checkEmail (email) {
        var ePattern = /^([A-Za-z0-9])+@([A-Za-z0-9])+\.([A-Za-z]{2,4})$/g
        return ePattern.test(email)
      },
      async invite () {
        // 检查邮箱格式并提交邀请
        if (this.checkEmail(this.customerEmail) === false) {
          this.$Message.warning('邮箱错误')
        } else {
          let res = await this.fetchBase('/api/enter/invite/', {
            'email': this.customerEmail
          })
          this.customerEmail = ''
          if (res['flag'] === global_.CONSTGET.MAILBOX_REGISTERED) {
            this.$Message.warning(global_.CONSTSHOW.MAILBOX_REGISTERED)
          } else if (res['flag'] === global_.CONSTGET.INVITE_FAILURE) {
            this.$Message.error(global_.CONSTSHOW.INVITE_FAILURE)
          } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
            window.location.href = '/enterprise/'
          } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
            this.customerDataAll.push({
              name: res['message']['name'],
              email: res['message']['email'],
              state: this.stateMap['' + res['message']['state']],
              service_number: res['message']['service_number'],
              serviced_number: res['message']['serviced_number'],
              cid: res['message']['cid']
            })
            this.init(true)
            this.$Message.success('邀请成功')
          }
        }
      },
      changePage (current) {
        this.current = current
        this.init(false)
      },
      async logoff (index) {
        // 注销或者重新激活客服
        if (this.customerDataShow[index]['state'] === 0) {
          this.$Message.error('操作失败')
          return
        }
        let res = await this.fetchBase('/api/enter/reset/', {
          'cid': this.customerDataShow[index]['cid']
        })
        if (res['flag'] === global_.CONSTGET.CUSTOMER_NOT_EXIST) {
          this.$Message.warning(global_.CONSTSHOW.CUSTOMER_NOT_EXIST)
        } else if (res['flag'] === global_.CONSTGET.FAIL_LOG_OFF) {
          this.$Message.error(global_.CONSTSHOW.FAIL_LOG_OFF)
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          let i = 0
          for (; i < this.customerDataAll.length; ++i) {
            if (this.customerDataAll[i].cid === this.customerDataShow[index].cid) {
              break
            }
          }
          this.customerDataAll[i]['state'] = this.customerDataAll[i]['state'] === this.stateMap['-1'] ? this.stateMap['1'] : this.stateMap['-1']
          this.init(false)
        }
      },
      search () {
        // 根据信息查找客服，支持模糊查询
        this.init(true)
        this.searchWord = ''
      },
      changeSort () {
        // 排序
        let key = ''
        if (this.sortKeyWord === '状态') {
          key = 'state'
        } else if (this.sortKeyWord === '服务总人数') {
          key = 'serviced_number'
        } else if (this.sortKeyWord === '当前服务人数') {
          key = 'service_number'
        } else if (this.sortKeyWord === '按关键字排序') {
          return
        }
        let num = 1
        if (this.sortOrder === '降序') {
          num = -1
        }
        this.customerData.sort((item1, item2) => {
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
        // 根据传入的type导出不同的数据
        let csv = '\ufeff'
        let keys = []
        let temp = this.customerDataAll
        if (type === 2) {
          temp = this.customerData
        }
        this.customerForm.forEach(function (item) {
          csv += '"' + item['title'] + '",'
          keys.push(item['key'])
        })
        csv = csv.replace(/,$/, '\n')
        temp.forEach(function (item) {
          keys.forEach(function (key) {
            csv += '"' + item[key] + '",'
          })
          csv = csv.replace(/,$/, '\n')
        })
        var blob = new window.Blob([csv], {
          type: 'text/csv,charset=UTF-8'
        })
        let csvUrl = window.URL.createObjectURL(blob)
        let a = document.createElement('a')
        a.download = '客服人员.csv'
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
      // 先获取所有客服列表
      let res = await this.fetchBase('/api/get_customers/', {})
      if (res['flag'] === global_.CONSTGET.ERROR) {
        this.$Message.error(global_.CONSTSHOW.ERROR)
      } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
        window.location.href = '/enterprise/'
      } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
        for (let i = 0; i < res['message'].length; ++i) {
          this.customerDataAll.push({
            'cid_show': res['message'][i]['cid'].substring(0, 5),
            'name': res['message'][i]['name'],
            'email': res['message'][i]['email'],
            'cid': res['message'][i]['cid'],
            'state': this.stateMap['' + res['message'][i]['state']],
            'service_number': res['message'][i]['service_number'],
            'serviced_number': res['message'][i]['serviced_number'],
            'avg_feedback': res['message'][i]['avg_feedback']
          })
        }
        this.init(true)
      }
    }
  }
</script>
<style scoped>
.email-input {
  width: 15%;
  height: 5%;
}
.search-input {
  width: 15%;
  height: 5%;
}
.table {
  margin-top: 2vh;
}
.head {
  display: block;
  width: 100%;
}
.head-left {
  display: inline-block;
  width: 35%;
}
.head-right {
  display: inline-block;
  position: absolute;
  right: 28px;
  width: 55%;
  text-align: right;
}
.head-right span {
  text-align: left;
}
</style>