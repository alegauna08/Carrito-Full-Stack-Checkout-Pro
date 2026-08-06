import unittest

from backend.api import CartRequest, CartItem, build_payment_payload, build_payment_response


class BuildPaymentPayloadTests(unittest.TestCase):
    def test_build_payment_payload_uses_items_and_price(self):
        request = CartRequest(items=[CartItem(song_id=1, quantity=2)])
        payload = build_payment_payload(request, [
            {"id": 1, "title": "Bohemian Rhapsody", "artist": "Queen"}
        ], "http://localhost:5173")

        self.assertEqual(payload["items"][0]["title"], "Bohemian Rhapsody")
        self.assertEqual(payload["items"][0]["quantity"], 2)
        self.assertEqual(payload["items"][0]["unit_price"], 30.0)
        self.assertEqual(payload["back_urls"]["success"], "http://localhost:5173")

    def test_build_payment_response_returns_preference_id(self):
        response = build_payment_response({"id": "pref_123", "init_point": "https://test.com/pay"}, "pk_test")

        self.assertEqual(response["preference_id"], "pref_123")
        self.assertEqual(response["init_point"], "https://test.com/pay")
        self.assertEqual(response["public_key"], "pk_test")


if __name__ == "__main__":
    unittest.main()
