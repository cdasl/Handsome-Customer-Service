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
        </div>
        <div class="layout-content">
          <div class="layout-content-main"><div :is="type"></div></div>
        </div>
      </i-col>
    </Row>
  </div>
</template>
<script>
  import ManageCustomer from '../../components/ManageCustomer'
  import EnterpriseSetting from '../../components/EnterpriseSetting'
  import EnterpriseOverview from '../../components/EnterpriseOverview'
  import HistoryDialog from '../../components/HistoryDialog'
  import SetRobot from '../../components/SetRobot'
  export default {
    components: {ManageCustomer, EnterpriseSetting, EnterpriseOverview, HistoryDialog, SetRobot},
    data () {
      return {
        leftClass: 'my-fixed',
        type: 'set-robot',
        spanLeft: 5,
        spanRight: 19
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
      select (name) {
        this.type = name
      }
    },
    created () {
      fetch('/api/url_validate/', {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      })
      .then((res) => res.json())
      .then((res) => {
        if (res['flag'] === -1) {
          // window.location.href = '/enterprise/'
        } else {
          console.log('成功')
        }
      })
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
  /* height: 100%; */
}
.layout-breadcrumb {
  padding: 10px 15px 0;
}
.layout-content {
  min-height: 1080px;
  margin: 15px;
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
</style>