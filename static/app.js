function form_sign_up() {
    new Vue({
        el: '#auth-modal',
        data: {},
        created: function () {
            axios.get('/api/sign_up')
                .then(function (response) {
                    $('#auth-modal').html(response.data)
                })
        }
    })
}



function form_sign_in() {
    new Vue({
        el: '#auth-modal',
        data: {
            sing_in : 'sing_in'
        },
        created: function () {
            axios.get('/api/sign_in')
                .then(function (response) {
                    $('#auth-modal').html(response.data)
                    // vm.sing_in = response.data
                })
        }
    })
}