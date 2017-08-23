How to Access
==============
1. 登录企业后，在企业管理界面，点击 **设置**，会看到如下界面


.. image:: ../_static/capture.jpg
   :width: 65%


2. 在选择接入方式为 **内嵌** 的情况下，将代码复制在企业网页代码的 ``<script>`` 标签下


..

3. 效果如下

.. image:: ../_static/effect.jpg
   :width: 65%


A example
----------
以下为一个嵌入了客服系统的企业网页示例

::

  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>内嵌</title>
  </head>
  <body>
  <!-- 用户信息构造处，也可由企业获取到用户信息，然后将信息通过handsomeSendInfo传给客服系统，注意info需要是json格式 -->
    <script>
      let first = ['牛', '李', '马', '丁', '熊', '秦', '武']
      let second = ['大壮', '珍香', '寿生', '铁柱', '二妞', '狗蛋', '三宝']
      let user_info = {'info': JSON.stringify({'name': first[Math.floor(Math.random()*first.length)]+second[Math.floor(Math.random()*second.length)], 'age': Math.round(Math.random() * 50), 'gender': ['女','男'][Math.floor(Math.random()*2)]})}
      console.log(user_info)
    </script>
    <!-- 嵌入代码粘贴处 -->
    <script src="http://localhost:8000/static/js/template/oldBlank.js?eid=82a7ebc5f63e8c126767f4d0bf8c0ea8" id="handsomejs"></script>
  </body>
  </html>