import unittest
from canto_subtitle_cleaner.parse import segments, is_question

class TestParseFunctions(unittest.TestCase):

    def test_segments(self):
        self.assertEqual(segments(""), [])
        self.assertEqual(segments("！"), ["！"])
        self.assertEqual(segments("噉你係咪好開心？我都係咁諗！"), ["噉你係咪好開心？", "我都係咁諗！"])
        self.assertEqual(segments("為為為為為為為為揾揾揾揾揾揾揾"), ["為為為為為為為為揾揾揾揾揾揾揾"])

    def test_is_question(self):
        self.assertFalse(is_question("噉你係咪好開心？我都係咁諗！"))
        self.assertTrue(is_question("噉你係咪好開心？"))

if __name__ == "__main__":
    unittest.main()