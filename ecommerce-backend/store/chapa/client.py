import os
import uuid

class ChapaClient:
    """
    Minimal wrapper for initiating Chapa-like payments.
    For demo: returns fake payment URL and provider id.
    Replace with real HTTP calls when integrating.
    """
    def __init__(self):
        self.callback_url = os.getenv("CHAPA_CALLBACK_URL", "http://localhost:8000/api/payment/verify/")

    def create_payment(self, order_number, amount):
        # In production: call Chapa API to create payment
        provider_payment_id = str(uuid.uuid4())
        payment_url = f"https://checkout.chapa.example/pay/{provider_payment_id}"
        # return minimal structure
        return {"provider_payment_id": provider_payment_id, "payment_url": payment_url}
