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
                         , "雖然話大家係親戚，不過\n我哋其實只係遠房親戚，而佢哋就負責輪流照顧我")
        
    def test_repeating_phrases(self):
        self.assertEqual(clean_subtitle("快啲啦快啲啦"), "快啲啦…")
        self.assertEqual(clean_subtitle("快啲啦，快啲啦"), "快啲啦…")

        self.assertEqual(clean_subtitle("唔好，唔好食"), "唔好，唔好食")
        self.assertEqual(clean_subtitle("唔好，唔好，食"), "唔好…食")
        
        self.assertEqual(clean_subtitle("快啲，快啲走"), "快啲，快啲走")
        self.assertEqual(clean_subtitle("快啲，快啲，快啲走"), "快啲…快啲走")

        self.assertEqual(clean_subtitle("大佬大佬大佬"), "大佬…")
        self.assertEqual(clean_subtitle("大佬大佬"), "大佬…")
        
        self.assertEqual(clean_subtitle("喂喂喂"), "喂…")
        self.assertEqual(clean_subtitle("喂喂"), "喂喂")
        self.assertEqual(clean_subtitle("喂喂喂？"), "喂…？")
        self.assertEqual(clean_subtitle("喂!喂！喂？"), "喂…？")

        self.assertEqual(clean_subtitle("停啊，停啊，"), "停啊…")
        self.assertEqual(clean_subtitle("靜㗎，靜㗎，"), "靜㗎…")
        
        self.assertEqual(clean_subtitle("佢…佢，佢好鍾意"), "佢…佢好鍾意")
        #self.assertEqual(clean_subtitle("啊，我哋，我哋想分手"), "我哋…我哋想分手")

    def test_repeated_characters_into_word(self):
        # 3 repetitions
        #self.assertEqual(clean_subtitle("我我我哋"), "我…我哋")
        #self.assertEqual(clean_subtitle("我，我，我哋"), "我…我哋")
        #self.assertEqual(clean_subtitle("同我我我哋"), "同我…我哋")
        #self.assertEqual(clean_subtitle("同我，我，我哋"), "同我…我哋")

        self.assertEqual(clean_subtitle("你你你佢"), "你…佢")
        self.assertEqual(clean_subtitle("你，你，你佢"), "你…佢")
        self.assertEqual(clean_subtitle("同你你你佢"), "同你…佢")
        self.assertEqual(clean_subtitle("同你，你，你佢"), "同你…佢")

        # 2 repetitions #for now
        self.assertEqual(clean_subtitle("我我哋"), "我我哋")
        self.assertEqual(clean_subtitle("我，我哋"), "我…我哋")
        self.assertEqual(clean_subtitle("同我我哋"), "同我我哋")
        self.assertEqual(clean_subtitle("同我，我哋"), "同我，我哋")

        self.assertEqual(clean_subtitle("你你佢"), "你你佢")
        self.assertEqual(clean_subtitle("你，你佢"), "你…佢")
        self.assertEqual(clean_subtitle("同你你佢"), "同你你佢")
        self.assertEqual(clean_subtitle("同你，你佢"), "同你，你佢")


    def test_(self):
        self.assertEqual(clean_subtitle("你覺得我難睇㗎嘛？"), "你覺得我難睇㗎咩？")

if __name__ == "__main__":
    unittest.main()