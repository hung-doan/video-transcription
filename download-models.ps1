# Ref: https://github.com/openai/whisper/blob/main/whisper/__init__.py
# Download models for Whisper
# This is an optional step. The code will download the models automatically if they are not found.
Invoke-WebRequest -Uri "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt" -OutFile "./models/whisper/base.pt"
Invoke-WebRequest -Uri "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt" -OutFile "./models/whisper/large-v3.pt"