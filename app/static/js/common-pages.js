"use strict";
$(document).ready(function() {
    // $('.theme-loader').addClass('loaded');
    $('.theme-loader').animate({
        'opacity': '0',
    }, 1200);
    setTimeout(function() {
        $('.theme-loader').remove();
    }, 2000);
    $('.preloader3').animate({
        'opacity': '0',
    }, 1200);
    setTimeout(function() {
        $('.preloader3').remove();
    }, 2000);
    // $('.pcoded').addClass('loaded');
});
