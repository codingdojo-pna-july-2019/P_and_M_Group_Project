paypal.Buttons({
  createOrder: function(data, actions) {
    // Set up the transaction
    return actions.order.create({
      purchase_units: [{
        amount: {value: '0.01'}
      }]
    });
  }
}).render('#paypal-button-container');