"""Helper functions for reading and writing .srt files."""

import re
from datetime import datetime

class timecode:
    """A class to represent an SRT timecode."""
    TIMECODE_FORMAT = "%H:%M:%S,%f"
    
    start_time = None
    end_time = None

    def __init__(self, text):
        """Initialize the timecode from a string in the format 'HH:MM:SS,ms --> HH:MM:SS,ms'."""
        text = text.split(' --> ')
        if len(text) != 2:
            raise ValueError(f"Invalid timecode format: {text}")

        self.start_time = datetime.strptime(text[0], timecode.TIMECODE_FORMAT)
        self.end_time = datetime.strptime(text[1], timecode.TIMECODE_FORMAT)

        if (self.start_time >= self.end_time):
            raise ValueError(f"Start time must be less than end time: {text}")
    
    def __str__(self):
        return ' --> '.join([self.start_time.strftime(timecode.TIMECODE_FORMAT),
                             self.end_time.strftime(timecode.TIMECODE_FORMAT)])
    
    def diff(self, other):
        """Returns the difference between two timecodes in milliseconds."""
        if not isinstance(other, timecode):
            raise TypeError("Can only compare with another timecode instance")
        
        if self.start_time >= other.end_time or self.end_time <= other.start_time:
            return 0    # Overlapping timecodes
        
        if self.start_time < other.start_time:
            return (other.start_time - self.end_time).total_seconds() * 1000
        else:
            return (self.end_time - other.start_time).total_seconds() * 1000
    
    def duration(self):
        """Returns the duration of the timecode in milliseconds."""
        return (self.end_time - self.start_time).total_seconds() * 1000

# Takes an .srt file and returns an iterable list of (timecode, raw subtitle text)
def srt_to_list(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into blocks
    blocks = re.split(r'\n\s*\n', content.strip())
    subtitle_list = []

    for block in blocks:
        lines = block.splitlines()
        if len(lines) >= 3:
            # Ignore header index, we will renumber anyway
            block_timecode = lines[1]
            block_text = '\n'.join(lines[2:])
            subtitle_list.append((block_timecode, block_text))
        else:
            # Optional: skip malformed/short blocks entirely
            continue
    
    return subtitle_list

# Takes an iterable list of (timecode, subtitle text) and writes it to a file in .srt format
def list_to_srt(subtitle_list, output_path):
    blocks = []
    i = 1

    for timecode, text in subtitle_list:
        blocks.append(f'{i}\n{timecode}\n{text}')
        i += 1
    
    # Join blocks with blank lines
    cleaned_content = '\n\n'.join(blocks)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

