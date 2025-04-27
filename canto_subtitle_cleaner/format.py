"""Formats subtitles to ensure proper line breaks and spacing."""

import re
from datetime import datetime
from canto_subtitle_cleaner.parse import NO_BREAK_WORDS, is_non_chinese

def clean_subtitle_merge_tiny_and_huge_lines(text):
    lines = text.splitlines()
    result = []
    skip_next = False

    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue

        current = lines[i].strip()

        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()

            if (len(current) <= 5 and len(next_line) >= 16):
                result.append(f"{current}，{next_line}")
                skip_next = True
                continue
            elif (len(current) >= 16 and len(next_line) <= 5):
                result.append(f"{current}，{next_line}")
                skip_next = True
                continue

        result.append(current)

    return '\n'.join(result)

def clean_subtitle_enforce_line_break(text, line_break_length=10, line_max_length=21):
    if '\n' in text or len(text) <= line_max_length:
        return text  # Skip if already broken or too short

    def would_split_word(text, index, words_to_avoid):
        for word in words_to_avoid:
            if index > 0 and text[index - 1:index + 1] == word:
                return True
            if index + 1 < len(text) and text[index:index + 2] == word:
                return True
        return False
    
    def line_break_helper(text, line_break_length):
        if not would_split_word(text, line_break_length, NO_BREAK_WORDS):
            return text[:line_break_length] + '\n' + text[line_break_length:]
        else:
            # try to break after word ends
            for i in range(line_break_length + 1, len(text)):
                if not would_split_word(text, i, NO_BREAK_WORDS):
                    return text[:i] + '\n' + text[i:]
        return text  # give up if nowhere safe

    if is_non_chinese(text[line_break_length - 1]) and is_non_chinese(text[line_break_length]):
        # Start at line_break_length, look for first suitable non-latin char and non-breaking position
        i = line_break_length

        while i < len(text):
            if not is_non_chinese(text[i]) and not would_split_word(text, i, NO_BREAK_WORDS):
                return text[:i] + '\n' + text[i:]
            i += 1

        # fallback to breaking at line_break_length if safe
        return line_break_helper(text, line_break_length)
    else:
        return line_break_helper(text, line_break_length)
    
def final_step(text):
    # Step 2: Remove newline before ≤6 characters at END of subtitle
    text = re.sub(r'\n([^\n]{1,6})$', r'\1', text)

    # Step 3: Merge lines where second line starts with 1-2 characters followed by a Chinese comma
    text = re.sub(r'\n([^\n]{1,2}，)', r'\1', text)

    # Step 4: Insert newline after the fullwidth comma or ellipsis closest to the center
    if '\n' not in text and len(text) >= 20:
        if '，' in text:
            # Break at the comma closest to the center
            comma_indices = [m.start() for m in re.finditer('，', text)]
            center = len(text) // 2
            closest_index = min(comma_indices, key=lambda i: abs(i - center))
            text = text[:closest_index + 1] + '\n' + text[closest_index + 1:]
        elif '…' in text:
            # Break at the ellipsis closest to the center
            ellipsis_indices = [m.start() for m in re.finditer('…', text)]
            center = len(text) // 2
            closest_index = min(ellipsis_indices, key=lambda i: abs(i - center))
            text = text[:closest_index + 1] + '\n' + text[closest_index + 1:]

    # Step 5: Move 1–6 characters after a fullwidth comma to the next line,
    # but only if the first line is longer than or equal to the second
    def move_after_comma_conditional(match):
        part1 = match.group(1)
        part2 = match.group(2)

        # Get line before the match
        prefix = text[:match.start()]
        lines_before = prefix.split('\n')
        prev_line = lines_before[-1] if lines_before else ''

        if len(prev_line) >= len(part2):
            return f'，\n{part1}{part2}'
        else:
            return match.group(0)  # No change

    text = re.sub(
        r'，([^\n]{1,6})\n([^\n]+)',
        move_after_comma_conditional,
        text
    )

    # Step 6: Remove trailing fullwidth commas
    text = re.sub(r'，$', '', text)
    text = re.sub(r'，(?=\n)', '', text) 

    return text


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
