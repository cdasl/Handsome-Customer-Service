## 已将项目部署到服务器上了，测试地址: www.nkuhjp.com/hs.html 目前暂不支持聊天功能。
### 项目介绍

该项目是一个暑期实训项目，是一个面向企业的客服系统。

系统的整体框架为**Vue+Django**，前端为Vue的多页面，使用的是Django路由，前端没有提供路由。

此客服系统支持文字、表情、图片的发送，可以对页面进行截图；每次服务结束后用户可以对客服进行评分；客服也能选择转接用户给另一名客服；企业端有对客服服务情况的数据报表，并提供24小时内服务信息的统计图；除此之外我们引入了Python的ChatterBot机器人来为客服分担一部分任务，企业可以通过录入知识库来训练机器人。

### 效果图

1. #### 首页

   ![](https://raw.githubusercontent.com/dogloving/Handsome-Customer-Service/master/frontend/static/img/render1.png)

2. #### 企业注册页面

   ![](https://raw.githubusercontent.com/dogloving/Handsome-Customer-Service/master/frontend/static/img/render2.png)

3. #### 企业查看统计信息

   ![](https://raw.githubusercontent.com/dogloving/Handsome-Customer-Service/master/frontend/static/img/render3.png)

4. #### 企业管理客服

   ![](https://raw.githubusercontent.com/dogloving/Handsome-Customer-Service/master/frontend/static/img/render7.png)

5. #### 企业管理机器人知识库

   ![](https://raw.githubusercontent.com/dogloving/Handsome-Customer-Service/master/frontend/static/img/render4.png)

6. #### 客服和用户聊天(支持一个客服同时服务多个用户，还支持客服间的转接)

   ![](https://raw.githubusercontent.com/dogloving/Handsome-Customer-Service/master/frontend/static/img/render5.png)

   ![](https://raw.githubusercontent.com/dogloving/Handsome-Customer-Service/master/frontend/static/img/render6.png)

### 如何使用此项目

1.在你的Windows下安装

```bash
mysql, python3, npm, pip
```
2.打开`git bash`，执行
```bash
git clone git@github.com:dogloving/Handsome-Customer-Service.git
or
git clone https://github.com/dogloving/Handsome-Customer-Service.git
```
3.找到文件所在位置，打开`cmd`，执行
```bash
cd Group2
cd frontend
npm install
```
4.打开文件`frontend/node_modules/eslint-config-standard/eslintrc.json`, 如下编辑
```bash
globals: {
  "document": true,
  "navigator": false,
  "window": true,
  "fetch": true,
  "localStorage": true
}
```
```bash
"newIsCap": false
```
5.接第3步，执行
```bash
cd ..
pip install -r requirement.txt
```
6.在`frontend/dist/`下添加`upload`目录，在`frontend/static/`下添加`upload`目录

7.接第5步，执行
```bash
cd frontend
npm run build
```
8.创建一个`handsome`的账号，密码也为`handsome`。`root`账号需要将`customersystem`和`test_customersystem`的权限赋给`handsome`，然后在`handsome`账号下创建`customersystem`的数据库，方法为
```bash
create database customersystem default character set utf8 collate utf8_unicode_ci;
```
9.接第7步,执行
```bash
cd ..
python manage.py makemigrations
python manage.py migrate
```
10.复制`backend/data.py`中的代码，进入`Group2/`
```bash
git bash:  ./manage.py shell
or
cmd:  python manage.py shell
```
将代码复制进去，我们会为你在数据库中生成一些模拟数据;企业登录账号密码分别是`handsome@hs.com`和`handsome`，客服登录的账号密码分别是邮箱和`password`

11.依次执行
```bash
cd backend
python manage.py runserver 0:8000
```
在你的浏览器中打开 `http://localhost:8000` ; 如果失败了请关闭占用了8000端口的程序

12. 想了解更多可以查看项目wiki
