  $(document).ready(function(){
    $('#postBtn').click(function(){
      var data = $('#shipping-form').serialize();
      $('#paramsSent').html(data);

      $.ajax({
        method: "POST",
        url: "/address_validation",
        data: data
      })
      .done(function(res){
         $('#return').html(res);
       });
    });
  });
  