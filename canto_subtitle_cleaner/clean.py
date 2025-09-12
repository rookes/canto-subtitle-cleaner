"""Functions for cleaning a single Cantonese subtitle line."""
import re
import canto_subtitle_cleaner.parse as parse
from canto_subtitle_cleaner.parse import ZH, NOT_NUM
import canto_subtitle_cleaner.format as format

######################################## HELPER FUNCTIONS ########################################
def resub(text, pattern, repl):
    """Helper function to perform regex substitution."""
    
    return re.sub(pattern, repl, text)

def resub(text, regex_list):
    """Helper function to perform multiple regex substitutions."""
    
    for pattern, repl in regex_list:
        text = re.sub(pattern, repl, text)
    
    return text

####################################### PROCESS SUBTITLES #######################################
def standardize_chars_hk(text):
    regex_list = [
        ('爲', '為'),
        ('嬀', '媯'),
        ('僞', '偽'),
        ('潙', '溈'),
        ('蔿', '蒍'),
        ('搵', '揾'),
        ('溫', '温'),
        ('慍', '愠'),
        ('醞', '醖'),
        ('媼', '媪'),
        ('榲', '榅'),
        ('熅', '煴'),
        ('縕', '緼'),
        ('膃', '腽'),
        ('轀', '輼'),
        ('鰮', '鰛'),
        ('蒕', '蒀'),
        ('蘊', '藴'),
        ('氳', '氲'),
        ('兌', '兑'),
        ('說', '説'),
        ('脫', '脱'),
        ('稅', '税'),
        ('悅', '悦'),
        ('挩', '捝'),
        ('敓', '敚'),
        ('梲', '棁'),
        ('涗', '涚'),
        ('蛻', '蜕'),
        ('銳', '鋭'),
        ('閱', '閲'),
        ('㨂', '揀'),
        ('錬', '鍊'),
        ('床', '牀'),
        ('羣', '群'),
        ('裡', '裏'),
        ('麵', '麪'),
        ('敎', '教'),
        ('祕', '秘'),
        ('巿', '市'),
        ('衆', '眾'),
        ('潨', '潀'),
        ('溼', '濕'),
        ('鷄', '雞'),
        ('吿', '告'),
        ('汙', '污'),
        ('洩', '泄'),
        ('駡', '罵'),
        ('銹', '鏽'),
        ('鉤', '鈎'),
        ('衛', '衞'),
        ('蔥', '葱'),
        ('艷', '豔'),
        ('葯', '藥'),
        ('滙', '匯'),
        ('啟', '啓'),
        ('奬', '獎'),
        ('俾', '畀'),
        ('我地', '我哋'),
        ('你地', '你哋'),
        ('佢地', '佢哋'),
        ('人地', '人哋'),
        ('爹地', '爹哋'),
        ('妳', '你'),
        ('您', '你'),
        ('癐', '攰'),
        ('倆', '兩')
        
    ]
    return resub(text, regex_list)

def replace_standard_chinese(text):
    regex_list = [
        ('千萬別', '千祈唔好'),
        (r'(?<![天不毫虛可史])無(?![不敵依靠仇怨奈辜意上他倫價力助論窮言瑕限邪聊])', '冇'),
        (r'(?<![中兵出士打搭標目紅綠藍])的(?![士式水波確骰薂])', '嘅'),
        ('差不多', '差唔多'),
        ('不用', '唔使'),
        ('果陣', '嗰陣'),
        ('果啲', '嗰啲'),
        ('小鳥', '雀仔'),
        ('鳥仔', '雀仔'),
        (r'(?<![早熟瞌])睡(?![眠衣袍意袋鄉帽房夢椅相火])', '瞓'),
        ('昨天', '尋日'),
        ('明日', '聽日'),
        ('前天', '前日'),
        ('後天', '後日'),
        ('很好', '好好'),
        ('不要', '唔好'),
        ('這樣', '噉樣'),
        ('好不好', '好唔好'),
        ('好了', '好啦'),
        ('看來', '睇嚟'),
        ('出來', '出嚟'),
        (r'來[啦喇]', '嚟啦'),
        ('些', '啲'),
        ('昨日', '噚日'),
        ('就是', '就係'),
        ('躲埋', '匿埋'),
        ('躲', '匿'),
        (r'^難道', '唔通'),
        ('好久冇見', '好耐冇見'),
        (r'^沿着', '沿住'),
        (r'([好少咁噉常極太幾都乜別到])累', r'\1攰'),
        (r'([每][一]?)天', r'\1日'),
        ('唔好亂動', '唔好亂郁'),
        ('對不起', '對唔住'),
        ('抱唔住', '對唔住'),
        ('好細利', '好犀利'),
        ('慢住', '咪住'),
        ('閉嘴', '收聲'),
        ('肩膀', '膊頭')
    ]
    return resub(text, regex_list)

