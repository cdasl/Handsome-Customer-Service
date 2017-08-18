import Vue from 'vue'
import CustomerHistory from 'src/components/CustomerHistory.vue'
import 'whatwg-fetch'

describe('Test CustomerHistory', function () {
    this.timeout(5000)
    let vm = new Vue(CustomerHistory).$mount()
    it('Test cancel', () => {
        vm.cancel()
        expect(vm.show).not.to.be.ok
    })
    it("Test changePage", () => {
        vm.changePage(7)
        expect(vm.current).to.be.equal(7)
    })
})
