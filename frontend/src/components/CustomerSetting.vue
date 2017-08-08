<template>
  <div>
    <h2>个人信息</h2>
    <hr class="hr">
    <Form :model="formItem" class="form" label-position="left" :label-width="80">
      <Form-item label="邮箱">
        <Input v-model="formItem.mail" class="input" disabled>
      </Form-item>
      <Form-item label="名称">
        <Input v-model="formItem.name" class="input">
      </Form-item>
      <Form-item label="头像">
        <img src="../assets/img/zhanhui.jpg" class="image">
      </Form-item>
      <Form-item>
        <Button type="primary">保存</Button>
      </Form-item>
    </Form>
    <h2>密码设置</h2>
    <hr class="hr">
    <Form :model="passwordItem" class="form" label-position="left" :label-width="80">
      <Form-item label="原密码">
        <Input v-model="passwordItem.oldpassword" class="input" placeholder="请输入原密码">
      </Form-item>
      <Form-item label="新密码">
        <Input v-model="passwordItem.newpassword" class="input" placeholder="请输入新密码">
      </Form-item>
      <Form-item label="确认新密码">
        <Input v-model="passwordItem.confirm" class="input" placeholder="确认新密码">
      </Form-item>
      <Form-item>
        <Button type="primary">提交</Button>
      </Form-item>
    </Form>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        getItem: {
          mail: '123456@qq.com',
          name: '张三',
          image: 'demo.png'
        },
        formItem: {
          mail: '123456@qq.com',
          name: '张三',
          image: 'demo.png'
        },
        passwordItem: {
          oldpassword: '',
          newpassword: '',
          confirm: ''
        }
      }
    }
  }
</script>
<style scoped>
  h2 {
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
    font-size: 16px;
  }
  .form {
    margin-left: 30px;
  }
  .hr {
    FILTER: alpha(opacity=100,finishopacity=0,style=3);
    width: 80%;
    color: #987cb9;
    size: 3;
    margin-bottom: 40px;
    margin-top: 20px;
  }
  .image {
    width: 75px;
    height: 75px;
  }
  .input {
    width: 300px;
  }
</style>