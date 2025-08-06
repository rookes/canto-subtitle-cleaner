"""Helper functions for reading and writing .srt files."""

import re
import warnings
from datetime import datetime, timedelta

class timecode:
    """A class to represent an SRT timecode."""
    TIMECODE_FORMAT = "%H:%M:%S,%f"
    TIME_ZERO = datetime.strptime('00:00:00', '%H:%M:%S')
    
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
        return ' --> '.join([self.start_time.strftime(timecode.TIMECODE_FORMAT)[:-3],
                             self.end_time.strftime(timecode.TIMECODE_FORMAT)[:-3]])
    
    @property
    def start(self):
        return self.start_time.strftime(timecode.TIMECODE_FORMAT)[:-3]
    
    @property
    def end(self):
        return self.end_time.strftime(timecode.TIMECODE_FORMAT)[:-3]

    def __sub__(self, other):
        """Returns the difference between two timecodes in milliseconds."""
        if (self.start_time <= other.end_time and self.start_time >= other.start_time) \
            or (self.end_time >= other.start_time and self.end_time <= other.end_time):
            return 0    # Overlapping timecodes
        
        if self.start_time < other.start_time:
            return (other.start_time - self.end_time).total_seconds() * 1000
        else:
            return (self.start_time - other.end_time).total_seconds() * 1000
    
    def duration(self):
        """Returns the duration of the timecode in milliseconds."""
        return (self.end_time - self.start_time).total_seconds() * 1000
    
    def add_offset(self, offset):
        """Adds an offset to the timecode."""
        if isinstance(offset, datetime) or isinstance(offset, timecode):
            self.start_time = (offset - self.TIME_ZERO + self.start_time)
            self.end_time = (offset - self.TIME_ZERO + self.end_time)
        else:
            try:
                offset = datetime.strptime(str(offset), timecode.TIMECODE_FORMAT)
            except ValueError:
                raise ValueError(f"Invalid offset format: {offset}")
            self.start_time = (offset - self.TIME_ZERO + self.start_time)
            self.end_time = (offset - self.TIME_ZERO + self.end_time)

    def add_duration(self, duration):
        """Adds an offset to the end of the timecode."""
        if isinstance(duration, datetime) or isinstance(duration, timecode):
            self.end_time = (duration - self.TIME_ZERO + self.end_time)
        elif isinstance(duration, (int, float)):
            self.end_time = self.end_time + timedelta(milliseconds=duration)
        else:
            try:
                duration = datetime.strptime(str(duration), timecode.TIMECODE_FORMAT)
            except ValueError:
                raise ValueError(f"Invalid offset format: {duration}")
            self.end_time = (duration - self.TIME_ZERO + self.end_time)

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
            try:
                block_timecode = timecode(lines[1])
            except ValueError:
                warnings.warn(f"Warning: timecode is malformed {lines[1]}. Removing subtitle entry.")
                continue
            
            block_text = '\n'.join(lines[2:])
            subtitle_list.append((block_timecode, block_text))
        else:
            # Optional: skip malformed/short blocks entirely
            continue
    
    return subtitle_list

def clean_timecodes(subtitle_list):
    previous_timecode = None
    delta = datetime.strptime('00:00:00,001', '%H:%M:%S,%f') - datetime.strptime('00:00:00', '%H:%M:%S')

    for timecode, text in subtitle_list:
        if previous_timecode:
            if previous_timecode.end > timecode.start:
                previous_timecode.end_time = timecode.start_time - delta

        previous_timecode = timecode
    
    return subtitle_list


# Takes an iterable list of (timecode, subtitle text) and writes it to a file in .srt format
def list_to_srt(subtitle_list, output_path):
    blocks = []
    i = 1

    clean_timecodes(subtitle_list)

    for timecode, text in subtitle_list:
        blocks.append(f'{i}\n{timecode}\n{text}')
        i += 1
    
    # Join blocks with blank lines
    cleaned_content = '\n\n'.join(blocks)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

