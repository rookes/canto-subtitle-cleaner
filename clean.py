"""Functions for cleaning a single Cantonese subtitle line."""
import re
import parse

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
        ('搵', '揾'),
        ('溫', '温'),
        ('㨂', '揀'),
        ('說', '説'),
        ('脫', '脱'),
        ('稅', '税'),
        ('閱', '閲'),
        ('床', '牀'),
        ('羣', '群'),
        ('裡', '裏'),
        ('麵', '麪'),
        ('敎', '教'),
        ('祕', '秘'),
        ('巿', '市'),
        ('衆', '眾'),
        ('濕', '濕'),
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
        ('癐', '攰')
        
    ]
    return resub(text, regex_list)

def replace_standard_chinese(text):
    regex_list = [
        
        ('無錯', '冇錯'),
        ('無事', '冇事'),
        ('無人', '冇人'),
        ('無見', '冇見'),
        ('無嘢', '冇嘢'),
        ('無問題', '冇問題'),
        ('無能力', '冇能力'),
        ('無辦法', '冇辦法'),
        ('無可能', '冇可能'),
        ('無所謂', '冇所謂'),
        ('無任務', '冇任何'),
        ('無幾耐', '冇幾耐'),
        ('無其他', '冇其他'),
        ('有無', '有冇'),
        ('根本無', '根本冇'),
        ('有沒有', '有冇'),
        ('差不多', '差唔多'),
        ('果陣', '嗰陣'),
        ('果啲', '嗰啲'),
        ('閉喇', '弊喇'),
        ('小鳥', '雀仔'),
        ('鳥仔', '雀仔'),
        ('睡覺', '瞓覺'),
        ('明日', '聽日'),
        ('很好', '好好'),
        ('不要', '唔好'),
        ('這樣', '噉樣'),
        ('好不好', '好唔好'),
        ('好了', '好啦'),
        ('看來', '睇嚟'),
        ('些', '啲'),
        ('昨日', '噚日'),
        ('就是', '就係'),
        ('睡咗', '瞓咗'),
        ('躲埋', '匿埋'),
        ('好累', '好攰')
    ]
    return resub(text, regex_list)

def clean_question_final_particles(text):
    regex_list = [
        (r'\?', '？'),
        (r'\.\.\.', '…'),
        ('… ', '…'),
        (r'(?<![，。！!?.;？；…])係咪(?=[呀啊吖？])', '，係咪') # add comma to tag question 係咪
    ]

    text = resub(text, regex_list)

    # Smart replacement of final particles based on question context
    segments = parse.segments(text)

    def _update_segment(s):
        if s == '':
            return s

        has_question_mark = s[-1] == '？'
        
        if parse.is_question(s):        # has question mark and question word
            s = s.replace('呀','啊')
            s = s.replace('啫', '唧')
        elif has_question_mark:         # has question mark and no question word
            s = s.replace('㗎','嘎')
        else:                           # no question mark and no question word
            s = s.replace('呀','啊')
        
        return s

    segments = map(_update_segment, segments)
    text = ''.join(segments)

    return text

