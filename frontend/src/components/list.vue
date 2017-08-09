<template>
  <div class="list">
    <ul>
      <li v-for="(item,index) in lists" @click="swit(item, index)">
        <img class="avatar" width="30" height="30">
        <p class="name">联系人名字</p>
      </li>
    </ul>
  </div>
</template>
<script>
  export default {
    props: {
      lists: {
        type: Array
      }
    },
    data () {
      return {
        activeindex: 0
      }
    },
    methods: {
      swit (item, index) {
        this.activeindex = index
        this.$emit('swit', item)
      }
    }
  }
</script>
<style scoped lang="less">
.list {
  li {
    padding: 12px 15px;
    border-bottom: 1px solid #292C33;
    cursor: pointer;
    transition: background-color .1s;
    &:hover {
      background-color: rgba(255, 255, 255, 0.03);
    }
    &.active {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
  .avatar, .name {
    vertical-align: middle;
  }
  .avatar {
    border-radius: 2px;
  }
  .name {
    display: inline-block;
    margin: 0 0 0 15px;
  }
}
</style>