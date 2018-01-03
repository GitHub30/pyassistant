import unittest
from assistant.piassistant import Assistant

class TestAssistant(unittest.TestCase):

    def test_1(self):
        a = Assistant()

        self.assertEqual(a,"")



if __name__ == "__main__":
    unittest.main()