def clean_subtitle_punctuation(text):
    # Basic fixes to commas and periods, removing exclamation marks
    text = re.sub(r'[。.]$', '', text)
    text = re.sub(r'[。.]', '，', text)
    text = re.sub(r'!', '', text)
    text = re.sub(r',', '，', text)
    text = re.sub(r'^，', '', text) # delete comma at start of line
    
    # delete spaces when not next to Latin characters
    text = re.sub(r'(?<![a-zA-Z])\s+(?![a-zA-Z])', '', text) 
    
    # Final particle related changes
    text = re.sub(r'㗎㗎', '㗎', text)
    text = re.sub(r'嘅？', '𠸏？', text)

    # Add a comma after final particles
    text = re.sub(r'啊(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '啊，', text)
    text = re.sub(r'喎(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '喎，', text)
    text = re.sub(r'喇(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '喇，', text)
    text = re.sub(r'啦(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '啦，', text)
    text = re.sub(r'㗎(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '㗎，', text)
    text = re.sub(r'咋(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '咋，', text)
    text = re.sub(r'噃(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '噃，', text)
    text = re.sub(r'嘛(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '嘛，', text)
    text = re.sub(r'嗎(?![？\n！，…啊呀吖喇啦喎啝噃咩吒咋喳啫唧嘛嗱呢𠻹添㖭嗎嘛囉囖咯])', '嗎，', text)
    
    # Add a comma before or after certain words    
    text = re.sub(r'(?<![？！，])(?<!^)(?<![之])但係(?![，！？$])', r'，但係', text, flags=re.MULTILINE)
    text = re.sub(r'(?<![？！，])(?<!^)(?<![之只])不過(?![，！？$])', r'，不過', text, flags=re.MULTILINE)
    text = re.sub(r'(?<![？！，])(?<!^)雖然(?![，！？$])', r'，雖然', text, flags=re.MULTILINE)
    text = re.sub(r'(?<![？！，哋噉])(?<!^)首先(?![，！？$])', r'，首先', text, flags=re.MULTILINE) #I think this will probably get a fair amount of false positives 
    text = re.sub(r'(?<![？！，])(?<!^)嘅話(?![，！？$])', r'嘅話，', text, flags=re.MULTILINE)
    
    #remove trailing
    text = re.sub(r'^啊…', '', text)

    # Remove commas around 就係 
    text = re.sub('就，係，', '就係', text)
    text = re.sub('就係，', '就係', text)

    return text

def clean_subtitle_misc(text):
    # Misc changes for conventions
    regex_list_misc = [
        (r'咁(?![多耐濟滯細大靚高簡廣厚短瘦長少痛遲慘啱快難美遠容犀重脆硬蠢嚴奇荒熟遙弱辛平粗清慢心矮叻臭嘈])', '噉'),
        (r'噉([\u4e00-\u9fff][\u4e00-\u9fff])嘅', r'咁\1嘅'),
        (r'噉(認真|緊張|困難|容易)', r'咁\1'), # change to 咁 before specific 2-char adjectives
        (r'([冇幾])噉', r'\1咁'),
        (r'(?<![譯原])著(?![述名])', '着'),
        (r'[哂曬]', '晒'),
        (r'(?<![曝沖])晒(?=[招馬衫命乾張蓆])', '曬'),
        (r'晒(?=太陽|水艇|雨淋|月光|相舖)', '曬'),
        (r'(?<=[睇諗試求])吓', '下'),
        ('只不過', '之不過'), #FIX
        (r'之不過(?!，)', '之不過，'), #FIX
        (r'[姐唧啫]係', '即係'),
        (r'[依宜]家', '而家'), #FIX
        (r'(?<![空])翻(?![身閲轉譯])', '返'),
        (r'黎$', '嚟'),
        (r'黎([？！，…\n])', r'嚟\1'),
        (r'黎([\u4e00-\u9fff][？！，…\n])', r'嚟\1'),
        (r'^難道', '唔通')
    ]
    
    def fix_common_typos(text):
        regex_list = [
        ]
        return resub(text, regex_list)
    
    # Fix Misc Cantonese errors
    regex_list_cantonese_errors = [
        ('喺到', '喺度'),
        ('呢到', '呢度'),
        ('嗰到', '嗰度'),
        (r'([係答])岩', r'\1啱'),
        ('講得岩', '講得啱'),
        ('係呢邊', '喺呢邊'),
        ('係呢度', '喺呢度'),
        ('係呢個時候', '喺呢個時候'),
        ('係嗰個時候', '喺嗰個時候'),
        (r'係([^，？$]*?)前', r'喺\1前'),
        ('喺好耐之前嘅', '係好耐之前嘅'),
        ('喺喺', '係喺'),
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
        ('洗乜', '使乜'),
        ('任工', '陰功'),
        ('好無？', '好唔好？'),
        ('隔嚟', '隔籬'),
        ('隔離', '隔籬'),
        ('哎喲', '哎吔'),
        ('快乜', '廢物'),
        ('癌石', '岩石'),
        ('拔命', '搏命'),
        ('得濟', '得滯'),
        ('好餓', '好肚餓'),
        ('除然', '雖然'),
        ('算熟', '算數'),
        ('雪掃', '算數'),
        ('敢啱', '咁啱'),
        ('假馬', '咁啱'),
        ('睇黎', '睇嚟'),
        ('出黎', '出嚟'),
        ('快點', '快啲'),
        ('舊嘢', '嚿嘢'),
        (r'其樂|奇訥', '奇喇'),
        (r'果(?=[一二三四五六七八九十白千萬])', '過'), # likely refers to passing of X amount of time
        ('無啲', '冇啲'),
        ('乜野', '乜嘢'),
        ('等我比', '等我畀'),
        ('割到', '嗰度'),
        ('糟透', '早唞'),
        ('晚晚咩', '慢慢嚟'),
        (r'[洗駛]人唔使本', '使人唔使本'),
        ('亂噉', '亂咁'),
        ('唔好練噉', '唔好亂咁'),
        (r'([咁噉])趕', r'\1講'),
        ('唔好吓氣', '唔好客氣'),
        ('唔使吓氣', '唔使客氣'),
        (r'[份分訓]唔着', '瞓唔着'),
        ('細哥', '細個'),
        ('扣晒你', '靠晒你'),
        (r'^通，', '唔通，'),
        ('咩都無', '咩都冇'),
        (r'^埋住', '咪住'),
        (r'^如過', '如果'),
        (r'瞓([得到])好臨', r'瞓\1好稔'),
        ('晚啲', '晏啲'),
        (r'唔[濟齋]啊', '唔制啊'),
        (r'唔[濟齋]$', '唔制'),
        ('食你一啖', '錫你一啖'),
        (r'[洗駛]唔使', '使唔使'),
        ('洗費', '使費'),
        ('你來', '你嚟'),
        ('撲街', '仆街'),
        ('撲你個街', '仆你個街')
    ]
    
    text = resub(text, regex_list_misc)
    return resub(text, regex_list_cantonese_errors)

def clean_subtitle_particles(text):
    # Replace some final particles to get closer to conventions
    regex_list_particles = [
        (r'(?<!衫書十頭招衣帽李咪相棚房高)架(?=[，？…喇啦喎咯囉囖啫])', r'㗎'), # 架 to 㗎 avoiding 架-nouns
        (r'添$', '𠻹'),
        (r'添，', '𠻹，'),
        (r'添(?=[噃啵喎啊呀㗎架])', '𠻹'),
        (r'好嘛', '好嗎'),
        (r'[啫之姐咋]嘛', '吒嘛'),
        ('㗎嘛', '𠺢嘛'),
        ('唉啊', '哎吔'),
        ('哎啊', '哎吔'),
        (r'(?:啊){2,}', '啊'),
        ('啊啊', '啊'),
        ('哎吔啊', '哎吔'),
        ('冇事啊？', '冇事吖嘛？'),
        (r'冇([嘢事])吖嘛(?!？)', r'冇\1吖嘛？'),
        ('唔係啊嘛？', '唔係𠻺嗎？'),
        ('唔係啊嘛', '唔係𠻺嗎？'),
        ('好啊嘛', '好吖嘛'),
        ('好吖嘛，', '好吖嘛？'),
        ('啊嘛？', '𠻺嗎？'),
        ('呀嘛', '𠻺嗎'),
        ('啊嘛', '吖嘛'),
        ('真係啊', '真係吖'),
        ('話你知啊', '話你知吖'),
        ('話時話啊', '話時話吖'),
        ('老實講啊', '老實講吖'),
        ('都唔錯啊', '都唔錯吖'),
        ('真係唔錯啊', '真係唔錯吖'),
        (r'^畀你啊', '畀你吖'),
        (r'^求下你啊', '求下你吖'),
        (r'(?<=[^睇諗試求])下？', '吓？'),
        (r'不如([^，？$]*?)啊', r'不如\1吖'),
        (r'幫我([^，？$]*?)啊', r'幫我\1吖'),        
        ('啊下', '啊吓'),
        ('囉', '囖'),
        ('囖喎', '喇喎'),
        ('㗎啫', '㗎咋'),
        ('嘅咋', '㗎咋'),
        ('㗎嗎', '㗎咩'),
        ('嘅吓', '㗎嗬'),
        ('啦', '喇'),
        ('喇嘛', '啦嘛'),
        (r'(?<!太)好喇', '好啦'),
        ('就啦', '就喇'),
        ('啲喇', '啲啦'),
        ('下喇', '下啦'),
        (r'^嚟喇', '嚟啦'),
        (r'(?<=[，！？])嚟喇', '嚟啦'),
        (r'算數[喇囖]', '算數啦'),
        (r'梗係([^，？$]*?)喇', r'梗係\1啦'),
        (r'當然([^，？$]*?)喇', r'當然\1啦'),
        (r'反正([^，？$]*?)喇', r'反正\1啦'),
        (r'希望([^，？$]*?)喇', r'希望\1啦'),
        (r'隨便([^，？$]*?)喇', r'隨便\1啦'),
        (r'點都([^，？$]*?)喇', r'點都\1啦'),
        (r'唔使([^，？$]*?)喇', r'唔使\1啦'),
        (r'(?<!係)咪([^，？$]*?)喇', r'咪\1啦'),
        (r'唔係([\u4e00-\u9fff])喇', r'咪\1啦'),
        (r'唔好([^，？$]*?)喇', r'唔好\1啦'),
        (r'去([^，？到$]*?)喇', r'去\1啦'),
        ('行喇', '行啦'),
        (r'一於([^，？$]*?)喇', r'一於\1啦'),
        (r'不如([^，？$]*?)喇', r'不如\1啦'),
        (r'不如([^，？$]*?)囖', r'不如\1咯'),
        (r'等我([^，？$]*?)喇', r'等我\1啦'),
        (r'畀我([^，？$]*?)喇', r'畀我\1啦'),
        (r'我叫([^，？$]*?)喇', r'我叫\1啦'),
        (r'你叫([^，？$]*?)喇', r'你叫\1啦'),
        (r'佢叫([^，？$]*?)喇', r'佢叫\1啦'),
        (r'快啲([^，？$]*?)喇', r'快啲\1啦'),
        (r'都係([^，？$]*?)喇', r'都係\1啦'),
        (r'請([^，？$]*?)喇', r'請\1啦'),
        (r'唔怪得([^，？$]*?)喇', r'唔怪得\1啦'),
        (r'唔怪之([^，？$]*?)喇', r'唔怪之\1啦'),
        (r'都已經([^，？$]*?)喇', r'都已經\1啦'),
        (r'冇所謂([^，？$]*?)喇', r'冇所謂\1啦'),
        ('點就點喇', '點就點啦'),
        ('你信我喇', '你信我啦'),
        ('住佢喇', '住佢啦'),
        ('梗喇', '梗啦'),
        ('算喇', '算啦'),
        ('啲喇', '啲啦'),
        (r'^([睇見])喇，', r'\1啦，'),
        ('㗎囖', '㗎啦'),
        (r'^係囖', '係喇'),
        ('住囖', '住啦'),
        ('隨你囖', '隨你啦'),
        ('好嘞', '好啦'),
        (r'^噉嘅$', '噉𠸏？'), # isolated 噉嘅 become questions
        (r'係噉樣啊(?=，|$)', '係噉樣呀？'),
        (r'係噉啊(?=，|$)', '係噉呀？'),
        ('又係嘅', '又係𠸏'),
        ('咩原來', '乜原來'),
        (r'(?<!係)乜([^，？$]*?)啊', r'乜\1呀'),
        (r'原來([^，？$]*?)㗎', r'原來\1嘎'),
        ('喇？', '嗱？'),
        (r'即係(.*?)啫', r'只係\1啫'),
        ('呀呢', '啊哩'),
        (r'啊，你$', '啊哩？'),
        ('啦喎', '喇喎'), # fix overcorrection with 啦 replacements
        ('喂喇', '弊喇'),
        ('係咩啊', '係咪啊'),
        (r'喇，可$', '喇嗬'),
        (r'喇，可？$', '喇嗬？'),
        (r'^咩，原來', '乜原來'),
        (r'^啊？$', '吓？'),
        (r'唔([係會])掛', r'唔\1啩'),
        ('噉就係喇', '噉咪係囖'),
        (r'^就係喇', '咪係囖'),
        ('吓先', '下先'),
        (r'^咪係咩$', '乜係咩'),
        ('無喇喇', '無啦啦'),
        ('無啦啦，', '無啦啦'),
        (r'[巴吧][喇啦]，', '罷啦')
    ]
    return resub(text, regex_list_particles)

def clean_subtitle_custom_standards(text):
    # Delete certain noise/grunts
    regex_list_noise = [
        ('嘘，', ''),
        ('天啊，', ''),
        ('，啊，', '，'),
        (r'^[喇啊]，', ''),
        (r'[嘩嚿]啊', ''),
        (r'^嘩$', ''),
        (r'^吓$', ''),
        (r'^吓？$', ''),
        ('唉，', ''),
        ('哎，', ''),
        (r'哈$', ''),
        (r'(嘻){2,}', ''),
        (r'(唔){2,}', ''),
        (r'^唔$', ''),
        (r'^唔，', ''),
        (r'(嗯){2,}', ''),
        (r'(嗯){2,}', ''),
        (r'(咦){2,}', ''),
        (r'咦[…？]', ''),
        (r'(呼){2,}', ''),
        (r'呼[…]', '')
    ]
    # Fix double punctuation
    regex_list_punctuation = [
        ('，，', '，'),
        ('？，', '？')
    ]
    # Fix repeated speech
    regex_list_repeated = [
        (r'([\u4e00-\u9fff]+[，…])\1+', r'\1…'),     # 快啲啦快啲啦，  -> 快啲啦…
        (r'([\u4e00-\u9fff]{2,})[，…]\1+', r'\1…'),  # 快啲啦，快啲啦，-> 快啲啦…
        (r'([\u4e00-\u9fff]{2})\1+', r'\1…'),        # 大佬大佬大佬   -> 大佬…
        (r'([\u4e00-\u9fff])\1{2,}', r'\1…'),        # 喂喂喂         -> 喂…
        (r'([\u4e00-\u9fff]啊，)\1{2,}', r'\1…'),    # 停啊，停啊，    -> 停啊…
        (r'([\u4e00-\u9fff]㗎，)\1{2,}', r'\1…'),    # 靜㗎，靜㗎，    -> 靜㗎…
        ('，…', '…'),
        ('…，', '…'),
        ('……', '…'),
        (r'((我…|你…|佢…|唔…)){2,}', r'\1'),
        (r'((，我|，你|，佢)){2,}', r'\1…'),
        (r'^我，我', '我…我'),
        (r'^你，你', '你…你'),
        (r'^佢，佢', '佢…佢'),
        (r'[嗯唔哦啊]…', '')
    ]
    text = resub(text, regex_list_noise)
    text = resub(text, regex_list_punctuation)
    text = resub(text, regex_list_repeated)
    return text
        
def clean_subtitle_revert_uncommon_conventions(text):
    regex_list = [
        ('噉', '咁'),
        ('𠸏', '嘅'),
        ('啊', '呀'),
        ('[咯囖]', '囉'),
        ('𠻺嗎', '呀嘛'),
        ('𠻹', '添'),
        ('嗬', '可'),
        ('吒嘛', '咋嘛'),
        ('𠺢嘛', '㗎嘛'),
        ('唧', '啫'),
        ('哎吔', '哎呀'),
        ('之不過', '只不過')
        ]

    return resub(text, regex_list)

# Clean up a single text subtitle entry and return it
def clean_subtitle(text):
    # Remove all line breaks and tabs
    text = re.sub(r'[\n\t]+', ' ', text)

    # Handle English better
    text = re.sub(r'﹑', '\'', text) # restore normal apostrophe
    text = re.sub(r'([a-zA-Z])-([a-zA-Z])', r'\1\2', text) # remove random hyphens
    text = re.sub(r'([a-zA-Z])\n([a-zA-Z])', r'\1\2', text) # remove linebreaks in the middle of latin text
    
    text = standardize_chars_hk(text)
    text = clean_question_final_particles(text)
    text = clean_subtitle_punctuation(text)
    text = clean_subtitle_misc(text)
    text = clean_subtitle_particles(text)
    text = clean_subtitle_custom_standards(text)

    # TODO: line breaks and formatting

    # Step 6: Remove trailing fullwidth commas
    text = re.sub(r'，$', '', text)
    text = re.sub(r'，(?=\n)', '', text) 

    # Old functionality was to run this again at the end, no longer needed
    # text = clean_question_final_particles(text)

    return text