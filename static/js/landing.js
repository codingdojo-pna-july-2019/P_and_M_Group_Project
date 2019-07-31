$(document).ready(function () {
  console.log('working in jquery');
  $(function () {
    $('button').click(function () {
      $.ajax({
        url: '/add_to_cart/product.id',
        success: function (response) {
          console.log(response);
        },
        error: function (error) {
          console.log(error);
        }
      });
    });
  });

})//document.ready