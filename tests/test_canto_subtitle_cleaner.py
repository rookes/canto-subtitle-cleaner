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
        self.assertTrue(is_question("唔使，但我可唔可以跟埋嚟呀？"))
        self.assertTrue(is_question("我會唔會再見到佢嘎？"))
        self.assertFalse(is_question("乜你唔覺得我傻啊？"))

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
        self.assertEqual(clean_subtitle("你，你，你佢"), "你…你佢")
        self.assertEqual(clean_subtitle("同你你你佢"), "同你…佢")
        self.assertEqual(clean_subtitle("同你，你，你佢"), "同你…你佢")

        # 2 repetitions #for now
        #self.assertEqual(clean_subtitle("我我哋"), "我我哋")
        #self.assertEqual(clean_subtitle("我，我哋"), "我…我哋")
        #self.assertEqual(clean_subtitle("同我我哋"), "同我我哋")
        #self.assertEqual(clean_subtitle("同我，我哋"), "同我，我哋")

        #self.assertEqual(clean_subtitle("你你佢"), "你你佢")
        #self.assertEqual(clean_subtitle("你，你佢"), "你…佢")
        #self.assertEqual(clean_subtitle("同你你佢"), "同你你佢")
        #self.assertEqual(clean_subtitle("同你，你佢"), "同你，你佢")

    def test_乜_questions(self):
        self.assertEqual(clean_subtitle("乜你唔覺得我傻啊？"), "乜你唔覺得我傻呀？")
        self.assertEqual(clean_subtitle("乜嘢係代表我傻啊？"), "乜嘢係代表我傻啊？")
        self.assertEqual(clean_subtitle("乜都得，你係咪覺得我傻啊？"), "乜都得，你係咪覺得我傻啊？")

    def test_english_spacing(self):
        self.assertEqual(clean_subtitle("同 埋有陣時學,大家覺得好似係\nall or nothing,"), "同埋有陣時學，大家覺得好似係\nall or nothing")
        self.assertEqual(clean_subtitle("咁你就要走去Adobe\nIllustrator。"), "噉你就要走去Adobe\nIllustrator")
        
    def test_number_retention(self):
        self.assertEqual(clean_subtitle("呢個字體可以幫你完全,唔可以完全嘅,99.7％嘅時候,揀中呢一個"), "呢個字體可以幫你完全\n唔可以完全嘅，99.7%嘅時候，揀中呢一個")

    def test_chinese_numbers(self):
        self.assertEqual(clean_subtitle("一二三四五六七八九十"), "一二三四五六七八九十")
        self.assertEqual(clean_subtitle("十一月二十三號"), "11月23號")
        self.assertEqual(clean_subtitle("一月二十三號"), "1月23號")
        self.assertEqual(clean_subtitle("你二十三歲？一二三四五六七八九十"), "你23歲？一二三四五六七八九十")
        self.assertEqual(clean_subtitle("一二三四年果陣佢計咗數，「一二三」"), "1234年嗰陣佢計咗數，「一二三」")
        self.assertEqual(clean_subtitle("加埋一齊係四萬五千零一十蚊"), "加埋一齊係45010蚊")
        self.assertEqual(clean_subtitle("會活到一百零八歲"), "會活到108歲")

    def test_㗎咩(self):
        self.assertEqual(clean_subtitle("你覺得我難睇㗎嘛？"), "你覺得我難睇㗎咩？")

    def test_interjections(self):
        self.assertEqual(clean_subtitle("吓？？"), "")
        self.assertEqual(clean_subtitle("吼"), "")
        self.assertEqual(clean_subtitle("吓吼"), "吓吼")

if __name__ == "__main__":
    unittest.main()