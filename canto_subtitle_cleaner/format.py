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

    if length <= line_max_length - 2:
        return text

    # We always want two lines. Restrict first line shorter for aesthetic reasons.
    firstline_min_length = max(length // 4, 4)
    firstline_max_length = min(length // 2, line_max_length - 1)

    # if there is delimiting punctation, split after the first one
    for i in range(firstline_max_length, firstline_min_length - 1, -1):
        if re.match(RE_DELIMITING_PUNCTUATION, text[i]):
            return text[:i + 1] + '\n' + text[i + 1:]

    for i in range(firstline_max_length, firstline_min_length - 1, -1):
        # split at the first non-punctuation chinese character that's not in the middle of a word
        if is_punctuation(text[i]):
            return text[:i + 1] + '\n' + text[i + 1:]
        
        if (len(pycantonese.segment(text[i:i + 2])) == 1):
            print(f"Skipping line break at {i} because it is in the middle of a word: {text[i:i + 2]}")
            continue
            
        return text[:i + 1] + '\n' + text[i + 1:] 

    warnings.warn(f"No suitable line break found for line in line {text}.")
    return text
    
def final_step(text):
    # Step 6: Remove trailing fullwidth commas
    text = re.sub(r'，$', '', text)
    text = re.sub(r'，(?=\n)', '', text) 

    return text

# TODO: Currently not used, re-implement later
# Fix subtitles that incorrectly broken across 2 different subtitles
def adjust_subtitle_breaks(output_file):
    OMIT_CHARS = {"噉", "喂", "噢", "嗯", "哦"}

    def parse_timestamp(ts):
        return datetime.strptime(ts, "%H:%M:%S,%f")

    def ms_diff(t1, t2):
        return (t2 - t1).total_seconds() * 1000

    with open(output_file, 'r', encoding='utf-8') as f:
        subtitles = f.read().strip().split('\n\n')

    processed_subs = []
    for i in range(len(subtitles)):
        block = subtitles[i].split('\n')
        if len(block) < 3:
            processed_subs.append('\n'.join(block))
            continue

        index, timestamp, *text = block
        if i > 0 and text:
            prev_block = processed_subs[-1].split('\n')
            prev_index, prev_timestamp, *prev_text = prev_block
            current_first_line = text[0]

            match = re.match(r'^([^\x00-\x7F])，', current_first_line)
            if match:
                char = match.group(1)
                prev_end = parse_timestamp(prev_timestamp.split(' --> ')[1])
                curr_start = parse_timestamp(timestamp.split(' --> ')[0])
                delta_ms = ms_diff(prev_end, curr_start)

                if delta_ms < 801 and char not in OMIT_CHARS:
                    prev_block[-1] += char
                    text[0] = text[0][len(char) + 1:]
                    processed_subs[-1] = '\n'.join([prev_index, prev_timestamp] + prev_block[2:])

        processed_subs.append('\n'.join([index, timestamp] + text))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(processed_subs))
