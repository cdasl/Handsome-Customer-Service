<template>
  <div id="app">
    <Input v-model="customerEmail" class="email-input" placeholder="输入邮箱邀请客服"></Input>
    <Button @click="invite">邀请客服</Button>
    <Row>
        <Table border :columns="customerForm" :data="customerDataShow" ref="table"></Table>
        <Page :total="customerData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        customerEmail: '',
        customerForm: [
          {
            title: '姓名',
            key: 'name'
          }, {
            title: '邮箱',
            key: 'email'
          }, {
            title: '状态',
            key: 'state'
          }, {
            title: '服务总人数',
            key: 'serviced_number'
          }, {
            title: '当前服务人数',
            key: 'service_number'
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
                      this.logoff(params.index)
                    }
                  }
                }, '注销/激活')
              ])
            }
          }
        ],
        customerData: [],
        customerDataShow: [],
        current: 1,
        pageSize: 10
      }
    },
    methods: {
      init (iWantToChangePage) {
        if (iWantToChangePage) {
          this.current = 1
        }
        this.customerDataShow = this.customerData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.customerData.length))
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
        if (this.checkEmail(this.customerEmail) === false) {
          this.$Message.warning('邮箱错误')
        } else {
          let res = await this.fetchBase('/api/enter/invite/', {
            'email': this.customerEmail
          })
          if (res['flag'] === -10) {
            this.$Message.warning('改邮箱已被注册')
          } else if (res['flag'] === -11) {
            this.$Message.error('邀请失败')
          } else {
            this.customerData.push({
              name: res['message']['name'],
              email: res['message']['email'],
              state: res['message']['state'],
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
        let res = await this.fetchBase('/api/enter/reset/', {
          'cid': this.customerDataShow[index]['cid']
        })
        if (res['flag'] === -13) {
          this.$Message.warning('该客服不在数据库中')
        } else if (res['flag'] === 4) {
          this.$Message.error('操作失败')
        } else {
          let i = 0
          for (; i < this.customerData.length; ++i) {
            if (this.customerData[i].cid === this.customerDataShow[index].cid) {
              break
            }
          }
          this.customerData[i]['state'] = this.customerData[i]['state'] === -1 ? 1 : -1
          this.init(false)
        }
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
      let res = await this.fetchBase('/api/get_customers/', {})
      if (res['flag'] === -12) {
        this.$Message.error('客服人员获取失败')
      } else {
        for (let i = 0; i < res['message'].length; ++i) {
          this.customerData.push({
            name: res['message'][i]['name'],
            email: res['message'][i]['email'],
            state: res['message'][i]['state'],
            serviced_number: res['message'][i]['serviced_number'],
            service_number: res['message'][i]['service_number'],
            cid: res['message'][i]['cid']
          })
        }
        this.init(true)
      }
    }
  }
</script>
<style scoped>
.email-input {
  width: 30%;
  height: 5%;
}
</style>