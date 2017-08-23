<template>
  <div class="layout" :class="{'layout-hide-text': spanLeft < 5}">
    <Row type="flex" class="row">
      <i-col :span="spanLeft" class="layout-menu-left">
        <Menu active-name="customer-talk" theme="dark" width="auto" @on-select="select" :class="leftClass">
          <div class="layout-logo-left"></div>
          <Menu-item name="customer-talk">
            <Icon type="chatbubble" :size="iconSize"></Icon>
            <span class="layout-text">当前会话</span>
          </Menu-item>
          <Menu-item name="customer-history">
            <Icon type="ios-analytics" :size="iconSize"></Icon>
            <span class="layout-text">历史会话</span>
          </Menu-item>
          <Menu-item name="customer-overview">
            <Icon type="document-text" :size="iconSize"></Icon>
            <span class="layout-text">信息统计</span>
          </Menu-item>
          <Menu-item name="customer-setting">
            <Icon type="settings" :size="iconSize"></Icon>
            <span class="layout-text">设置</span>
          </Menu-item>
        </Menu>
      </i-col>
      <i-col :span="spanRight">
        <div class="layout-header">
          <i-button type="text" @click="toggleClick">
            <Icon type="navicon" size="32"></Icon>
          </i-button>
          <i-select v-model="status" class="select" @on-change="changeStatus">
            <i-option value="2">休息</i-option>
            <i-option value="3">工作</i-option>
          </i-select>
          <Button type="text" class="logout" @click="logout">退出</Button>
        </div>
        <div :class="contentClass">
          <div class="layout-content-main" :is="type" @send="send" @swit="swit" @close="close" @transfer="transferCustomer" :content="currentcontent" :lists="lists" :name="name" :icon="icon" :uid="uid"></div>
        </div>
      </i-col>
    </Row>
    <Modal v-model="show" width="40vw" @on-ok="ok">
      <Select v-model="selected">
        <Option v-for="item in customerList" :key="item.cid" :value="item.cid">{{item.name}}</Option>
      </Select>
    </Modal>
  </div>
