<template>
  <div class="image">
    <img :src="address" @click="show" class="small">
    <Modal
      v-model="modal"
      :closable="false"
      class="img">
      <div slot="header"></div>
      <img :src="address" class="big">
      <div slot="footer"></div>
    </Modal>
  </div>
</template>
<script>
  export default {
    props: {
      address: {
        type: String
      }
    },
    data () {
      return {
        modal: false
      }
    },
    methods: {
      show () {
        this.modal = true
      }
    }
  }
</script>
<style>
.small {
  width: 75px;
  height: 75px;
}
.big {
  height: 100%;
  width: 100%;
}
.img {
  width: 60vw;
  height: 60vh;
}
.vertical-center-modal {
  display: flex;
  align-items: center;
  justify-content: center;
}
.vertical-center-modal .ivu-modal {
  top: 0;
}
.img .ivu-modal-body {
  padding: 0!important;
  line-height: 0!important;
}
.img .ivu-modal-header {
  display: none!important;
}
.img .ivu-modal-footer {
  display: none!important;
}
.img .ivu-modal {
  width: 50vw!important;
  margin-left: auto;
  margin-right: auto;
}
</style>