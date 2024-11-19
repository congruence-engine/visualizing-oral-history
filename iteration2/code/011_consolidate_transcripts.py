# This script is designed to combine all the segments generated through automatic transcription
# for the different interviews into one single file. Also, the segments are aggregated sequentially
# to form segments between 100 and 300 words -- that is useful for topic modelling, as most approaches
# do not perform well on short texts.
# Depends on:
#     code/preprocessing/001_whisper_transcript.py

# Local setup
from local_dir_setup import *

# Libraries
import os
import math
import numpy as np
import pandas as pd

# Utils
def is_null(value):
    # Check if None
    if value is None:
        return True
    # Check if nan
    if isinstance(value, float) and math.isnan(value):
        return True
    # Check if NaN, Inf or -Inf
    if isinstance(value, (np.float64, np.float32, np.float16)) and np.isnan(value):
        return True
    # Check if pandas NaN or NaT
    if pd.isna(value):
        return True
    return False

# Setup and folders
folder_transcripts_input = dir_scratch + "---input-folder---" # Folder with the transcripts from 001_whisper_transcript.py
folder_transcripts_output = dir_scratch + "---output-folder---"

# Load files
ordered_file_list = sorted(os.listdir(folder_transcripts_input))

all_transcripts_segments = pd.DataFrame({
    'transcript': [],
    'start_id': [],
    'start_time': [],
    'end_id': [],
    'end_time': [],
    'text': [],
})

# For each file
for f in ordered_file_list:
    # Load the transcript
    print(f)
    transcript_i = pd.read_csv(folder_transcripts_input + "/" + f)
    current_segment = ""
    current_segment_start_id = None
    current_segment_start_time = None
    current_segment_end_id = None
    current_segment_end_time = None
    # For each sentence in the transcript
    for index, row in transcript_i.iterrows():
        # if the new current transcript segment is empty
        # add row info to the current transcript segment
        if current_segment == "":
            current_segment_start_id = row["id"]
            current_segment_end_id = row["id"]
            current_segment_start_time = row["start"]
            current_segment_end_time = row["end"]
        # add row text to the current transcript segment
        if is_null(row["text"]):
            print("Empty text in:" + f)
            print(current_segment)
            print(row["text"])
            print("\n")
        else:
            current_segment += row["text"]
            # if the text ends with a dot
            # add it to the consolidated dataset
            if (row["text"].endswith(".") and len(current_segment.split()) > 100) or \
                    len(current_segment.split()) > 200 or \
                    index == transcript_i.shape[0] - 1:
                #print(f"{index} {transcript_i.shape[0]}")
                current_segment_end_id = row["id"]
                current_segment_end_time = row["end"]
                new_row = {
                    'transcript': f[:10],
                    'start_id': current_segment_start_id,
                    'start_time': current_segment_start_time,
                    'end_id': current_segment_end_id,
                    'end_time': current_segment_end_time,
                    'text': current_segment,
                }
                all_transcripts_segments = pd.concat([all_transcripts_segments, pd.DataFrame([new_row])])
                current_segment = ""
                current_segment_start_id = None
                current_segment_start_time = None
                current_segment_end_id = None
                current_segment_end_time = None

# Count length of segments
all_transcripts_segments["word_count"] = all_transcripts_segments['text'].str.split().str.len()
# Write output
all_transcripts_segments.to_csv(folder_transcripts_output + "---output-csv-file---", index=False)