def clean_punctuation(text):
    regex_list = [
        (r'[\n\t]+', ' '), # Replace all line breaks and tabs with a space (to be removed later)
        (r'﹑', '\''), # restore normal apostrophe
        (r'([a-zA-Z])-([a-zA-Z])', r'\1\2'), # remove random hyphens
        (r'(?<![a-zA-Z])\s+(?![a-zA-Z])', ''), # remove spaces when not next to Latin characters
        (r'(?<=' + ZH + r')\s+', ''), # remove spaces next to Chinese characters
        (r'\s+(?=' + ZH + r')', ''),
        (r'\s+', ' '), # reduce all spaces to single space
        ('％', '%'), # Netflix standard uses half-width percent sign
        (r'\?', '？'),
        (r'\.\.\.', '…'),
        ('… ', '…'),
        (r'(' + NOT_NUM + r')[。.](' + NOT_NUM + r')', r'\1，\2'),
        (r'[。.]$', ''),
        (r'^[。.]', ''),
        (r'[!！]', '，'),
        (r',', '，'),
        (r'^，', ''),
        (r'，$', ''),
        (r'([，？…])[，？…]+', r'\1') # remove repeated punctuation
    ]

    return resub(text, regex_list)

def clean_question_final_particles(text):
    # Smart replacement of final particles based on question context
    segments = parse.segments(text)

    def _update_segment(s):
        if s == '':
            return s

        has_question_mark = s[-1] == '？'
        
        if parse.is_question(s):        # has question mark and question word
            s = s.replace('呀', '啊')
            s = s.replace('嘎', '㗎')
            s = s.replace('啫？', '唧？')

            # 啊 -> 呀 in cases like "乜你覺得唔開心啊？"
            if s[0] == '乜' and s[1] != '嘢':
                s = s.replace('啊？', '呀？')
        elif has_question_mark:         # has question mark and no question word
            s = s.replace('㗎？','嘎？')
            s = s.replace('啊？','呀？')
        else:                           # no question mark and no question word
            s = s.replace('呀', '啊')
            s = s.replace('嘎', '㗎')
        
        return s

    segments = map(_update_segment, segments)
    text = ''.join(segments)

    regex_list = [
        (r'(?<![，。！!?.;？；…])係咪(?=[呀啊吖？])', '，係咪'), # add comma to tag question 係咪
        (r'[㗎喇]㗎', '㗎'),
        (r'嘅？', '𠸏？'),
        ('啦啦聲', '嗱嗱聲'),
        (r'([啊喎喇啦㗎咋噃嘛嗎])(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', r'\1，'), #Add comma after final particles
        (r'^啊…', '') # Remove isolated 啊…
    ]

    text = resub(text, regex_list)

    return text

