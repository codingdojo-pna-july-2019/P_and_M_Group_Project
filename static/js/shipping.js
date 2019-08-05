$(document).ready(function() {
console.log('working in jquery');

$('#fn').keyup(delay(function(e){
  console.log('on keyup function');
  console.log('time elapsed!',this.value);
  $('.flash-messages').hide();
  if (this.value.length < 2){
    $('.fn').show();
  }
  if (this.value.length >=2 ){
    $('.fn').hide();
  }
}, 500));

$('#ln').keyup(delay(function(e){
  console.log('on keyup function');
  console.log('time elapsed!',this.value);
  $('.flash-messages').hide();
  if (this.value.length < 2){
    $('.ln').show();
  }
  if (this.value.length >=2 ){
    $('.ln').hide();
  }
}, 500));

$('#street1').keyup(delay(function(e){
  console.log('on keyup function');
  console.log('time elapsed!',this.value);
  $('.flash-messages').hide();
  if (this.value.length < 2){
    $('.street').show();
  }
  if (this.value.length >=2 ){
    $('.street').hide();
  }
}, 500));

$('#street2').keyup(delay(function(e){
  console.log('on keyup function');
  console.log('time elapsed!',this.value);
  $('.flash-messages').hide();
  if (this.value.length < 2){
    $('.street').show();
  }
  if (this.value.length >=2 ){
    $('.street').hide();
  }
}, 500));

$('#city').keyup(delay(function(e){
  console.log('on keyup function');
  console.log('time elapsed!',this.value);
  $('.flash-messages').hide();
  if (this.value.length < 2){
    $('.city').show();
  }
  if (this.value.length >=2 ){
    $('.city').hide();
  }
}, 500));

$('#state').keyup(delay(function(e){
  console.log('on keyup function');
  console.log('time elapsed!',this.value);
  $('.flash-messages').hide();
  if (this.value.length < 2){
    $('.state').show();
  }
  if (this.value.length >=2 ){
    $('.state').hide();
  }
}, 500));

$('#zip_code').keyup(delay(function(e){
  console.log('on keyup function');
  console.log('time elapsed!',this.value);
  $('.flash-messages').hide();
  if (this.value.length < 2){
    $('.zip_code').show();
  }
  if (this.value.length >=2 ){
    $('.zip_code').hide();
  }
}, 500));

function delay(callback, ms) {
  var timer = 0;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      callback.apply(context, args);
    }, ms || 0);
  };
}

})//document.ready