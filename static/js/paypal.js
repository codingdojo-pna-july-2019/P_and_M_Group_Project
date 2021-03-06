paypal.Button.render({
  env: 'sandbox', // Or 'production'
  // Set up the payment:
  // 1. Add a payment callback
  payment: function(data, actions) {
    // 2. Make a request to your server
    return actions.request.post('/my-api/create-payment/').then(function(data) {
        // 3. Return res.id from the response
        return data.paymentID;
      });
  },
  // Execute the payment:
  // 1. Add an onAuthorize callback
  onAuthorize: function(data, actions) {
    // 2. Make a request to your server
    return actions.request.post('/my-api/execute-payment/', {
      paymentID: data.paymentID,
      payerID:   data.payerID
    })
      .then(function(res) {
        // 3. Show the buyer a confirmation message.
        window.location.replace(res.success);
       // console.log(res.success)
      });
  }
}, '#paypal-button');
