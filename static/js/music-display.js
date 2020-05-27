$(document).ready(function() {
    console.log("document ready");
    var state = false;

    function openNav() {
        document.querySelector(".main-sec ").style.marginLeft = "16rem ";
        document.querySelector("#side-nav ").style.width = "16rem ";
        document.querySelector("#main-cont_wrapper ").style.marginLeft = "16rem ";
        console.log("nav opened ");
    }

    function closeNav() {
        document.querySelector(".main-sec ").style.marginLeft = "0 ";
        document.querySelector("#side-nav ").style.width = "0 ";
        document.querySelector("#main-cont_wrapper ").style.margin = "auto ";
    }
    document.querySelector('#user-account').addEventListener('click', function(e) {
        e.preventDefault();
        toggleNav();
    });

    function toggleNav() {
        if (state == true) {
            openNav();
            state = false;
        } else {
            closeNav();
            state = true;
        }
    }
    console.log(window.innerWidth);
    if (window.innerWidth < 648) {
        state = false;
        toggleNav();
        console.log("closing nav ");
    }



    // $('div#play-audio').on('click', function() {

    //     let audi_player = '<audio controls autoplay><source src=' + $(this).attr('data-url') + ' type="audio/mpeg"/></audio>'

    //     $('.audio-player').show().append(audi_player);

    // });

});