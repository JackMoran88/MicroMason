$(document).ready(function () {
    // //Dropdown
    $(".dropdown__content").hide(),
        $(".dropdown__btn").click(function () {
            $(this).siblings(".dropdown__content").slideToggle(),
                $(this).children(".fa").toggleClass(["fa-caret-right", "fa-caret-down"])
        })
// //!Dropdown

});


//Отступ для контента от Header
$(document).ready(function () {

    // $('div.page').css({'padding-top': $('nav.navbar').outerHeight()})

    if ($(window).width() <= 992) {
        console.log('<= 992')
        $('div.navbar-collapse').css({'padding-top': $('nav.navbar').outerHeight()})
    } else {
        console.log('> 992')
        $('div.navbar-collapse').css({'padding-top': 0})
    }

    new ResizeSensor($('nav.navbar'), function () {
        var win = $(window);
        $('div.page').css({'padding-top': $('nav.navbar').outerHeight()})

        //CART IMAGE
        console.log('resized')
        $('.card-image').height($('.card-image').width());
        //

        if (win.width() <= 992) {
            if ($('.navbar-toggler').is(':visible')) {
                $('div.navbar-collapse').css({'padding-top': $('nav.navbar').outerHeight()})
            }
        }
        else {
            $('div.navbar-collapse').css({'padding-top': 0})
        }
    });


})
//!Отступ для контента от Header
