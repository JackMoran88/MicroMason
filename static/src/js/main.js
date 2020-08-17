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
        $('section.dropdown__categories').css({'padding-top': $('nav.navbar').outerHeight()})

        //CART IMAGE
        console.log('resized')
        $('.card-image').height($('.card-image').width() * 1.1);
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
function getElementIndex(element) {
    return Array.from(element.parentNode.children).indexOf(element);
}

//CATALOG
$(document).ready(function () {
    //Нажатие на бургер
    $('#btn_burger').bind('click', function () {
        //Анимация бургера
        $(this).toggleClass("active")
        //Закрываем все подкатегории
        $('.category-sub').removeClass('active')
        //Убираем угол
        $('.category').removeClass('active')
        //Главная цель, отображение.
        $('#dropdown__categories').toggleClass("active")
    });

    //Срабатывание на клавиши
    $(document).on('keydown', function (event) {
        if (event.key == "Escape") {
            $('#btn_burger').removeClass('active')
            $('#dropdown__categories').removeClass('active')
        }
    });


    $('.dropdown__categories__inner .category  li').hover(function () {

        $('.category-sub').removeClass('active')
        $('.category').addClass('active')
        $('.category-sub').eq(getElementIndex(this)).addClass('active')
    })
    // console.log(category_hover)
})
//!CATALOG!