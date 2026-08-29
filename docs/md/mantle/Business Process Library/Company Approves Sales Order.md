# Company Approves Sales Order

## Ideas to Incorporate

* Special case statuses and manual approval

## Story

Sales Orders are approved automatically when paid by credit card and CC authorization is successful.

Sales Orders are placed in Pending approval status after checkout then auto-approve once a third-party payment processor (PayPal, etc.) sends notification.

Sales Orders are placed in Rejected status when authorization fails.

Once order is approved Company reserves inventory for approved order, reducing Available To Promise (ATP) quantity. If inventory is not available negative inventory reservations are created and the order is placed on back-order.

Company sends confirmation email to the Placing Customer.
