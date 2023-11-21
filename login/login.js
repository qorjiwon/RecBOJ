$(document).ready(function () {
    var errorMessage = $('.error-message');
    var user_id = $('#user_id');
    var submitButton = $('.submitButton');
    errorMessage.hide();
  
    $('.submitButton').on('click', function () {
      if (user_id.val() === '' || !user_id[0].checkValidity()) {
        errorMessage.show().text('ID를 입력해 주세요.');
        console.log("hay")
      } else {
        console.log("click");
        $('.login').addClass('loading').delay(2200).queue(function () {
          $(this).addClass('active');
          console.log("active");
        });
      }
    });
  });
  