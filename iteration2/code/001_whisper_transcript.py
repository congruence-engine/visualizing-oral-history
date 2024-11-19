# This script uses OpenAI's Whisper to generate transcripts
# using the large-v3 model (the language is set to English)

# Local setup
from local_dir_setup import *

# Libraries
import os
import datetime
import pandas as pd
import torch
import whisper


# Check device
if torch.cuda.is_available():
    print('Run on CUDA')
    print(f'Device count: {torch.cuda.device_count()}')
    print(f'Current device: {torch.cuda.current_device()}')
    print(f'Current device name: {torch.cuda.get_device_name(torch.cuda.current_device())}')
else:
    print('Run on CPU')


# Folders
folder_cut = dir_scratch + "---input-folder---" # Folder with the audio files
folder_whisper_transcript = dir_scratch + "---output-folder---"
print(f"{folder_cut=}")
print(f"{folder_whisper_transcript=}")

# Load the model
model = whisper.load_model("large-v3", download_root=dir_modelcache)

ordered_file_list = sorted(os.listdir(folder_cut))
for f in ordered_file_list:

    # Filenames
    input_recording_path = folder_cut + "/" + f
    output_csv_path = folder_whisper_transcript + "/" + f[:-4] + "__segments.csv"

    # Transcribe
    print("transcribing: ", datetime.datetime.now())
    result = model.transcribe(
        input_recording_path,
        fp16=False,
        task="transcribe",
        language="en",
        patience=2,
        beam_size=5
    )

    # Save the segments
    print("saving: ", datetime.datetime.now())
    df = pd.DataFrame(result["segments"])
    df.to_csv(output_csv_path, index=False)