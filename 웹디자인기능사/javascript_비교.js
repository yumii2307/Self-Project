jQuery(document).ready(function() {

    // 메뉴 하나씩 내려오는 코드
    $('.navi>li').mouseover(function() {
        $(this).find('.submenu').stop().slideDown(500);
    }).mouseout(function() {
        $(this).find('.submenu').stop().slideUp(500);
    });

    // 메뉴 전체가 배경과 함께 내려오는 코드
    $('.navi>li').mouseover(function() {
        $('.submenu').stop().slideDown(500);
        $('#menu_bg').stop().slideDown(500);
    }).mouseout(function() {
        $('.submenu').stop().slideUp(500);
        $('#menu_bg').stop().slideUp(500); 
    })

    $('.navi>li').mouseover(function() {
        $('.submenu').stop().slideDown(500);
    }).mouseout(function() {
        $('.submenu').stop().slideUp(500);
    });

    // Fade-in, Fade-out
    $('.imgslide a:gt(0)').hide();
    setInterval(function() {
        $('.imgslide a:first-child')
        .fadeOut(1000)
        .next('a')
        .fadeIn(1000)
        .end()
        .appendTo('.imgslide');
    }, 3000);

    // 좌-우 슬라이드
    setInterval(function() {
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginLeft : -1200});
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginLeft : -2400});
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginLeft : 0});
        $('.slidelist').delay(2000);
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

    // 위-아래 슬라이드
    setInterval(function() {
        $('.slidelist').delay(1000);
        $('.slidelist').animate({marginTop: -300});
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginTop: -600});
        $('.slidelist').delay(2000);
        $('.slidelist').animate({marginTop: 0});
        $('.slidelist').delay(2000);
    });

    // 탭메뉴 전환
    $(function() {
        $('.tabmenu>li>a').click(function() {
            $(this).parent().addClass("active")
            .siblings().removeClass("active");
        return false;
        });
    });

    // 레이어
    $(".notice li:first").click(function() {
        $("#modal").addClass("active");
    });
    $(".btn").click(function() {
        $("#modal").removeClass("active");
    });

    // 
});