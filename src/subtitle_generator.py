from utils import format_time

def generate_subtitles(transcript):
    """
    Generate subtitles for the video.
    :param transcript: List of tuples (start_time, end_time, text).
    :return: List of subtitles with timestamps.
    """
    subtitles = []
    for idx, (start_time, end_time, text) in enumerate(transcript):
        subtitles.append((start_time, end_time, text))
    return subtitles

def format_srt(subtitles):
    """
    Format subtitles into SRT format.
    :param subtitles: List of subtitles with timestamps.
    :return: Formatted SRT string.
    """
    srt_content = ""
    for idx, (start, end, text) in enumerate(subtitles):
        start_time = format_time(start)
        end_time = format_time(end)
        srt_content += f"{idx + 1}\n{start_time} --> {end_time}\n{text}\n\n"
    return srt_content

def write_srt_file(srt_content, filename="subtitles.srt"):
    """
    Write SRT content to a file.
    :param srt_content: Formatted SRT string.
    :param filename: Output SRT file name.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(srt_content)