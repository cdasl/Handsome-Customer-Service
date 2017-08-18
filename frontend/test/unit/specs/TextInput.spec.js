import Vue from 'vue'
import TextInput from 'src/components/TextInput.vue'
import 'whatwg-fetch'

describe('Test TextInput', function () {
    this.timeout(5000)
    let vm = new Vue(TextInput).$mount()
    it('Test toggle', () => {
        expect(vm.emoji).to.be.ok
        vm.toggle()
        expect(vm.emoji).not.to.be.ok
    })
})
