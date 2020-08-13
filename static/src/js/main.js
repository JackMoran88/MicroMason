$(document).ready(function () {
    // //Dropdown
    $(".dropdown__content").hide(),
        $(".dropdown__btn").click(function () {
            $(this).siblings(".dropdown__content").slideToggle(),
                $(this).children(".fa").toggleClass(["fa-caret-right", "fa-caret-down"])
        })
// //!Dropdown

});


MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var observer = new MutationObserver(function (mutations, observer) {
    // fired when a mutation occurs
    // console.log(mutations, observer);
    // ...
});

// define what element should be observed by the observer
// and what types of mutations trigger the callback
observer.observe(document, {
    subtree: true,
    attributes: true,
    childList: true,
    // attributeFilter: 'html',
});


//Отступ для контента от Header
$(document).ready(function () {
    $('div.wrapper').css({'padding-top': $('nav.navbar').outerHeight()})
    $('div.navbar-collapse').css({'padding-top': $('nav.navbar').outerHeight()})

    $(window).on('resize', function () {
        var win = $(this); //this = window
        $('div.wrapper').css({'padding-top': $('nav.navbar').outerHeight()})
        if (win.width() <= 991){
            $('div.navbar-collapse').css({'padding-top': $('nav.navbar').outerHeight()})
        }
        else{
            $('div.navbar-collapse').css({'padding-top': 0})
        }
    });
})
//!Отступ для контента от Header