def clean_subtitle_misc(text):
    # Add a comma before or after certain words    
    regex_list_commas = [
        (r'(?<![？！，…])(?<!^)(?<![？！，…之])但係(?![，！？])', r'，但係'),
        (r'(?<![？！，])(?<!^)(?<![之只])不過(?![，！？])', r'，不過'),
        (r'(?<![？！，])(?<!^)雖然(?![，！？])', r'，雖然'),
        (r'(?<![？！，哋咁噉你佢我])(?<!^)首先(?![，！？])', r'，首先'), 
        (r'(?<![？！，])(?<!^)嘅話(?![…，！？])', r'嘅話，')
    ]

    # Misc changes for conventions
    regex_list_misc = [
        (r'咁(?![多耐濟滯細大靚高簡廣厚短瘦長少痛遲慘啱快難美遠容犀重脆硬蠢嚴奇荒熟遙弱辛平粗清慢心矮叻臭嘈悶])', '噉'),
        (r'(?<![\u4e00-\u9fff])咁(?=[多耐濟滯細大靚高簡廣厚短瘦長少痛遲慘啱快難美遠容犀重脆硬蠢嚴奇荒熟遙弱辛平粗清慢心矮叻臭嘈悶]啲)', '噉，'),
        (r'噉(' + ZH + ZH + r')嘅', r'咁\1嘅'),
        (r'噉(認真|緊張|困難|容易)', r'咁\1'), # change to 咁 before specific 2-char adjectives
        (r'([冇幾])噉', r'\1咁'),
        ('噉上下', '咁上下'),
        (r'(?<![譯原])著(?![述名作])', '着'),
        (r'(?<![空])翻(?![身閲轉譯一二兩三四五六七八九十百千萬數])', '返'),
        (r'(?<![\d一二兩三四五六七八九十百千萬數呢嗰])番(?![\d一二兩三四五六七八九十百千萬數心])', '返'),
        (r'[哂曬]', '晒'),
        (r'(?<![曝沖])晒(?=[招馬衫命乾張蓆])', '曬'),
        (r'晒(?=太陽|水艇|雨淋|月光|相舖)', '曬'),
        (r'(?<=[睇諗試求])吓', '下'),
        # ('只不過', '之不過'),
        (r'(?<!，)之不過(?!，)', '之不過，'),
        (r'[姐唧啫]係', '即係'),
        ('宜家', '而家'),
        (r'黎$', '嚟'),
        (r'黎([？！，…\n])', r'嚟\1'),
        (r'黎([\u4e00-\u9fff][？！，…\n])', r'嚟\1'),
        (r'^難道', '唔通'),
        ('傾計', '傾偈'),
        (r'傾([\u4e00-\u9fff])計', r'傾\1偈'),
        ('日圓', '円')
    ]
    
    # Fix Misc Cantonese errors
    regex_list_cantonese_errors = [
        ('喺到', '喺度'),
        ('呢到', '呢度'),
        ('嗰到', '嗰度'),
        ('割到', '嗰度'),
        (r'([係答])岩', r'\1啱'),
        ('講得岩', '講得啱'),
        ('係呢邊', '喺呢邊'),
        ('係呢度', '喺呢度'),
        ('係呢個時候', '喺呢個時候'),
        ('係嗰個時候', '喺嗰個時候'),
        (r'係([^，？$]*?)前', r'喺\1前'),
        ('喺好耐之前嘅', '係好耐之前嘅'),
        ('喺喺', '係喺'),
        ('係係', '係喺'),
        ('喺邊到', '喺邊度'),
        ('幾好嗎', '你好嗎'),
        (r'壞[咗喇啦]', '弊喇'),
        ('冷靜點', '冷靜啲'),
        ('無得', '冇得'),
        ('水果', '生果'),
        ('蒼蠅', '烏蠅'),
        ('碰', '掂'),
        ('比心', '畀心'),
        ('舊鐘', '夠鐘'),
        ('一舊', '一嚿'),
        ('啪啪', '噼噼'),
        ('唔洗', '唔使'),
        (r'洗([乜咩])', r'使\1'),
        ('任工', '陰功'),
        ('好無？', '好唔好？'),
        ('隔嚟', '隔籬'),
        ('隔離', '隔籬'),
        ('快乜', '廢物'),
        ('癌石', '岩石'),
        ('拔命', '搏命'),
        ('得濟', '得滯'),
        ('好餓', '好肚餓'),
        ('除然', '雖然'),
        ('算熟', '算數'),
        ('雪掃', '算數'),
        (r'[噉敢]啱', '咁啱'),
        ('假馬', '咁啱'),
        ('睇黎', '睇嚟'),
        ('出黎', '出嚟'),
        ('黎緊', '嚟緊'),
        ('快點', '快啲'),
        ('舊嘢', '嚿嘢'),
        (r'其樂|奇訥', '奇喇'),
        (r'果(?=[一二三四五六七八九十白千萬])', '過'), # likely refers to passing of X amount of time
        ('無啲', '冇啲'),
        ('乜野', '乜嘢'),
        ('隻野', '隻嘢'),
        ('等我比', '等我畀'),
        ('糟透', '早唞'),
        ('晚晚咩', '慢慢嚟'),
        (r'[洗駛]人唔使本', '使人唔使本'),
        ('亂噉', '亂咁'),
        ('唔好練噉', '唔好亂咁'),
        (r'([咁噉])趕', r'\1講'),
        ('唔好吓氣', '唔好客氣'),
        ('唔使吓氣', '唔使客氣'),
        ('唔生客氣', '唔使客氣'),
        ('噉客氣', '咁客氣'),
        (r'[份分訓]唔着', '瞓唔着'),
        ('細哥', '細個'),
        ('扣晒你', '靠晒你'),
        (r'^通，', '唔通，'),
        ('咩都無', '咩都冇'),
        (r'^埋住', '咪住'),
        (r'^如過', '如果'),
        (r'瞓住', r'瞓着'),
        (r'瞓([得到])好臨', r'瞓\1好稔'),
        ('晚啲', '晏啲'),
        (r'唔[濟齋]啊', '唔制啊'),
        (r'唔[濟齋]$', '唔制'),
        ('食你一啖', '錫你一啖'),
        (r'[洗駛]唔使', '使唔使'),
        ('洗費', '使費'),
        ('你來', '你嚟'),
        ('撲街', '仆街'),
        ('撲你個街', '仆你個街'),
        ('無𠸎𠸎', '無啦啦'), # reverts earlier change
        ('就因為', '就係因為'),
        (r'([食過好])左', r'\1咗'),
        ('食燈', '熄燈'),
        ('食咗啲燈', '熄咗啲燈'),
        ('仲有做係', '仲有就係'),
        (r'^呢度做乜嘢', '你喺度做乜嘢'),
        (r'^呢度做咩', '你喺度做咩'),
        (r'細嚟([啊呀喎㗎])', r'犀利\1'),
        (r'吓係([喇啦])', r'哦，係\1'),
        (r'訓教', r'瞓覺'),
        (r'沖([過咗完])糧',r'沖\1涼'),
        (r'([有冇啲])野', r'\1嘢'),
        ('極氣', '激氣'),
        ('東姑', '冬菇'),
        ('排山', '爬山'),
        ('屁屁', '噼噼'),
        ('早頭', '早唞'),
        ('錢鞍', '錢罌'),
        ('先領', '先令'),
        ('細理', '犀利'),
        ('細利', '犀利'),
        ('痴槍', '枝槍'),
        ('漢寶包', '漢堡包'),
        (r'打[交擾攪]晒', '打搞晒'),
        (r'用黎', '用嚟'),
        (r'唔駛', '唔使'),
        (r'好耶', '好嘢'),
        ('含辛遇苦', '含辛茹苦'),
        ('聽手', '停手'),
        ('別喇', '弊喇'),
        ('中意', '鍾意'),
        ('轉心', '專心'),
        ('嘢獸', '野獸'),
        ('知到', '知道'),
        (r'([好少咁噉常極太幾都乜別到])白煙', r'\1百厭')
    ]
    
    text = resub(text, regex_list_commas)
    text = resub(text, regex_list_misc)
    return resub(text, regex_list_cantonese_errors)

