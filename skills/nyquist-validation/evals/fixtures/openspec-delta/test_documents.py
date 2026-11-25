import unittest
from documents import can_delete, can_view

class DocumentTests(unittest.TestCase):
    def test_owner_can_delete(self):
        self.assertTrue(can_delete("owner"))

    def test_member_can_view(self):
        self.assertTrue(can_view("member"))
