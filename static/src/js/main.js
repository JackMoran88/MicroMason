function getElementIndex(element) {
    return Array.from(element.parentNode.children).indexOf(element);
}

//Dropdown
$(document).ready(function () {
    $(".dropdown__content").hide(),
        $(".dropdown__btn").click(function () {
            $(this).siblings(".dropdown__content").slideToggle(),
                $(this).children(".fa").toggleClass(["fa-caret-right", "fa-caret-down"])
        })

});
//!Dropdown

//Отступ для контента от Header
$(document).ready(function () {
    new ResizeSensor($('nav.navbar'), function () {
        var win = $(window);
        $('div.page').css({'padding-top': $('nav.navbar').outerHeight()})
        $('section.categories').css({'padding-top': $('nav.navbar').outerHeight()})

        //CART IMAGE
        console.log('resized')
        $('.card__image').height($('.card__image').width() * 1.1);
        //

        if (win.width() <= 992) {
            if ($('.navbar-toggler').is(':visible')) {
                $('div.navbar-collapse').css({'padding-top': $('nav.navbar').outerHeight()})
            }
            else {
                $('div.navbar-collapse').css({'padding-top': 0})
            }
        }
        else {
            $('div.navbar-collapse').css({'padding-top': 0})
        }
    });


//    ПРИ СКРОЛИНГЕ
    $(window).scroll(function () {
        //Скрывать userline
        if ($(this).scrollTop() > 100) {
            $('.js-userline').addClass('hide')
        }
        if ($(this).scrollTop() < 80) {
            $('.js-userline').removeClass('hide')
        }
        //!Скрывать userline!
    });

})
//!Отступ для контента от Header


//CATALOG
$(document).ready(function () {
    //Нажатие на бургер
    $('#btn_burger').bind('click', function () {
        //Анимация бургера
        $(this).toggleClass("active")
        //Закрываем все подкатегории
        $('.categories__list_sub').removeClass('active')
        //Убираем угол
        $('.categories__list').removeClass('active')
        //Главная цель, отображение.
        $('#categories').toggleClass("active")
    });

    $('#categories').bind('click', function () {
        $('#btn_burger').removeClass('active')
        $('#categories').removeClass('active')
    })

    //Срабатывание на клавиши
    $(document).on('keydown', function (event) {
        if (event.key == "Escape") {
            $('#btn_burger').removeClass('active')
            $('#categories').removeClass('active')

            $('#js-input-search').blur()
            $('#js-input-search').val("");
        }
        if (event.keyCode >= 65 && event.keyCode <= 90 && !$('input').is(':focus')) {
            if (!$('#js-input-search').is(':focus')) {
                $('#js-input-search').focus().select();
            }
        }
    });


    $('.categories__content .categories__list  li').hover(function () {
        $('.categories__list_sub').removeClass('active')
        $('.categories__list').addClass('active')
        $('.categories__list_sub').eq(getElementIndex(this)).addClass('active')
    })
    //Если категория пуста, то при наведении, скрываю меню и делаю углы
    $('.categories__list-item.hide').hover(function () {
        console.log('hover')
        $('.categories__list').removeClass('active')
    })


    $(document).ready(function () {
        $(document).on('keydown', function (event) {


        });
    });
})
//!CATALOG!


// ANIMATION BURGER
$(document).ready(function () {
    $('#js-custom-toggler').on('click', function () {

        $('.animated-burger').toggleClass('open');
    });
});
// !ANIMATION BURGER!

