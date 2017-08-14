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
          <Menu-item name="4">
            <Icon type="cube" :size="iconSize"></Icon>
            <span class="layout-text">知识库</span>
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
          <i-select v-model="status" class="select">
            <i-option value="2">在线</i-option>
            <i-option value="3">休息</i-option>
          </i-select>
          <Button type="text" class="logout" @click="logout">退出</Button>
        </div>
        <div class="layout-content">
          <div class="layout-content-main" :is="type" @send="send" @swit="swit" @close="close" :content="currentcontent" :lists="lists"></div>
        </div>
      </i-col>
    </Row>
  </div>
</template>
<script>
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
        sid: '',
        cid: '',
        eid: ''
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
          window.location.replace('/customer_login/')
        })
      },
      swit (item) {
        // 由于switch是js关键字 无法使用
        this.sid = item
        this.currentcontent = this.content[item]
        for (let i = 0; i < this.lists.length; ++i) {
          if (this.lists[i]['sid'] === item) {
            this.lists[i]['num'] = 0
            break
          }
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
        data['src'] = '/static/js/emojiSources/huaji/1.jpg'
        this.currentcontent.push(data)
        this.socket.emit('customer message', {data: encodeURI(msg), time: data['time'], sid: this.sid, src: encodeURI(data['src'])})
      },
      select (name) {
        this.type = name
      },
      close (flag) {
        this.socket.emit('disconnect a user', {sid: this.sid, eid: this.eid})
        for (let i = 0; i < this.lists.length; ++i) {
          if (this.sid === this.lists[i]['sid']) {
            this.lists.splice(i, 1)
            break
          }
        }
        delete this.content[this.sid]
        if (this.lists.length !== 0) {
          this.sid = this.lists[0]['sid']
          this.currentcontent = this.content[this.sid]
        } else {
          this.sid = ''
          this.currentcontent = []
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
      },
      getCid () {
        return fetch('/api/customer/get_id/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then((res) => res.json())
      }
    },
    mounted: async function () {
      if (this.socket === null) {
          /* global location io: true */
        this.socket = io.connect('http://' + document.domain + ':' + location.port + '/test')
        let res = await this.getCid()
        this.cid = res['message']['cid']
        this.eid = res['message']['eid']
        this.socket.emit('a customer connected', {cid: this.cid})
        this.socket.on('customer connected', (msg) => {
          console.log(msg['data'])
        })
        this.socket.on('new user', (msg) => {
          // 将新加入的用户放在列表中的第一位
          this.lists.unshift({'sid': msg['sid'], 'num': 0})
          this.sid = msg['sid']
          this.content[msg['sid']] = []
          this.currentcontent = this.content[msg['sid']]
        })
        this.socket.on('my response', (msg) => {
          let data = {}
          data['word'] = decodeURI(msg['data'])
          data['time'] = msg['time']
          data['self'] = false
          data['src'] = decodeURI(msg['src'])
          this.content[msg['sid']].push(data)
          // 生成未读消息数
          if (this.sid !== msg['sid']) {
            let i = 0
            for (i = 0; i < this.lists.length; ++i) {
              if (this.lists[i]['sid'] === msg['sid']) {
                this.lists[i]['num'] += 1
                console.log(this.lists[i]['num'])
                break
              }
            }
          }
        })
      }
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
.layout-content {
  min-height: 1080px;
  margin: 15px;
  overflow: auto;
  background: #fff;
  border-radius: 4px;
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
  width: 20.88%!important;
  left: 0;
}
.my-fixed-shrink {
  position: fixed;
  width: 8.33%!important;
  left: 0;
}
.layout-header {
  height: 60px;
  background: #fff;
  box-shadow: 0 1px 1px rgba(0,0,0,.1);
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
  width: 7%;
  top: 1.5%;
}
.logout {
  position: absolute;
  right: 0;
  top: 1.5%;
}
</style>