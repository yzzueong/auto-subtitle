import os
from typing import Iterator, TextIO


def str2bool(string):
    string = string.lower()
    str2val = {"true": True, "false": False}

    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

# ensure each line is a complete sentence
def write_srt(transcript: Iterator[dict], file: TextIO):
    idx = 1
    current_text = ""
    start, end = None, None
    for segment in transcript:
        tt = segment['text'].strip().replace('-->', '->')
        current_text += tt if current_text.endswith(" ") else f" {tt}"
        start = segment['start'] if start==None else start
        end = segment['end']
        if current_text.endswith((".","?","!")) or segment==transcript[-1]:
            # end of sentence or end of video
            print(
                f"{idx}\n"
                f"{format_timestamp(start, always_include_hours=True)} --> " 
                f"{format_timestamp(end, always_include_hours=True)}\n" 
                f"{current_text}\n",
                file=file,
                flush=True,
            )
            idx += 1
            current_text, start, end = "", None, None

def filename(path):
    return os.path.splitext(os.path.basename(path))[0]
