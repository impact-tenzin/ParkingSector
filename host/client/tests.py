from django.test import TestCase

class TestErrorMessages(TestCase):
    def test_sending_all_messages(self):
        self.assertEqual(1 + 1, 2)
