<template>
  <div class="layout" :class="{'layout-hide-text': spanLeft < 4}">
    <Row type="flex" class="row">
      <i-col :span="spanLeft" class="layout-menu-left">
        <Menu active-name="customer-talk" theme="dark" width="auto" @on-select="select">
          <div class="layout-logo-left"></div>
          <Menu-item name="customer-talk">
            <Icon type="ios-keypad" :size="iconSize"></Icon>
            <span class="layout-text">当前会话</span>
          </Menu-item>
          <Menu-item name="3">
            <Icon type="ios-analytics" :size="iconSize"></Icon>
            <span class="layout-text">历史会话</span>
          </Menu-item>
          <Menu-item name="4">
            <Icon type="cube" :size="iconSize"></Icon>
            <span class="layout-text">知识库</span>
          </Menu-item>
          <Menu-item name="CustomerSetting">
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
        </div>
        <div class="layout-content">
          <div class="layout-content-main" :is="type" @send="send" :content="currentcontent"></div>
        </div>
      </i-col>
    </Row>
  </div>
</template>
<script>
  import CustomerTalk from '../../components/CustomerTalk'
  import CustomerSetting from '../../components/CustomerSetting'
  export default {
    components: {
      CustomerTalk,
      CustomerSetting
    },
    data () {
      return {
        type: 'customer-talk',
        spanLeft: 4,
        spanRight: 20,
        content: [],
        socket: null,
        list: [],
        currentcontent: [],
        status: '2',
        sid: ''
      }
    },
    computed: {
      iconSize () {
        return this.spanLeft === 4 ? 10 : 24
      }
    },
    methods: {
      toggleClick () {
        if (this.spanLeft === 4) {
          this.spanLeft = 2
          this.spanRight = 22
        } else {
          this.spanLeft = 4
          this.spanRight = 20
        }
      },
      send (msg) {
        this.socket.emit('my broadcast event', {data: encodeURI(msg)})
      },
      select (name) {
        this.type = name
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
        let cid = ''
        fetch('api/get_cid/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then((res) => res.json()).then((res) => {
          cid = res['cid']
        })
        return cid
      }
    },
    mounted: function () {
      if (this.socket === null) {
          /* global location io: true */
        this.socket = io.connect('http://' + document.domain + ':' + location.port + '/test')
        this.socket.on('connected', (msg) => {
          this.sid = msg['sid']
        })
        this.socket.on('my response', (msg) => {
          let data = {}
          data['word'] = decodeURI(msg['data'])
          data['time'] = new Date()
          data['self'] = msg['sid'] === this.sid
          this.currentcontent.push(data)
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
  height: 100%;
}
.layout-breadcrumb {
  padding: 10px 15px 0;
}
.layout-content {
  min-height: 450px;
  margin: 15px;
  overflow: hidden;
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
  width: 100px;
  top: 1.5%;
}
</style>