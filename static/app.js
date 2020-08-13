function form_sign_up() {
    new Vue({
        el: '#auth_test',
        data: {},
        created: function () {
            axios.get('/api/sign_up')
                .then(function (response) {
                    $('#auth_test').html(response.data)
                })
        }
    })
}



function form_sign_in() {
    new Vue({
        el: '#auth_test',
        data: {},
        created: function () {
            axios.get('/api/sign_in')
                .then(function (response) {
                    $('#auth_test').html(response.data)
                })
        }
    })
}