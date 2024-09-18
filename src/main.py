import os
import argparse
import time
import av
import whisper
import webrtcvad
import wave
import logging
from datetime import datetime
from pydub import AudioSegment
from subtitle_generator import generate_subtitles, format_srt, write_srt_file

# Function to configure logging

def configure_logging(output_dir):
    # Create logs folder inside output_dir if it does not exist
    logs_dir = os.path.join(output_dir, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file = os.path.join(logs_dir, f'log_{datetime.now().strftime("%Y-%m-%d")}.log')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


# Function to extract audio from video file
def extract_audio(video_file, output_folder):
    logging.info(f"Starting audio extraction from {video_file}")
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    audio_file = os.path.join(output_folder, f"{base_name}.wav")
    container = av.open(video_file)
    audio_stream = container.streams.audio[0]
    output = av.open(audio_file, mode='w')
    output_stream = output.add_stream('pcm_s16le', rate=16000, layout='mono')

    for frame in container.decode(audio_stream):
        frame.pts = None  # Reset PTS to avoid timestamp issues
        for packet in output_stream.encode(frame):
            output.mux(packet)

    for packet in output_stream.encode():
        output.mux(packet)

    output.close()
    logging.info(f"Audio extracted to {audio_file}")
    return audio_file

def read_wave(path):
    logging.info(f"Reading wave file {path}")
    audio = AudioSegment.from_wav(path)
    
    if audio.channels != 1:
        logging.info("Converting stereo audio to mono")
        audio = audio.set_channels(1)
    
    pcm_data = audio.raw_data
    sample_rate = audio.frame_rate
    sample_width = audio.sample_width
    
    assert sample_width == 2, "Audio file must be 16-bit"
    assert sample_rate in (8000, 16000, 32000, 48000), "Sample rate must be 8kHz, 16kHz, 32kHz, or 48kHz"
    
    logging.info(f"Wave file {path} read successfully")
    return pcm_data, sample_rate

def write_wave(path, audio, sample_rate):
    logging.info(f"Writing wave file {path}")
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)
    logging.info(f"Wave file {path} written successfully")

def vad_filter(audio_file, output_file, aggressiveness=3):
    logging.info(f"Starting VAD filtering on {audio_file} with aggressiveness level {aggressiveness}")
    vad = webrtcvad.Vad(aggressiveness)
    audio, sample_rate = read_wave(audio_file)
    frame_duration = 30  # ms
    frame_size = int(sample_rate * (frame_duration / 1000) * 2)
    segments = []

    for i in range(0, len(audio), frame_size):
        frame = audio[i:i + frame_size]
        if len(frame) < frame_size:
            break
        is_speech = vad.is_speech(frame, sample_rate)
        if is_speech:
            segments.append(frame)
        else:
            segments.append(b'\x00' * frame_size)  # Append silence for non-speech segments

    filtered_audio = b''.join(segments)
    write_wave(output_file, filtered_audio, sample_rate)
    logging.info(f"VAD filtering completed on {audio_file}, output saved to {output_file}")
    logging.info(f"Original audio length: {len(audio)} bytes")
    logging.info(f"Filtered audio length: {len(filtered_audio)} bytes")

def transcribe_audio(audio_file, device, model_name):
    logging.info(f"Starting transcription on {audio_file} using model {model_name} on {device}")
    model = whisper.load_model(model_name, device=device)
    
    usefp16 = True if device == 'cuda' else False
    result = model.transcribe(audio_file, fp16=usefp16, verbose=False)
    segments = result['segments']
    total_segments = len(segments)
    transcript = []

    for i, seg in enumerate(segments):
        transcript.append((seg['start'], seg['end'], seg['text']))
        progress = (i + 1) / total_segments * 100
        logging.info(f"Transcription progress: {progress:.2f}%")

    logging.info(f"Transcription completed for {audio_file}")
    return transcript

def main(input_folder, output_folder, device, model_name):
    logging.info(f"Processing videos in {input_folder}")
    for video_file in os.listdir(input_folder):
        if video_file.endswith(('.mp4', '.avi', '.mkv')):
            logging.info(f"****************")
            logging.info(f"Processing video file {video_file}")
            video_path = os.path.join(input_folder, video_file)
            audio_file = extract_audio(video_path, output_folder)
            filtered_audio_file = os.path.join(output_folder, f"filtered_{os.path.basename(audio_file)}")
            vad_filter(audio_file, filtered_audio_file)
            transcript = transcribe_audio(filtered_audio_file, device, model_name)
            subtitles = generate_subtitles(transcript)
            srt_content = format_srt(subtitles)
            srt_file_name = os.path.splitext(video_file)[0] + '.srt'
            srt_file_path = os.path.join(output_folder, srt_file_name)
            write_srt_file(srt_content, srt_file_path)
            logging.info(f"Subtitle file {srt_file_path} created successfully")
    logging.info("Processing completed for all videos")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Transcription")
    parser.add_argument('--input_dir', type=str, required=True, help="Path to the input folder containing video files")
    parser.add_argument('--output_dir', type=str, required=True, help="Path to the output folder for SRT files")
    parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], default='cpu', help="Device to run the model on (cpu or cuda)")
    parser.add_argument('--model_name', type=str, choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'], default='base', help="Whisper model to use (e.g., base, large-v2, large-v3)")
    args = parser.parse_args()

    # Configure logging with the output directory
    configure_logging(args.output_dir)

    # Record the start time
    start_time = time.time()

    logging.info(f"Starting video transcription with input directory: {args.input_dir} and output directory: {args.output_dir}, using device: {args.device}, and model: {args.model_name}")
    main(args.input_dir, args.output_dir, args.device, args.model_name)
    logging.info("Video transcription completed")

    # Record the end time
    end_time = time.time()

    # Calculate and log the elapsed time
    elapsed_time = end_time - start_time
    logging.info(f"Total execution time: {elapsed_time:.2f} seconds")