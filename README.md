

# Video Transcription
- [Video Transcription](#video-transcription)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Available models](#available-models)
  - [Usage](#usage)
    - [Option 1 - Run from source code](#option-1---run-from-source-code)
    - [Option 2 - Run from a pre-built image](#option-2---run-from-a-pre-built-image)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)


This project extracts audio from video files ('.mp4', '.avi', '.mkv'), applies Voice Activity Detection (VAD) to filter out non-speech segments, and generates subtitles using the Whisper model.

We can clone the source code and run the tool from there. We can also use the pre-built docker image that is published here: https://hub.docker.com/r/hungdoan/video-transciption

## Features

- Extract audio from video files
- Apply VAD to filter out non-speech segments
- Transcribe audio to text using Whisper
- Generate subtitles in SRT format

## Requirements

- Python 3.7+
- Docker
- Docker Compose
- CUDA supported machine

## Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Ensure Docker and Docker Compose are installed and running on your machine.

## Available models
There are five model sizes, offering speed and accuracy tradeoffs. Below are the names of the available models and their approximate memory requirements and inference speed relative to the large model; actual speed may vary depending on many factors including the available hardware.

|  Size  | Multilingual model | Required VRAM | Relative speed |
|:------:|:------------------:|:-------------:|:--------------:|
|  tiny  |  `tiny`       |     ~1 GB     |      ~32x      |
|  base  |  `base`       |     ~1 GB     |      ~16x      |
| small  |  `small`       |     ~2 GB     |      ~6x       |
| medium |  `medium`      |     ~5 GB     |      ~2x       |
| large  |  `large`       |    ~10 GB     |       1x       | 

(Source: [Whisper](https://github.com/openai/whisper))

## Usage
### Option 1 - Run from source code
1. Place your video files in the input directory.
2. Run the script using Docker Compose:
    ```sh
    docker compose -p "video-transcript" --env-file .env --env-file .env.base up --build --remove-orphans
    ```
    All configurable variables are defined in the .env files, where: 
    - MODEL_NAME: model name that we wanna use, see **Available models** section for the list. The default is `base`
    - DEVICE: It can be "cuda" or "cpu", the "cuda" is recommended if you have GPU(s) has CUDA cores. The default is `cuda`


3. The output SRT files will be saved in the output directory.


**Example:**

To transcribe a video file named `example.mp4`. 
In the directory that contain the source code.
1. Clone the source code
    ```
    git clone <repository-url>
    ```
2. Change working directory to the source code
    ```
    cd <repository-directory>
    ```
3. Place `example.mp4` in the `input` directory.
    ```
    cp example.mp4 <repository-directory>/input/
    ```
4. Run the script using Docker Compose:
    ```sh
    docker compose -p "video-transcript" --env-file .env --env-file .env.base up --build --remove-orphans
    ```
3. The generated subtitle file `example.srt` will be saved in the [`output`] directory.

### Option 2 - Run from a pre-built image
Execute this script in your powershell
```powershell
$input_dir = "D:/input" 
$output_dir = "D:/output" 
$model_cache_dir = "D:/model_caches"
$model_name = "base" 
$device = "cuda" 
docker pull hungdoan/video-transciption:latest
docker run --gpus=all --rm -it --env MODEL_NAME=${model_name} --env DEVICE=${device} -v ${input_dir}:/input -v ${output_dir}:/output -v ${model_cache_dir}:/root/.cache/whisper hungdoan/video-transciption:latest 
```
Where: 
- MODEL_NAME: model name that we wanna use, see **Available models** section for the list. The default is `base`
- DEVICE: It can be "cuda" or "cpu", the "cuda" is recommended if you have GPU(s) has CUDA cores. The default is `cuda`
- `-v ${input_dir}:/input` : we need to specify (mount) input folder so that the tool could scans input videos
- `-v ${output_dir}:/output`: we need to specify (mount) output folder to save the file. 
- `-v ${model_cache_dir}:/root/.cache/whisper`: optionally, we can specify the model folder to keep downloaded model and reuse it.
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Whisper](https://github.com/openai/whisper) - A general-purpose speech recognition model by OpenAI
- [WebRTC VAD](https://github.com/wiseman/py-webrtcvad) - Python interface to the WebRTC Voice Activity Detector
- [PyAV](https://github.com/mikeboers/PyAV) - Pythonic bindings for FFmpeg's libraries
