"""Formats subtitles to ensure proper line breaks and spacing."""

import re
from datetime import datetime
import pycantonese
import warnings
from canto_subtitle_cleaner.parse import is_punctuation, is_non_chinese, RE_DELIMITING_PUNCTUATION

def linebreak(text, line_max_length=21):
    if '\n' in text:
        raise ValueError("Text already contains line breaks.")

    length = len(text)

    if length <= line_max_length - 3:
        return text

    # We always want two lines. Restrict first line shorter for aesthetic reasons.
    firstline_min_length = max(length // 4, 4)
    firstline_max_length = min(length // 2, line_max_length - 1)
    firstline_extended_length = min(length // 4 * 3, line_max_length - 3)

    # If possible, split after delimiting punctuation in the first half the line
    for i in range(firstline_max_length, firstline_min_length - 1, -1):
        if re.match(RE_DELIMITING_PUNCTUATION, text[i]):
            return text[:i + 1] + '\n' + text[i + 1:]
        
    # Otherwise, split after delimiting punctuation in the second half of the line
    for i in range(firstline_max_length, firstline_extended_length + 1):
        if re.match(RE_DELIMITING_PUNCTUATION, text[i]):
            return text[:i + 1] + '\n' + text[i + 1:]

    # Otherwise, split at the first non-punctuation chinese character that's not in the middle of a word
    for i in range(firstline_max_length, firstline_min_length - 1, -1):
        
        if is_punctuation(text[i]):
            return text[:i + 1] + '\n' + text[i + 1:]
        
        if (len(pycantonese.segment(text[i:i + 2])) == 1):
            print(f"Skipping line break at char {i} because it is in the middle of a word: {text[i:i + 2]}")
            continue
            
        return text[:i + 1] + '\n' + text[i + 1:] 

    # If all else fails, just return the original text
    warnings.warn(f"No suitable line break found for line in line {text}.")
    return text
    
def final_step(text):
    # Step 6: Remove trailing fullwidth commas
    text = re.sub(r'，$', '', text)
    text = re.sub(r'，(?=\n)', '', text) 

    return text

# Fix subtitles that incorrectly broken across 2 different subtitles
def adjust_subtitle_breaks(subtitle_list):
    OMIT_CHARS = {"噉", "喂", "噢", "嗯", "哦", "好", "吓", "哼", "嘩", "係", "吼"}
    prev_text = None

    for i, (timecode, text) in enumerate(subtitle_list):
        if prev_text and text:
            # If final character of previous is not a Chinese letter, skip
            if re.match(r'[\x00-\x7F]', prev_text[-1]):
                prev_text = text
                prev_timecode = timecode
                continue

            match = re.match(r'^([^\x00-\x7F])[，]|^([^\x00-\x7F])[？]', text)
            
            if match:
                if match.group(1):
                    char = match.group(1)
                    question_mark = ""

                if match.group(2):
                    char = match.group(2)
                    question_mark = "？"
                
                if not char:
                    raise ValueError("Error: beginning of line was matched, but no matching character was set.")

                delta_ms = timecode - prev_timecode

                if delta_ms < 1000 and char not in OMIT_CHARS:
                    subtitle_list[i - 1] = (prev_timecode, prev_text + char + question_mark)
                    
                    print(f"============ Subtitle break: Pulling back char {char} from line {i}. ============")
                    print(f"End of previous line at {prev_timecode.end}; start of current at {timecode.start}; delta {int(delta_ms)}ms")
                    print(f"({repr(prev_text)} {repr(text)}) -> ({repr(prev_text + char + question_mark)} {repr(text[len(char + question_mark) + 1:])})")
                    print("============================================================================")
                    
                    text = text[len(char + question_mark) + 1:]
                    subtitle_list[i] = (timecode, text)

        prev_text = text
        prev_timecode = timecode

    return subtitle_list