def update_particle_conventions(text):
    # Replace some final particles to get closer to conventions
    regex_list_particles = [
        (r'(?<!衫書十頭招衣帽李咪相棚房高)架(?=[，？…喇啦喎咯囉囖啫])', r'㗎'), # 架 to 㗎 avoiding 架-nouns
        (r'閉[喇啦]', '弊喇'),
        #(r'閉㗎[啦喇]', '弊㗎喇'),
        (r'添[，…]', '𠻹'),
        (r'添$', '𠻹'),
        (r'添，', '𠻹，'),
        (r'添(?=[噃啵喎啊呀喇嘞啦㗎])', '𠻹'),
        (r'好嘛', '好嗎'),
        (r'[啫之姐咋]嘛', '吒嗎'),
        ('㗎嘛？', '㗎咩？'),
        ('㗎嘛', '𠺢嗎'),
        ('唉啊', '哎吔'),
        ('哎啊', '哎吔'),
        (r'(啊){2,}', '啊'),
        ('哎吔啊', '哎吔'),
        ('冇事啊？', '冇事吖嗎？'),
        (r'冇([嘢事])吖嘛，', r'冇\1吖嗎？'),
        (r'冇([嘢事])吖嘛(?!？)', r'冇\1吖嗎？'),
        ('唔係啊嘛？', '唔係𠻺嘛？'),
        ('唔係啊嘛', '唔係𠻺嘛？'),
        ('好啊嘛', '好吖嗎'),
        ('好吖嘛，', '好吖嗎？'),
        ('吖嘛，', '吖嗎'),
        ('啊嘛？', '𠻺嘛？'),
        ('呀嘛', '𠻺嘛'),
        ('啊嘛', '吖嗎'),
        (r'^嚟啊', '嚟吖'),
        ('真係啊', '真係吖'),
        ('話你知啊', '話你知吖'),
        ('話時話啊', '話時話吖'),
        ('老實講啊', '老實講吖'),
        ('坦白講啊', '坦白講吖'),
        ('都唔錯啊', '都唔錯吖'),
        ('真係唔錯啊', '真係唔錯吖'),
        (r'^畀你啊', '畀你吖'),
        (r'^求下你啊', '求下你吖'),
        (r'，求下你啊', '，求下你吖'),
        (r'^聽我講啊', '聽我講吖'),
        (r'，聽我講啊', '，聽我講吖'),
        (r'(?<=[^睇諗試求傾])下？', '吓？'),
        (r'不如([^，…？]*?)啊', r'不如\1吖'),
        (r'幫我([^，…？]*?)啊', r'幫我\1吖'),
        (r'等我([^，…？]*?)啊', r'等我\1吖'),        
        ('啊下', '啊吓'),
        ('囉', '囖'),
        ('囖喎', '喇喎'),
        ('㗎啫', '㗎咋'),
        ('嘅咋', '㗎咋'),
        ('㗎嗎', '㗎咩'),
        ('嘅咩', '㗎咩'),
        ('嘅吓', '㗎嗬'),
        ('啦', '喇'),
        ('喇嘛', '啦嗎'),
        (r'(?<![太備])好喇', '好啦'), # 備 for 準備好喇
        ('你放心喇', '你放心啦'),
        (r'^放心喇', '放心啦'),
        (r'(?<=[，\n])放心喇', '放心啦'),
        ('就啦', '就喇'),
        ('啲喇', '啲啦'),
        ('下喇', '下啦'),
        (r'^嚟喇', '嚟啦'),
        (r'(?<=[，！？])嚟喇', '嚟啦'),
        (r'算數[喇囖]', '算數啦'),
        (r'梗係([^，？]*?)喇', r'梗係\1啦'),
        (r'當然([^，？]*?)喇', r'當然\1啦'),
        (r'反正([^，？]*?)喇', r'反正\1啦'),
        (r'希望([^，？]*?)喇', r'希望\1啦'),
        (r'隨便([^，？]*?)喇', r'隨便\1啦'),
        (r'點都([^，？]*?)喇', r'點都\1啦'),
        (r'唔使([^，？]*?)喇', r'唔使\1啦'),
        (r'(?<!係)咪([^，？$]*?)喇', r'咪\1啦'),
        (r'唔係([\u4e00-\u9fff])喇', r'咪\1啦'),
        (r'唔係住([啊喇啦])', r'咪住\1'),
        (r'唔好([^，？$]*?)喇', r'唔好\1啦'),
        ('去喇', '去啦'),
        ('行喇', '行啦'),
        (r'一於([^，？]*?)喇', r'一於\1啦'),
        (r'不如([^，？]*?)喇', r'不如\1啦'),
        (r'不如([^，？]*?)囖', r'不如\1咯'),
        (r'等我([^，？]*?)喇', r'等我\1啦'),
        (r'畀我([^，？]*?)喇', r'畀我\1啦'),
        (r'我叫([^，？]*?)喇', r'我叫\1啦'),
        (r'你叫([^，？]*?)喇', r'你叫\1啦'),
        (r'佢叫([^，？]*?)喇', r'佢叫\1啦'),
        (r'快啲([^，？]*?)喇', r'快啲\1啦'),
        (r'都係([^，？]*?)喇', r'都係\1啦'),
        (r'請([^，？]*?)喇', r'請\1啦'),
        (r'唔怪得([^，？]*?)喇', r'唔怪得\1啦'),
        (r'唔怪之([^，？]*?)喇', r'唔怪之\1啦'),
        (r'而家([^，？]*?)㗎啦', r'而家\1㗎喇'),
        (r'已經([^，？]*?)㗎啦', r'已經\1㗎喇'),
        (r'冇所謂([^，？]*?)喇', r'冇所謂\1啦'),
        (r'你就應該([^，？]*?)喇', r'你就應該\1啦'),
        ('點就點喇', '點就點啦'),
        ('你信我喇', '你信我啦'),
        ('住佢喇', '住佢啦'),
        ('算喇', '算啦'),
        ('啲喇', '啲啦'),
        (r'^([睇見])喇，', r'\1啦，'),
        ('㗎囖', '㗎啦'),
        (r'^係囖', '係喇'),
        (r'冇辦法喇', '冇辦法啦'),
        (r'等陣先喇', '等陣先啊'),
        ('住囖', '住啦'),
        ('隨你囖', '隨你啦'),
        ('好嘞', '好啦'),
        (r'^噉嘅$', '噉𠸏？'), # isolated 噉嘅 become questions
        (r'係噉樣啊，', '係噉樣呀？'),
        (r'係噉樣啊(?=$)', '係噉樣呀？'),
        (r'係噉啊，', '係噉呀？'),
        (r'係噉啊(?=$)', '係噉呀？'),
        ('又係嘅', '又係𠸏'),
        ('咩原來', '乜原來'),
        (r'原來([^，？$]*?)㗎', r'原來\1嘎'),
        ('喇？', '嗱？'),
        (r'即係(.*?)啫', r'只係\1啫'),
        ('呀呢', '𠻺哩'),
        (r'啊，你$', '𠻺哩？'),
        ('啦喎', '喇喎'), # fix overcorrection with 啦 replacements
        ('喂喇', '弊喇'),
        ('係咩啊', '係咪啊'),
        (r'喇，可$', '喇嗬'),
        (r'喇，可？$', '喇嗬？'),
        (r'[吖啊呀]，可？$', '啊嗬？'),
        (r'^咩，原來', '乜原來'),
        (r'^咩([^，？$]*?)㗎咩', r'乜\1㗎咩'),
        (r'^[何啊]？$', '吓？'),
        (r'唔([係會])掛', r'唔\1啩'),
        ('噉就係喇', '噉咪係囖'),
        (r'^就係喇', '咪係囖'),
        ('吓先', '下先'),
        (r'^咪係咩$', '乜係咩'),
        (r'[冇無]喇喇', '無啦啦'),
        ('無啦啦，', '無啦啦'),
        (r'[巴吧][喇啦]，', '罷啦，'),
        (r'咩啊[，]?話？', '咩話？'),
        (r'係邊([度]?)啊？', r'喺邊\1啊？'),
        ('就得啦', '就得喇'),
        ('嘅喎', '㗎喎'),
        ('係啦', '係喇'),
        ('飲吓', '飲下')
    ]
    return resub(text, regex_list_particles)

