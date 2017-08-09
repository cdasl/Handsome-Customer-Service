<template>
  <div id="app">
    <Alert v-if="warn">
        <template slot="desc">{{ warnMes }}</template>
    </Alert>
    <Input v-model="customerEmail" class="email-input" placeholder="输入邮箱邀请客服"></Input>
    <Button @click="invite">邀请客服</Button>
    <Row>
        <Table border :columns="customerForm" :data="customerDataShow" ref="table"></Table>
        <Page :total="customerData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
    <Button @click="add">添加数据</Button>
    <Button @click="replace">替换</Button>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        warn: false,
        warnMes: '',
        customerEmail: '',
        customerForm: [
          {
            title: '姓名',
            key: 'name'
          },
          {
            title: '邮箱',
            key: 'email'
          },
          {
            title: '状态',
            key: 'state'
          },
          {
            title: '服务总人数',
            key: 'serviced_number'
          },
          {
            title: '当前服务人数',
            key: 'service_number'
          },
          {
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
        customerDataShow: [{
          name: 'Name',
          age: 45,
          address: 'Addr'
        }],
        current: 1,
        pageSize: 10
      }
    },
    methods: {
      warning (s) {
        this.warnMes = s
        this.warn = true
        setTimeout(() => { this.warn = false }, 2000)
        this.customerEmail = ''
      },
      checkEmail (email) {
        var ePattern = /^([A-Za-z0-9])+@([A-Za-z0-9])+\.([A-Za-z]{2,4})$/g
        return ePattern.test(email)
      },
      invite () {
        if (this.checkEmail(this.customerEmail) === false) {
          this.warning('邮箱错误')
        } else {
          fetch('/api/enter/invite/', {
            method: 'post',
            credentials: 'same-origin',
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken'),
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              'email': this.customerEmail
            })
          })
          .then((res) => res.json())
          .then((res) => {
            this.warning(res['message'])
            this.customerData.push(res['message'])
          })
        }
      },
      changePage (current) {
        this.current = current
        this.customerDataShow = this.customerData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.customerData.length))
      },
      logoff (index) {
        // pass
        console.log(this.customerDataShow[index]['cid'])
        fetch('/api/enter/logoff/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'cid': this.customerDataShow[index]['cid']})
        })
        .then((res) => res.json())
        .then((res) => {
          console.log(res['message'])
          this.customerDataShow[index]['state'] = -1
        })
      },
      remove (index) {
        this.customerData.splice(index, 1)
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
        this.customerData.push({
          name: String(Math.random()),
          age: 'age',
          address: 'dd'
        })
        this.customerDataShow = this.customerData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.customerData.length))
      },
      replace () {
        this.customerData = [{
          name: 'name',
          age: 4,
          address: 'dd'
        }]
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
    mounted () {
      console.log('fuck the world')
      fetch('/api/get_customers/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken'),
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'eid': 'test_eid'})
      })
      .then((res) => res.json())
      .then((res) => {
        console.log('what the fuck')
        console.log(res['message'])
        this.customerData = res['message']
        this.customerDataShow = this.customerData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.customerData.length))
      })
    }
  }
</script>
<style scoped>
.visible {
  display: block;
  height: 20%;
  visibility: visible;
}
.hidden {
  display: block;
  height: 20%;
  visibility: hidden;
}
.email-input {
  width: 30%;
  height: 5%;
}
</style>