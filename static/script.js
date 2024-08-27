$(document).ready(function(){

   $('#menu').click(function(){
    $(this).toggleClass('fa-times');
    $('.navbar').toggleClass('nav-toggle');
});
$(window).on('load scroll',function(){
    $('#menu').removeClass('fa-times');
    $('.navbar').removeClass('nav-toggle');

    if($(window).scrollTop() >0){
        $('header').addClass('sticky');
    }else{
        $('header').removeClass('sticky');
    }


    if($(window).scrollTop() >0){
        $('.scroll-top').show();
    }else{
        $('scroll-top').hide();
    }

    $('section').each(function(){
     let top = $(window).scrollTop();
     let offset = $(this).offset().top - 200;
     let id=$(this).attr('id');
     let height=$(this).height();

     if(top > offset && top < offset + height){
        $('.navbar a').removeClass('active');
        $('.navbar').find(`[href="#${id}"]`).addClass('active');
      }

    });

  });


  $('a[href*="#"]').on('click',function(e){

    $('html, body').animate({

      scrollTop : $($(this).attr('href')).offset().top,

    },
      500,
      'linear'
    );

  });

});


document.addEventListener('DOMContentLoaded', function() {
  const moreLink = document.getElementById('moreLink');
  const moreSubmenu = document.getElementById('moreSubmenu');

  moreLink.addEventListener('click', function(event) {
      
      event.preventDefault();
      
      moreSubmenu.classList.toggle('show');
  });
});

  document.addEventListener('DOMContentLoaded', function() {
    const profileImage = document.querySelector('.profile-image');
    profileImage.addEventListener('click', function() {
      window.location.href = "{{ url_for('profile') }}"; 
    });
  });