</template>
<script>
  import global_ from '../../components/Const'
  import CustomerTalk from '../../components/CustomerTalk'
  import CustomerSetting from '../../components/CustomerSetting'
  import CustomerHistory from '../../components/CustomerHistory'
  import CustomerOverview from '../../components/CustomerOverview'
  export default {
    components: {
      CustomerTalk,
      CustomerSetting,
      CustomerHistory,
      CustomerOverview
    },
    data () {
      return {
        leftClass: 'my-fixed',
        type: 'customer-talk',
        spanLeft: 5,
        spanRight: 19,
        content: {},
        socket: null,
        lists: [],
        currentcontent: [],
        status: '2',
        uid: '',
        cid: '',
        eid: '',
        name: '',
        icon: '',
        show: false,
        selected: '',
        customerList: [{
          name: '小明',
          cid: 'ccc'
        }, {
          name: '小光',
          cid: 'ddd'
        }],
        roboticon: '',
        contentClass: 'layout-content1'
      }
    },
    computed: {
      iconSize () {
        return this.spanLeft === 5 ? 14 : 24
      }
    },
    methods: {
      toggleClick () {
        if (this.spanLeft === 5) {
          this.spanLeft = 2
          this.spanRight = 22
          this.leftClass = 'my-fixed-shrink'
        } else {
          this.spanLeft = 5
          this.spanRight = 19
          this.leftClass = 'my-fixed'
        }
      },
      logout () {
        fetch('/api/customer/logout/', {
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
          } else {
            this.$Message.success('退出成功')
            window.location.replace('/customer_login/')
          }
        })
      },
      swit (item) {
        // 由于switch是js关键字 无法使用
        this.uid = item
        this.currentcontent = this.content[item]
        for (let i = 0; i < this.lists.length; ++i) {
          if (this.lists[i]['uid'] === item) {
            this.lists[i]['num'] = 0
            break
          }
        }
      },
      getCustomerList () {
        return fetch('/api/customer/get_other_online/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({data: ''})
        }).then((res) => res.json())
      },
      async transferCustomer () {
        let res = await this.getCustomerList()
        if (res['message'].length === 0) {
          /* global alert: true */
          alert('当前没有其他客服在线')
        } else {
          this.customerList = res['message']
          this.show = true
        }
      },
      getTransferCustomer () {
        this.socket.on('transfer customer', (msg) => {
          this.lists.unshift({'uid': msg['uid'], 'num': 0})
          this.uid = msg['uid']
          this.content[msg['uid']] = []
          for (let i = 0; i < msg['content'].length; ++i) {
            let data = this.getData(msg['content'][i])
            this.content[msg['uid']].push(data)
          }
          this.currentcontent = this.content[msg['uid']]
        })
      },
      changeStatus (curvalue) {
        if (curvalue === '2') {
          if (this.lists.length !== 0) {
            alert('还有客户在线，不可以休息')
            this.socket.emit('continue work', {data: 'true'})
          } else {
            this.socket.emit('customer rest', {cid: this.cid, eid: this.eid})
          }
        } else {
          this.connectServer()
        }
      },
      dateformat (date) {
        let seperator1 = '-'
        let seperator2 = ':'
        let month = date.getMonth() + 1
        let strDate = date.getDate()
        if (month >= 1 && month <= 9) {
          month = '0' + month
        }
        if (strDate >= 0 && strDate <= 9) {
          strDate = '0' + strDate
        }
        var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate + ' ' + date.getHours() + seperator2 + date.getMinutes() + seperator2 + date.getSeconds()
        return currentdate
      },
      send (msg) {
        let data = {}
        data['word'] = msg
        data['time'] = this.dateformat(new Date())
        data['self'] = true
        data['src'] = this.icon
        this.currentcontent.push(data)
        this.socket.emit('customer message', {data: encodeURI(msg), time: data['time'], cid: this.cid, uid: this.uid, src: encodeURI(data['src'])})
      },
      select (name) {
        if (name === 'customer-talk') {
          this.contentClass = 'layout-content1'
        } else if (name === 'customer-history') {
          this.contentClass = 'layout-content2'
        } else if (name === 'customer-overview') {
          this.contentClass = 'layout-content3'
        } else if (name === 'customer-setting') {
          this.contentClass = 'layout-content4'
        }
        this.type = name
      },
      ok () {
        if (this.selected !== '' && this.uid !== '') {
          this.socket.emit('transfer customer', {uid: this.uid, fromcid: this.cid, targetcid: this.selected})
          this.deleteUser()
        }
      },
      deleteUser () {
        for (let i = 0; i < this.lists.length; ++i) {
          if (this.uid === this.lists[i]['uid']) {
            this.lists.splice(i, 1)
            break
          }
        }
        delete this.content[this.uid]
        if (this.lists.length !== 0) {
          this.uid = this.lists[0]['uid']
          this.currentcontent = this.content[this.uid]
        } else {
          this.uid = ''
          this.currentcontent = []
        }
      },
      close (flag) {
        this.socket.emit('disconnect a user', {uid: this.uid, eid: this.eid, cid: this.cid})
        this.deleteUser()
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
      getInfo () {
        return fetch('/api/customer/get_info/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then((res) => res.json())
      },
      getData (msg) {
        let data = {}
        data['word'] = decodeURI(msg['data'])
        data['time'] = msg['time']
        data['self'] = msg['send'] !== this.uid
        if (data['self']) {
          data['src'] = msg['send'] === 'robot' ? this.roboticon : this.icon
        } else {
          data['src'] = '/static/js/emojiSources/huaji/10.jpg'
        }
        return data
      },
      newUser () {
        this.socket.on('new user', (msg) => {
          // 将新加入的用户放在列表中的第一位
          this.lists.unshift({'uid': msg['uid'], 'num': 0})
          this.uid = msg['uid']
          this.content[msg['uid']] = []
          for (let i = 0; i < msg['content'].length; ++i) {
            let data = this.getData(msg['content'][i])
            this.content[msg['uid']].push(data)
          }
          this.currentcontent = this.content[msg['uid']]
        })
      },
      myResponse () {
        this.socket.on('my response', (msg) => {
          let data = {}
          data['word'] = decodeURI(msg['data'])
          data['time'] = msg['time']
          data['self'] = false
          data['src'] = decodeURI(msg['src'])
          this.content[msg['uid']].push(data)
          // 生成未读消息数
          if (this.uid !== msg['uid']) {
            let i = 0
            for (i = 0; i < this.lists.length; ++i) {
              if (this.lists[i]['uid'] === msg['uid']) {
                this.lists[i]['num'] += 1
                console.log(this.lists[i]['num'])
                break
              }
            }
          }
        })
      },
      oldData () {
        this.socket.on('old data', (msg) => {
          for (let i = 0; i < msg['list'].length; ++i) {
            this.lists.push({'uid': msg['list'][i], 'num': 0})
            this.content[msg['list'][i]] = []
            this.uid = msg['list'][i]
            for (let j = 0; j < msg['content'][i].length; ++j) {
              let data = this.getData(msg['content'][i][j])
              this.content[msg['list'][i]].push(data)
            }
          }
          this.status = '3'
        })
      },
      customerAlive () {
        this.socket.on('customer alive', (msg) => {
          console.log('alive')
          this.socket.emit('customer alive', {cid: this.cid})
        })
      },
      userDisconnected () {
        this.socket.on('user disconnected', (msg) => {
          this.socket.emit('disconnect a user', {uid: msg['uid'], eid: this.eid, cid: this.cid})
          this.deleteUser()
        })
      },
      connectServer () {
        if (this.socket === null) {
          /* global location io: true */
          this.socket = io.connect('http://' + document.domain + ':' + location.port + '/test')
          this.socket.emit('a customer connected', {cid: this.cid, eid: this.eid})
          this.oldData()
          this.newUser()
          this.myResponse()
          this.userDisconnected()
          this.getTransferCustomer()
          this.customerAlive()
          this.socket.on('continue work', (msg) => {
            this.status = '3'
          })
        }
      }
    },
    created: async function () {
      let res = await this.getInfo()
      if (res['flag'] === global_.CONSTGET.CID_NOT_EXIST) {
        this.$Message.error(global_.CONSTSHOW.CID_NOT_EXIST)
        window.location.replace('/customer_login/')
        return
      }
      if (res['message']['state'] === 1) {
        window.location.replace('/customer_login/')
        return
      }
      this.cid = res['message']['cid']
      this.eid = res['message']['eid']
      this.name = res['message']['name']
      this.icon = res['message']['icon']
      this.status = (res['message']['state']).toString()
      this.roboticon = res['message']['roboticon']
    }
  }
