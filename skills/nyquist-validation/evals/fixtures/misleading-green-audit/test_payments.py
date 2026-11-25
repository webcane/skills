import unittest
from payments import Payments

class PaymentTests(unittest.TestCase):
    def test_retry_status(self):
        api = Payments()
        self.assertEqual(api.post("same", 100)[0], 200)
        self.assertEqual(api.post("same", 100)[0], 200)

    @unittest.skip("concurrency harness not ready")
    def test_concurrent_retry(self):
        pass
