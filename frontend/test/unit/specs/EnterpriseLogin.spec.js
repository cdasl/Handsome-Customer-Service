import Vue from 'vue'
import EnterpriseLogin from 'src/components/EnterpriseLogin.vue'
import 'whatwg-fetch'

describe('Test EnterpriseLogin', function () {
    this.timeout(5000)
    let vm = new Vue(EnterpriseLogin).$mount()
    it('Test findEmail', () => {
        vm.findback.email = '123'
        expect(vm.findback.email).to.equal('123')
    })
    it('Test ok', () => {
        fetch('http://localhost:8000/api/reset_password', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': vm.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'email': '152@hh.com'})
        }).then((res) => res.json())
        .then((res) => {
            expect(res['message']).to.equal('enterprise_reset')
        })
    })
    it('Test warning', done => {
        vm.warning('test')
        expect(vm.warn).to.be.ok
        expect(vm.warnMes).to.be.equal('test')
        setTimeout(function() {
            expect(vm.warn).not.to.be.ok
            done()
        }, 2000);
    })
    it('Test reset', () => {
        vm.formItem.password = '161318313'
        vm.formItem.name = 'river tam'
        vm.reset()
        expect(vm.formItem.password).to.be.empty
        expect(vm.formItem.name).to.be.empty
    })
    it('Test submit', () => {
        fetch('http://localhost:8000/api/enter/login/', {
          method: 'post',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': vm.getCookie('csrftoken'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            'email': '152@hh.com',
            'password': 'guoqiang'
          })
        })
        .then((res) => res.json())
        .then((res) => {
            expect(res['message']).to.be.equal('Login Success!')
        })
    })
})
