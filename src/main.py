import av
import whisper
from subtitle_generator import generate_subtitles, format_srt, write_srt_file
import sys
import os
import argparse

def extract_audio(video_file, audio_file="audio.wav"):
    container = av.open(video_file)
    audio_stream = container.streams.audio[0]
    output = av.open(audio_file, mode='w')
    output_stream = output.add_stream('pcm_s16le')

    for frame in container.decode(audio_stream):
        for packet in output_stream.encode(frame):
            output.mux(packet)

    for packet in output_stream.encode():
        output.mux(packet)

    output.close()
    return audio_file

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    segments = result['segments']
    transcript = [(seg['start'], seg['end'], seg['text']) for seg in segments]
    return transcript

def main(input_folder, output_folder):
    for video_file in os.listdir(input_folder):
        if video_file.endswith(('.mp4', '.avi', '.mkv')):
            video_path = os.path.join(input_folder, video_file)
            audio_file = extract_audio(video_path)
            transcript = transcribe_audio(audio_file)
            subtitles = generate_subtitles(transcript)
            srt_content = format_srt(subtitles)
            srt_file_name = os.path.splitext(video_file)[0] + '.srt'
            srt_file_path = os.path.join(output_folder, srt_file_name)
            write_srt_file(srt_content, srt_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Transcription")
    parser.add_argument('--input_dir', type=str, required=True, help="Path to the input folder containing video files")
    parser.add_argument('--output_dir', type=str, required=True, help="Path to the output folder for SRT files")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)