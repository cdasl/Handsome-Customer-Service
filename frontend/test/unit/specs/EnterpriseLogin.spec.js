import Vue from 'vue'
import EnterpriseLogin from 'src/components/EnterpriseLogin.vue'
import 'whatwg-fetch'

describe('Test EnterpriseLogin', function () {
    this.timeout(5000)
    let vm = new Vue(EnterpriseLogin).$mount()
    it('Test findEmail', () => {
        vm.findEmail()
        expect(vm.findback.modal).to.be.ok
        vm.findEmail()
        expect(vm.findback.modal).not.to.be.ok
    })
    it('Test reset', () => {
        vm.formItem.password = '161318313'
        vm.formItem.email = 'rivertam@djsa.com'
        vm.reset()
        expect(vm.formItem.password).to.be.empty
        expect(vm.formItem.email).to.be.empty
    })
    it('Test trimItem', () => {
        vm.formItem.password = '161318313  '
        vm.findback.email = '16@sdf.com  '
        vm.trimItem()
        expect(vm.formItem.password).to.be.equal('161318313')
        expect(vm.findback.email).to.be.equal('16@sdf.com')
    })
})