</script>
<style scoped>
.row {
  display: flex;
  height: 100%;
}
.layout {
  border: 1px solid #d7dde4;
  background: #f5f7f9;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  min-height: 100%;
}
.layout-breadcrumb {
  padding: 10px 15px 0;
}
.layout-content1 {
  min-height: 680px;
  margin: 15px;
  margin-top: 75px;
  overflow: auto;
  background: #fff;
  border-radius: 4px;
}
.layout-content2 {
  min-height: 680px;
  margin: 15px;
  margin-top: 75px;
  overflow: auto;
  background: #fff;
  border-radius: 4px;
}
.layout-content3 {
  min-height: 680px;
  margin: 15px;
  margin-top: 75px;
  overflow: auto;
  background: #fff;
  border-radius: 4px;
}
.layout-content4 {
  min-height: 680px;
  margin: 15px;
  margin-top: 75px;
  overflow: auto;
  background: #fff;
  border-radius: 4px;
}
.layout-content-main {
  width: 100%;
  padding: 10px;
}
.layout-copy{
  text-align: center;
  padding: 10px 0 20px;
  color: #9ea7b4;
}
.layout-menu-left {
  background: #464c5b;
  position: relative;
}
.my-fixed {
  position: fixed;
  width: 20.87%!important;
  left: 0;
}
.my-fixed-shrink {
  position: fixed;
  width: 8.33%!important;
  left: 0;
}
.layout-header {
  position: fixed;
  width: 100%;
  height: 60px;
  background: #fff;
  box-shadow: 0 1px 1px rgba(0,0,0,.1);
  z-index: 100;
}
.layout-logo-left {
  width: 90%;
  height: 30px;
  background: #5b6270;
  border-radius: 3px;
  margin: 15px auto;
}
.layout-ceiling-main a {
  color: #9ba7b5;
}
.layout-hide-text .layout-text {
  display: none;
}
.ivu-col {
  transition: width .2s ease-in-out;
}
.select {
  position: absolute;
  right: 10%;
  width: 10%;
  top: 2vh;
  right: 30vw;
  z-index: 1000;
}
.logout {
  position: absolute;
  right: 0;
  top: 2vh;
  right: 23vw;
  z-index: 1000;
}
</style>