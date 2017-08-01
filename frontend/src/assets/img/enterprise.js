let signup = document.getElementById('signup')
let login = document.getElementById('login')
let es = document.getElementById('enterprise-signup')
let el = document.getElementById('enterprise-login')
es.setAttribute('class', 'none')
signup.onclick = function () {
  es.setAttribute('class', 'show')
  el.setAttribute('class', 'none')
  alert('fuck')
}
login.onclick = function () {
  es.setAttribute('class', 'none')
  el.setAttribute('class', 'show')
}