<template class="body">
  <div class="layout" :class="{'layout-hide-text': spanLeft < 5}">
    <Row type="flex" class="row">
      <i-col :span="spanLeft" class="layout-menu-left">
        <Menu active-name="enterprise-overview" theme="dark" width="auto" @on-select="select" :class="leftClass">
          <div class="layout-logo-left"></div>
          <Menu-item name="enterprise-overview">
            <Icon type="ios-navigate" :size="iconSize"></Icon>
            <span class="layout-text">主页</span>
          </Menu-item>
          <Menu-item name="manage-customer">
            <Icon type="ios-keypad" :size="iconSize"></Icon>
            <span class="layout-text">客服管理</span>
          </Menu-item>
          <Menu-item name="history-dialog">
            <Icon type="ios-analytics" :size="iconSize"></Icon>
            <span class="layout-text">历史会话</span>
          </Menu-item>
          <Menu-item name="set-robot">
            <Icon type="cube" :size="iconSize"></Icon>
            <span class="layout-text">知识库</span>
          </Menu-item>
          <Menu-item name="enterprise-setting">
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
          <ul class="nav">
            <li><a @click="goHome">汉森首页</a></li>
            <li><a @click="goHelp">帮助中心</a></li>
            <li><a @click="showSub">{{ enterName }}</a><Icon type="arrow-down-b" color="#2d8cf0"></Icon></li>
          </ul>
          <Icon type="arrow-up-b" class="arrow-up" size="20" v-if="subShow"></Icon>
          <ul class="sub-list" v-if="subShow">
            <li>{{ enterName }}</li>
            <li><a @click="goCustomer">客服登录</a></li>
            <li><a @click="logout">退出登录</a></li>
          </ul>
        </div>
        <div :class="contentClass">
          <div class="layout-content-main"><div :is="type"></div></div>
        </div>
      </i-col>
    </Row>
  </div>
</template>
<script>
  import global_ from '../../components/Const'
  import ManageCustomer from '../../components/ManageCustomer'
  import EnterpriseSetting from '../../components/EnterpriseSetting'
  import EnterpriseOverview from '../../components/EnterpriseOverview'
  import HistoryDialog from '../../components/HistoryDialog'
  import SetRobot from '../../components/SetRobot'
  export default {
    components: {ManageCustomer, EnterpriseSetting, EnterpriseOverview, HistoryDialog, SetRobot},
    data () {
      return {
        contentClass: 'layout-content',
        leftClass: 'my-fixed',
        type: 'enterprise-overview',
        spanLeft: 5,
        spanRight: 19,
        enterName: '',
        subShow: false
      }
    },
    computed: {
      iconSize () {
        return this.spanLeft === 5 ? 14 : 24
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
      goHome () {
        // 前往首页
        window.location.href = '/'
      },
      goHelp () {
        // 前往帮助中心
        window.location.href = '/'
      },
      goCustomer () {
        // 前往客服登录页面
        fetch('/api/enter/logout/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({})
        })
        window.location.href = '/customer_login/'
      },
      showSub () {
        // 显示下拉菜单
        this.subShow = !this.subShow
      },
      logout () {
        // 退出登录
        fetch('/api/enter/logout/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({})
        })
        window.location.href = '/enterprise/'
      },
      toggleClick () {
        // 调整左侧栏样式
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
      select (name) {
        // 选择显示不同的子组件
        if (name === 'enterprise-setting') {
          this.contentClass = 'layout-content2'
        } else {
          this.contentClass = 'layout-content'
        }
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
      }
    },
    created () {
      // 先验证是否已经登录，防止直接输入网址进入管理界面
      fetch('/api/url_validate/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      })
      .then((res) => res.json())
      .then((res) => {
        if (res['flag'] === global_.CONSTGET.ERROR || res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        }
      })
    },
    async mounted () {
      // 获取企业信息
      let res = await this.fetchBase('/api/enter/enter_info/', {})
      if (res['flag'] === global_.CONSTGET.ERROR) {
        this.$Message.error('企业名获取失败')
      } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
        window.location.href = '/enterprise/'
      } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
        this.enterName = res['message']['name']
      }
    }
  }
</script>
<style>
.nav {
  text-align: right;
  height: 60px;
  line-height: 60px;
  padding-right: 100px;
  margin-top: -50px;
  margin-right: 250px;
}
.nav li {
  font-size: 1.2em;
  display: inline-block;
  margin-left: 10px;
}
.nav li a {
  margin-right: 3px;
}
.arrow-up {
  position: fixed!important;
  right: 4vw!important;
  top: 6.1vh!important;
}
.sub-list {
  width: 8vw;
  position: fixed;  
  right: 0.1vw;
  top: 8vh;
  background-color: white;
  box-shadow: 0 0 10px rgba(0,0,0,0.3);
}
.sub-list li {
  width: 8vw;
  height: 4vh;
  line-height: 4vh;
  text-align: center;
  font-size: 1.2em;
}
.sub-list li:hover {
  background-color: #FAFAFA;
  color: #2d8cf0;
  cursor: pointer;
}
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
  min-height: 800px;
  margin: 15px;
  margin-top: 75px;
  overflow: hidden;
  background: #fff;
  border-radius: 4px;
}
.layout-content2 {
  min-height: 1080px;
  margin: 15px;
  margin-top: 75px;
  overflow: hidden;
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
.layout-logo-left {
  width: 90%;
  height: 30px;
  background: #5b6270;
  border-radius: 3px;
  margin: 15px auto;
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
  position: fixed;
  width: 100%;
  height: 60px;
  background: #fff;
  box-shadow: 0 1px 1px rgba(0,0,0,.1);
  z-index: 100;
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
.m-logo {
  position: relative;
  width: 320px;
  height: 54px;
  padding: 0;
  font-size: 12px;
  color: #fff;
  line-height: 30px;
  background-color: #5294e0;
}
.logo {
  position: relative;
  left: 16px;
  display: inline-block;
  width: 300px;
  height: 50px;
  background: url('/static/img/tubiao.gif') no-repeat;
  background-position: left center;
  background-size: contain;
}
</style>