def clean_interjections(text):
    # Delete certain noise/grunts
    regex_list_noise = [
        ('嘘，', ''),
        #('天啊，', ''),
        ('，啊，', '，'),
        (r'^[喇啊]，', ''),
        (r'[嘩嚿]啊', ''),
        (r'^[唔嘩嗯啊嗚咦誒哦哈嘿哇，…？]{1,}?$', ''),
        (r'^[吓吼][，…？]?$', ''),
        ('唉，', ''),
        ('哎，', ''),
        (r'哈$', ''),
        (r'(嘻){2,}', ''),
        (r'(唔){2,}', ''),
        (r'^唔？$', '嗯？'),
        (r'^唔$', ''),
        (r'^唔，', ''),
        (r'(嗯){2,}', ''),
        (r'(嗯){2,}', ''),
        (r'(咦){2,}', ''),
        (r'咦[…？]', ''),
        (r'(呼){2,}', ''),
        (r'[嘩呼]…', '')
    ]

    # Fix repeated speech
    regex_list_repeated = [
        (r'([\u4e00-\u9fff]{2,})\1+[，…]*', r'\1…'), # 大佬大佬大佬   -> 大佬…
        (r'([\u4e00-\u9fff])\1{2,}[，…]*', r'\1…'), # 喂喂喂 -> 喂…
        
        (r'([\u4e00-\u9fff])([，…]\1){2,}[，…？]*？', r'\1…？'), # 喂，喂，喂？
        (r'([\u4e00-\u9fff])([，…]\1){2,}[，…]+', r'\1…'), # 喂，喂，喂，
        (r'([\u4e00-\u9fff])([，…]\1){2,}[，…]+$', r'\1…'), # 喂，喂，喂(end of line)
        (r'([\u4e00-\u9fff])([，…]\1){2,}', r'\1…\1'), # 喂，喂，喂-> 喂…喂

        (r'(?<![\u4e00-\u9fff])([\u4e00-\u9fff])[，…](\1[，…$])+', r'\1…'),
        (r'(?<![\u4e00-\u9fff])([\u4e00-\u9fff]{2,})[，…](\1[，…])+', r'\1…'), # 快啲啦，快啲啦，-> 快啲啦…
        (r'(?<![\u4e00-\u9fff])([\u4e00-\u9fff][啊㗎])[，…](\1[，…])*(\1)+[，…]?', r'\1…'), # 停啊，停啊    -> 停啊…

        (r'(?<=[？…，])([我你佢])，\1', r'\1…\1'),
        (r'^([我你佢])，\1', r'\1…\1')
    ]

    text = resub(text, regex_list_noise)
    text = resub(text, regex_list_repeated)
    return text
        
