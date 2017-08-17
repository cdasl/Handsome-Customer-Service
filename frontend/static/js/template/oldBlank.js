// 弹出新窗口模式

let src = document.getElementById('handsomejs').src
let temp = src.split('?')[src.split('?').length - 1]
let eid = temp.split('=')[temp.split('=').length - 1]

function oldBlank () {
  // 页面添加iframe
  let uid = 'uid1' + Math.random().toString(36).substr(2)
  let href = 'http://localhost:8000/user/' + eid + '/' + uid
  let frame = document.createElement('iframe')
  frame.src = href
  frame.style = 'position:fixed;display:block;width:50vw;height:60vh;left:25vw;top:15vh;'
  frame.scrolling = 'no'
  frame.id = 'handsome-talk'
  document.body.appendChild(frame)
}
function remove () {
  // 页面删除iframe
  let tmp = document.getElementById('handsome-talk')
  if (tmp) {
    tmp.parentNode.removeChild(tmp)
  }
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
let show = false
btn.onclick = function () {
  if (show) {
    remove()
    p.innerText = '咨询客服'
    btn.style.backgroundColor = '#2d8cf0'
  } else {
    oldBlank()
    p.innerText = '关闭窗口'
    btn.style.backgroundColor = 'lightblue'
  }
  show = !show
}
btn.appendChild(img)
btn.appendChild(p)
document.body.appendChild(btn)