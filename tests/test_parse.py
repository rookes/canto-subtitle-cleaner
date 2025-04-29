import unittest
from canto_subtitle_cleaner.parse import segments, is_question
from canto_subtitle_cleaner.clean import clean_subtitle

class TestParseFunctions(unittest.TestCase):

    def test_segments(self):
        self.assertEqual(segments(""), [])
        self.assertEqual(segments("！"), ["！"])
        self.assertEqual(segments("噉你係咪好開心？我都係咁諗！"), ["噉你係咪好開心？", "我都係咁諗！"])
        self.assertEqual(segments("為為為為為為為為揾揾揾揾揾揾揾"), ["為為為為為為為為揾揾揾揾揾揾揾"])

    def test_is_question(self):
        self.assertFalse(is_question("噉你係咪好開心？我都係咁諗！"))
        self.assertTrue(is_question("噉你係咪好開心？"))

    def testLinebreak(self):
        self.assertEqual(clean_subtitle("雖然話大家係親戚,不過,我哋其實只係遠房親戚,而佢哋就負責輪流照顧我。")
                         , "雖然話大家係親戚，不過\n我哋其實只係遠房親戚而佢哋就負責輪流照顧我")

if __name__ == "__main__":
    unittest.main()