import Vue from 'vue'
import EnterpriseSetting from 'src/components/EnterpriseSetting.vue'
import 'whatwg-fetch'

describe('Test EnterpriseSetting', function () {
    this.timeout(5000)
    let vm = new Vue(EnterpriseSetting).$mount()
    it('Test reset', () => {
        vm.password.old = 'hshshshs'
        vm.password.new = 'hshshshs'
        vm.password.newConfirm = 'ytytytyt'
        vm.reset()
        expect(vm.password.old).to.be.empty
        expect(vm.password.new).to.be.empty
        expect(vm.password.newConfirm).to.be.empty
    })
})
