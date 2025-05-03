"""Helper functions for parsing and pattern recognition on a single line of Cantonese."""
import re

# List of characters that may be used alone to start a sentence before a comma
STANDALONE_START_CHARS = {"噉", "喂", "噢", "嗯", "哦", "嗱", "係", "好", "嘩"}

# Punctuation characters that break lines into independent segments
RE_DELIMITING_PUNCTUATION = re.compile(r'([，？！…。：；]+)')

RE_QUESTION_PAT = re.compile(r'([\u4e00-\u9fff])唔\1')          
QUESTION_WORDS = ['做乜', '係咪', '未', '有冇', '好冇', '邊', '咩', '邊個', '點解', '幾耐', '幾時', '邊度', '點', '點樣', '幾多', '乜嘢']

ZH = r'[\u4e00-\u9fff]'
NUM = r'[\d零一二兩两三四五六七八九十百千]'
NOT_NUM = r'[^\d零一二兩两三四五六七八九十百千]'

def segments(line):
    """Split a line into segments based on punctuation and standalone characters."""
    line = re.sub(RE_DELIMITING_PUNCTUATION, r'\1,', line) # add an English comma as our new delimiter
    line = [x for x in line.split(',') if x] # remove empty segments
    
    return line

def is_question(segment):
    """Check if a line segment has a question format, regardless of any final particles."""
    if segment[-1] == '？':
        if re.match(RE_QUESTION_PAT, segment) or  any(word in segment for word in QUESTION_WORDS):
            return True 
    
    return False

def is_non_chinese(char):
    return re.match(r'[A-Za-z\d]', char)

def is_punctuation(char):
    return re.match(r'[，？！…：；\s\-]', char)