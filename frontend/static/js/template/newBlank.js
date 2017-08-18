// 弹出新窗口模式

let src = document.getElementById('handsomejs').src
let temp = src.split('?')[src.split('?').length - 1]
let eid = temp.split('=')[temp.split('=').length - 1]
let uid = 'uid2' + Math.random().toString(36).substr(2)

function handsomeSendInfo () {
  // 将用户信息传给客服
  user_info.uid = uid
  fetch('http://localhost:8000/api/enter/send_user_info/', {
    method: 'post',
    credentials: 'same-origin',
    body: JSON.stringify(user_info)
  })
  .then((res) => res.json())
  .then((res) => {
    if ('message' in res) {
      console.log('用户信息发送成功')
    } else {
      console.log('用户信息发送失败')
    }
  })
}

function handsomeNewBlank () {
  // 页面添加iframe
  let a = document.createElement('a')
  a.href = 'http://localhost:8000/user/' + eid + '/' + uid
  a.target = '_blank'
  a.click()
  handsomeSendInfo()
}
let p = document.createElement('p')
p.style = 'display:inline-block;width:60%;height:7vh;line-height:7vh;margin:0;text-align:center;margin:0;font-size:1em;position:relative;top:-2.4vh;'
p.innerText = '咨询客服'
let img = document.createElement('img')
img.src = 'http://localhost:8000/static/img/icon.png'
img.style = 'display:inline-block;width:35%;height:100%;'
let btn = document.createElement('div')
btn.style = 'width:7vw;height:7vh;border:1px solid blue;background-color:#2d8cf0;position:fixed;right:0;bottom:20vh;margin-right:1vw;'
btn.onmouseover = () => {
  btn.style.backgroundColor = 'lightgreen'
  btn.style.cursor = 'pointer'
}
btn.onclick = function () {
  handsomeNewBlank()
}
btn.appendChild(img)
btn.appendChild(p)
document.body.appendChild(btn)