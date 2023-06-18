jQuery(document).ready(function() {

    $('.navi>li').mouseover(function() {
        $(this).find('.submenu').stop().slideDown(500)
    }).mouseout(function() {
        $(this).find('.submenu').stop().slideUp(500);
    });

    setInterval(function() {
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginLeft: -800});
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginLeft: -1600});
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginLeft: 0});
        $('.slidelist').delay(2000);
    });

    $(function() {
        $('.tabmenu>li>a').click(function() {
            $(this).parent().addClass("active")
            .siblings().removeClass("active");
        return false
        });
    });

    $(".notice li:first").click(function() {
        $('#layer').addClass("active");
    });
    $(".btn").click(function() {
        $('#layer').removeClass("active");
    });
});