<template>
  <div class="list">
    <ul>
        <li v-for="(item,index) in lists" @click="swit(item, index)" :class="{ active: index === activeindex }">
          <Badge :count="item.num">
            <img class="avatar" width="30" height="30" :src="headIcons[index % 8]">
            <p class="name">{{ item.uid.substring(3, 6) }}</p>
          </Badge>
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
        activeindex: 0,
        headIcons: ['/static/js/emojiSources/huaji/1.jpg', '/static/js/emojiSources/huaji/8.jpg', '/static/js/emojiSources/huaji/9.jpg',
          '/static/js/emojiSources/huaji/11.jpg', '/static/js/emojiSources/huaji/12.jpg',
          '/static/js/emojiSources/huaji/18.jpg', '/static/js/emojiSources/huaji/19.jpg', '/static/js/emojiSources/huaji/22.jpg']
      }
    },
    methods: {
      swit (item, index) {
        this.activeindex = index
        this.$emit('swit', item['uid'])
      }
    }
  }
</script>
<style scoped >
.list li {
  padding: 12px 15px;
  border-bottom: 1px solid #292C33;
  cursor: pointer;
  transition: background-color 0.1s;
}
.list li:hover {
  background-color: rgba(255, 255, 255, 0.03);
}
.list li.active {
  background-color: rgba(255, 255, 255, 0.1);
}
.list .avatar,
.list .name {
  vertical-align: middle;
}
.list .avatar {
  border-radius: 2px;
}
.list .name {
  display: inline-block;
  margin: 0 0 0 15px;
}
</style>