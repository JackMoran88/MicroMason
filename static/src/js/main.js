$(document).ready(function () {
    // //Dropdown
$(".dropdown__content").hide(),
        $(".dropdown__btn").click(function () {
            $(this).siblings(".dropdown__content").slideToggle(),
                $(this).children(".fa").toggleClass(["fa-caret-right", "fa-caret-down"])
        })
// //!Dropdown

});