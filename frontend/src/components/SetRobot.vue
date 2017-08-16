<template>
  <div id="app">
    <div class="head">
      <div class="head-left">
        <Button @click="addQuestion" type="primary">添加问题</Button>
        <Select v-model="myCategory" style="width:150px;text-align:left;" @on-change="changeCategory">
          <Option v-for="item of categoryList2" :value="item" :key="item">{{ item }}</Option>
        </Select>
      </div>
      <div class="head-right">
        <Select v-model="sortKeyWord" style="width:150px;text-align:left;" @on-change="changeSort">
          <Option v-for="item of sortList" :value="item" :key="item">{{ item }}</Option>
        </Select>
        <Select v-model="sortOrder" style="width:150px;text-align:left;" @on-change="changeSort">
          <Option v-for="item of orderList" :value="item" :key="item">{{ item }}</Option>
        </Select>
      </div>
    </div>    
    <Row class="table">
        <Table border :columns="questionForm" :data="questionDataShow" ref="table"></Table>
        <Page :total="questionData.length" @on-change="changePage" :page-size="pageSize"></Page>
    </Row>
    <br>
    <Button type="primary" size="large" @click="exportData(1)"><Icon type="ios-download-outline"></Icon> 导出原始数据</Button>
    <Button type="primary" size="large" @click="exportData(2)"><Icon type="ios-download-outline"></Icon> 导出排序和过滤后的数据</Button>
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
  import global_ from './Const'
  export default {
    data () {
      return {
        sortList: ['按关键字排序', '类别'], // 排序的所有关键字
        sortKeyWord: '按关键字排序', // 排序关键字
        sortOrder: '升序', // 升序或降序
        orderList: ['升序', '降序'],
        qid: '', // 问题id
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
            'title': '问题',
            'key': 'question'
          }, {
            'title': '答案',
            'key': 'answer'
          }, {
            'title': '类别',
            'key': 'category'
          }, {
            'title': '操作',
            'key': 'action',
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
        questionDataShow: [], // 当前显示的所有问题
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
      init (iWantToChangePage) {
        // 根据当前情况将questionDataAll中的数据传给questionData和questionDataShow
        if (this.myCategory === '全部问题') {
          this.questionData = this.questionDataAll
        } else {
          this.questionData = []
          for (let i = 0; i < this.questionDataAll.length; ++i) {
            if (this.questionDataAll[i]['category'] === this.myCategory) {
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
      async submitQuestion () {
        // 提交添加问题
        let cate = ''
        if (this.myQuestoin.trim() === '') {
          this.$Message.warning('问题内容不能为空')
          return
        }
        if (this.currentCategory.trim() === '' && this.selfCategory.trim() === '') {
          this.$Message.warning('类别不能为空')
          return
        } else if (this.selfCategory.trim() !== '') {
          cate = this.selfCategory.trim()
        } else {
          cate = this.currentCategory.trim()
        }
        let res = await this.fetchBase('/api/enter/set_robot_question/', {
          'question': this.myQuestoin,
          'answer': this.myAnswer,
          'category': cate
        })
        if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.error(global_.CONSTSHOW.ERROR)
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('添加成功')
          this.questionDataAll.push({
            'qid': res['message'],
            'question': this.myQuestoin,
            'answer': this.myAnswer,
            'category': this.selfCategory.trim() === '' ? this.currentCategory : this.selfCategory
          })
          this.init(true)
        }
      },
      async submitModify () {
        // 提交修改问题
        let i = 0
        for (i = 0; i < this.questionDataAll.length; ++i) {
          if (this.questionDataAll[i]['qid'] === this.qid) {
            break
          }
        }
        let res = await this.fetchBase('/api/enter/modify_question/', {
          'qid': this.questionDataAll[i]['qid'],
          'question': this.myQuestoin,
          'answer': this.myAnswer,
          'category': this.selfCategory === '' ? this.currentCategory : this.selfCategory
        })
        if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.error(global_.CONSTSHOW.ERROR)
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('修改成功')
          this.questionDataAll[i]['question'] = this.myQuestoin
          this.questionDataAll[i]['answer'] = this.myAnswer
          this.questionDataAll[i]['category'] = this.selfCategory === '' ? this.currentCategory : this.selfCategory
          this.init(false)
        }
        this.cancel()
      },
      addQuestion () {
        // 弹出添加问题模态框
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
        this.qid = this.questionDataShow[index]['qid']
        this.myQuestoin = this.questionDataShow[index]['question']
        this.myAnswer = this.questionDataShow[index]['answer']
        this.currentCategory = this.questionDataShow[index]['category']
        this.show2 = true
      },
      async remove (index) {
        // 提交删除问题
        let qid = this.questionDataShow[index]['qid']
        let i = 0
        for (; i < this.questionDataAll.length; ++i) {
          if (this.questionDataAll[i]['qid'] === qid) {
            break
          }
        }
        let res = await this.fetchBase('/api/enter/delete_question/', {
          'qid': this.questionDataShow[index]['qid']
        })
        if (res['flag'] === global_.CONSTGET.ERROR) {
          this.$Message.warning(global_.CONSTSHOW.ERROR)
        } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
          window.location.href = '/enterprise/'
        } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
          this.$Message.success('删除成功')
          this.questionDataAll.splice(i, 1)
          this.init(false)
        }
      },
      changePage (current) {
        // 修改页码
        this.current = current
        this.init(false)
      },
      changeSort () {
        // 排序
        let key = ''
        if (this.sortKeyWord === '类别') {
          key = 'category'
        } else if (this.sortKeyWord === '按关键字排序') {
          return
        }
        let num = 1
        if (this.sortOrder === '降序') {
          num = -1
        }
        this.questionData.sort((item1, item2) => {
          if (item1[key] > item2[key]) {
            return num
          } else if (item1[key] < item2[key]) {
            return -num
          } else {
            return 0
          }
        })
        this.init(true)
      },
      exportData (num) {
        let csv = '\ufeff'
        let keys = []
        let data = []
        if (num === 1) {
          data = this.questionDataAll
        } else if (num === 2) {
          data = this.questionData
        }
        this.questionForm.forEach(function (item) {
          csv += '"' + item['title'] + '",'
          keys.push(item['key'])
        })
        csv = csv.replace(/,$/, '\n')
        data.forEach(function (item) {
          keys.forEach(function (key) {
            csv += '"' + item[key] + '",'
          })
          csv = csv.replace(/,$/, '\n')
        })
        csv = csv.replace(/"null"/g, '""')
        var blob = new window.Blob([csv], {
          type: 'text/csv,charset=UTF-8'
        })
        let csvUrl = window.URL.createObjectURL(blob)
        let a = document.createElement('a')
        a.download = '知识库.csv'
        a.href = csvUrl
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
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
      // 获取所有问题信息，并收集所有类别
      let res = await this.fetchBase('/api/enter/get_all_question/', {})
      if (res['flag'] === global_.CONSTGET.ERROR) {
        this.$Message.error(global_.CONSTSHOW.ERROR)
      } else if (res['flag'] === global_.CONSTGET.EID_NOT_EXIST) {
        window.location.href = '/enterprise/'
      } else if (res['flag'] === global_.CONSTGET.SUCCESS) {
        this.questionDataAll = res['message']
        this.init(true)
        for (let i = 0; i < this.questionDataAll.length; ++i) {
          if (this.categoryList.indexOf(this.questionDataAll[i]['category']) === -1) {
            this.categoryList.push(this.questionDataAll[i]['category'])
            this.categoryList2.push(this.questionDataAll[i]['category'])
          }
        }
      }
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
.table {
  margin-top: 2vh;
}
.head {
  display: block;
  width: 100%;
}
.head-left {
  display: inline-block;
  width: 35%;
}
.head-right {
  display: inline-block;
  position: absolute;
  right: 28px;
  width: 55%;
  text-align: right;
}
</style>