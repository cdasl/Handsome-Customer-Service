import Vue from 'vue'
import ManageCustomer from 'src/components/ManageCustomer.vue'
import 'whatwg-fetch'

describe('Test ManageCustomer', function () {
    this.timeout(5000)
    let vm = new Vue(ManageCustomer).$mount()
    it('Test checkEmail', () => {
        expect(vm.checkEmail('265@')).not.to.be.ok
        expect(vm.checkEmail('46464@dsa.com')).to.be.ok
    })
})