def clean_subtitle_revert_uncommon_conventions(text):
    regex_list = [
        ('噉', '咁'),
        ('𠸏', '嘅'),
        ('啊', '呀'),
        ('𠻺', '呀'),
        (r'[咯囖]', '囉'),
        ('𠻹', '添'),
        ('嗬', '可'),
        ('吖嗎', '吖嘛'),
        ('吒嗎', '咋嘛'),
        ('𠺢嗎', '㗎嘛'),
        ('唧', '啫'),
        ('哎吔', '哎呀')
        ]

    return resub(text, regex_list)

def convert_chinese_numbers_in_text(text):
    chinese_digits = {
        '零': 0, '一': 1, '二': 2, '兩': 2, '两': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9
    }
    chinese_units = {'十': 10, '百': 100, '千': 1000, '萬': 10000}
    uncertain_words = {'幾', '數', '多', '餘', '約'}
    named_date_words = {'月', '號'}

    pattern = re.compile(r'[零一二兩两三四五六七八九十百千萬]+([月號]?)')

    def parse_chinese_number(chinese_num):
        if any(word in chinese_num for word in uncertain_words):
            return None

        if (chinese_num[0] not in chinese_digits and chinese_num[0] != '十'):
            return None

        num = 0
        unit = 1
        temp = 0
        last_was_digit = False

        length = len(chinese_num)
        i = 0

        while i < length:
            char = chinese_num[i]
            if char in chinese_digits:
                if last_was_digit:
                    # Two digits in a row without unit = invalid
                    return None
                temp = chinese_digits[char]
                i += 1
                last_was_digit = True
                if i < length:
                    next_char = chinese_num[i]
                    if next_char in named_date_words:
                        num += temp
                        return str(num)
                    elif next_char in chinese_units:
                        unit = chinese_units[next_char]
                        num += temp * unit
                        temp = 0
                        i += 1
                        last_was_digit = False
                    else:
                        num += temp
                        temp = 0
                else:
                    num += temp
            elif char in chinese_units:
                unit = chinese_units[char]
                if i == 0:
                    num += 1 * unit
                i += 1
                last_was_digit = False
            else:
                return None
            
        if 10 < num < 100000 and num not in {100, 1000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000}:
            return str(num)
        else:
            return None

    def replacer(match):
        chinese_num = match.group(0)
        arabic_num = parse_chinese_number(chinese_num)
        if arabic_num is not None:
            return arabic_num + match.group(1)
        else:
            return chinese_num + match.group(1)

    text = pattern.sub(replacer, text)

    year_pattern = re.compile(r'[零一二三四五六七八九]{2,4}年')

    def year_replacer(match):
        chinese_num = match.group(0)
        
        for old_char, new_char in chinese_digits.items():
            chinese_num = chinese_num.replace(old_char, str(new_char))

        return chinese_num

    return year_pattern.sub(year_replacer, text)

def trim_subtitle(text):
    text = re.sub(r'^，', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)
    
    text = re.sub(r'，$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+$', '', text, flags=re.MULTILINE)

    return text

# Clean up a single text subtitle entry and return it
def clean_subtitle(text):
    text = clean_punctuation(text)
    text = standardize_chars_hk(text)
    text = clean_question_final_particles(text)
    text = replace_standard_chinese(text)
    text = clean_subtitle_misc(text)
    text = convert_chinese_numbers_in_text(text)
    text = update_particle_conventions(text)
    text = clean_interjections(text)

    text = format.linebreak(text)
    
    # TODO: more line breaks and formatting

    # Remove commas
    text = trim_subtitle(text)

    return text
