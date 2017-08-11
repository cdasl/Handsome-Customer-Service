<template>
  <div id="app">
    <Button @click="addQuestion" type="primary">添加问题</Button>
    <Select v-model="myCategory" style="width:200px" @on-change="changeCategory">
      <Option v-for="item of categoryList2" :value="item" :key="item">{{ item }}</Option>
    </Select>
    <Row>
        <Table border :columns="questionForm" :data="questionDataShow" ref="table"></Table>
        <Page :total="questionData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
    <Button @click="add">添加</Button>
    <Modal
      v-model="show"
      title="添加问题"
      @on-ok="submitQuestion"
      @on-cancel="cancel"
      width="45vw">
      <div class="add-question" v-if="show">
        <h4>问题:</h4>
        <textarea class="text-area" placeholder="输入问题" v-model="myQuestoin"></textarea>
        <h4>答案:</h4>
        <textarea class="text-area" placeholder="预设答案" v-model="myAnswer"></textarea>
        <h4>分类</h4>
        <Select v-model="currentCategory" style="width:200px">
          <Option v-for="item of categoryList" :value="item" :key="item">{{ item }}</Option>
        </Select>
        <h4>自定义分类</h4>
        <Input class="my-input" v-model="selfCategory"></Input><br>
      </div>
    </Modal>
    <Modal
      v-model="show2"
      title="修改问题"
      @on-ok="submitModify"
      @on-cancel="cancel"
      width="45vw">
      <div class="add-question" v-if="show2">
        <h4>问题:</h4>
        <textarea class="text-area" v-model="myQuestoin"></textarea>
        <h4>答案:</h4>
        <textarea class="text-area" v-model="myAnswer"></textarea>
        <h4>分类</h4>
        <Select v-model="currentCategory" style="width:200px">
          <Option v-for="item of categoryList" :value="item" :key="item">{{ item }}</Option>
        </Select>
      </div>
    </Modal>
  </div>
</template>
<script>
  export default {
    data () {
      return {
        myCategory: '全部问题', // 当前问题类别
        myQuestoin: '', // 添加问题的问题
        myAnswer: '', // 添加问题的答案
        currentCategory: '', // 添加问题的类别(select)
        selfCategory: '', // 添加问题的类别(自定义)
        categoryList: [], // 添加问题的类别列表
        categoryList2: ['全部问题'], // 问题列表
        show: false, // 显示添加问题
        show2: false, // 显示修改问题
        questionForm: [
          {
            title: '问题',
            key: 'question'
          }, {
            title: '答案',
            key: 'answer'
          }, {
            title: '类别',
            key: 'category'
          }, {
            title: '操作',
            key: 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.modify(params.index)
                    }
                  }
                }, '修改'),
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.remove(params.index)
                    }
                  }
                }, '删除')
              ])
            }
          }
        ], // 问题表格格式
        questionDataAll: [], // 所有问题
        questionData: [], // 当前类别所有问题
        questionDataShow: [{
          question: '为什么我有了奥特曼变僧器还是不能变僧？',
          answer: '你可能买了假货',
          category: '类别'
        }], // 当前显示的所有问题
        current: 1, // 页码
        pageSize: 10 // 每页的数据条数
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
      // 根据当前情况将questionDataAll中的数据传给questionData和questionDataShow
      init (iWantToChangePage) {
        if (this.myCategory === '全部问题') {
          this.questionData = this.questionDataAll
        } else {
          this.questionData = []
          for (let i = 0; i < this.questionDataAll.length; ++i) {
            if (this.questionDataAll[i].category === this.myCategory) {
              this.questionData.push(this.questionDataAll[i])
            }
          }
        }
        if (iWantToChangePage) {
          this.questionDataShow = this.questionData.slice(0, Math.min(this.pageSize, this.questionData.length))
          this.current = 1
        } else {
          this.questionDataShow = this.questionData.slice((this.current - 1) * this.pageSize, Math.min((this.current - 1) * this.pageSize + this.pageSize, this.questionData.length))
        }
      },
      changeCategory () {
        // 改变问题类别
        this.init(true)
      },
      add () {
        this.questionDataAll.push({
          question: Math.round(Math.random() * 100),
          answer: '答案',
          category: this.categoryList[Math.floor(Math.random() * this.categoryList.length)]
        })
        this.changeCategory()
      },
      submitQuestion () {
        // 提交添加问题
        if (this.currentCategory.trim() === '' && this.selfCategory.trim() === '') {
          this.$Message.warning('类别不能为空')
          return
        } else if (this.selfCategory.trim() !== '') {
          this.$Message.success('自定义')
        } else {
          this.$Message.success('下拉框')
        }
        this.questionDataAll.push({
          question: this.myQuestoin,
          answer: this.myAnswer,
          category: this.selfCategory.trim() === '' ? this.currentCategory : this.selfCategory
        })
        this.init(true)
      },
      submitModify () {
        // 提交修改问题
        for (let i = 0; i < this.questionDataAll.length; ++i) {
          if (this.questionDataAll[i].question === this.myQuestoin) {
            this.questionDataAll[i].answer = this.myAnswer
            this.questionDataAll[i].category = this.currentCategory
            break
          }
        }
        this.init(false)
        this.cancel()
      },
      addQuestion () {
        // 弹出添加问题模态框
        this.$Message.error('添加问题')
        this.show = true
        this.cancel()
      },
      cancel () {
        this.myQuestoin = ''
        this.myAnswer = ''
        this.currentCategory = ''
        this.selfCategory = ''
      },
      modify (index) {
        // 弹出修改问题模态框
        this.$Message.success('' + this.questionDataShow[index].question)
        this.myQuestoin = this.questionDataShow[index].question
        this.myAnswer = this.questionDataShow[index].answer
        this.currentCategory = this.questionDataShow[index].category
        this.show2 = true
      },
      remove (index) {
        // 提交删除问题
        this.$Message.success('' + this.questionDataShow[index].question)
        let qid = this.questionDataShow[index]
        let i = 0
        for (; i < this.questionDataAll.length; ++i) {
          if (this.questionDataAll[i] === qid) {
            break
          }
        }
        this.questionDataAll.splice(i, 1)
        this.init(false)
        // 发送请求删除该问题（欠一个）
      },
      changePage (current) {
        // 修改页码
        this.current = current
        this.init(false)
      },
      exportData (type) {
        if (type === 1) {
          this.$refs.table.exportCsv({
            filename: '原始数据'
          })
        } else if (type === 2) {
          this.$refs.table.exportCsv({
            filename: '排序和过滤后的数据',
            original: false
          })
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
      }
    },
    async mounted () {
      let res = await this.fetchBase('')
    }
  }
</script>
<style scoped>
.text-area {
  display: block;
  width: 80%;
  height: 25%;
}
.my-input {
  display: block;
  margin-bottom: 5px;
  width: 60%;
}
.add-question {
  margin: 20px auto;
  width: 45vw;
  height: 40vh;
  overflow: hidden;
  border-radius: 3px;
  .main {
    height: 100%;
    position: relative;
    overflow: hidden;
    background-color: white;
  }
  .text {
    position: absolute;
    width: 100%;
    bottom: 0;
    left: 0;
  }
  .message {
    height: ~'calc(100% - 160px)';
  }
}
</style>