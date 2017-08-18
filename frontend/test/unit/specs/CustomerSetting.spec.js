import Vue from 'vue'
import CustomerSetting from 'src/components/CustomerSetting.vue'
import 'whatwg-fetch'

describe('Test CustomerSetting', function () {
    this.timeout(5000)
    let vm = new Vue(CustomerSetting).$mount()
    it('Test reset', () => {
        vm.passwordItem.oldpassword = '2727527'
        vm.passwordItem.newpassword = '2727527'
        vm.passwordItem.confirm = '27272752'
        vm.reset()
        expect(vm.passwordItem.oldpassword).to.be.empty
        expect(vm.passwordItem.newpassword).to.be.empty
        expect(vm.passwordItem.confirm).to.be.empty
    })
})
