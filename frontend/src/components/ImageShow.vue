<template>
  <div class="image">
    <img :src="address" @click="show" class="small">
    <Modal v-model="modal" class-name="vertical-center-modal">
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
<style scoped>
.small {
  width: 75px;
  height: 75px;
}
.big {
  height: 100%;
  width: 100%;
}
.vertical-center-modal {
  display: flex;
  align-items: center;
  justify-content: center;
}
.vertical-center-modal .ivu-modal {
  top: 0;
}
</style>