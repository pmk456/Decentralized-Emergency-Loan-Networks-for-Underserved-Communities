import razorpay
class Payment:
    def __init__(self):
        self.client = razorpay.Client(auth=("rzp_test_DG2hG9ikul7Let", "1HFlHJ9BfGoPYe4zSLQ0w87u"))
    
    def create_payment(self, amount):
    
        data = {
                'currency': 'INR',
                'amount': amount
            }
        try:
            self.order_data = self.client.order.create(data)
        except Exception: raise
        return self.order_data['id']


    def verify_payment(self, order_id, payment_id, payment_signature):
        try:
            self.client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': payment_signature
            })
            return True
        except razorpay.errors.SignatureVerificationError:
            return False
