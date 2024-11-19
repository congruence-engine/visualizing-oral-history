# This script is designed to create encodings from the transcript segments
# using the sentence-transformers/all-mpnet-base-v2
# (see https://huggingface.co/sentence-transformers/all-mpnet-base-v2 )
# Depends on:
#     code/preprocessing/011_consolidate_transcripts.py

# Local setup
from local_dir_setup import *

# Libraries
import os
import pandas as pd
import pickle
import torch
from sentence_transformers import SentenceTransformer


# Check device
if torch.cuda.is_available():
    print('Run on CUDA')
    print(f'Device count: {torch.cuda.device_count()}')
    print(f'Current device: {torch.cuda.current_device()}')
    print(f'Current device name: {torch.cuda.get_device_name(torch.cuda.current_device())}')
else:
    print('Run on CPU')


# Setup and folders
folder_transcripts = dir_scratch + "---input-folder---" # Folder with the transcripts from 011_consolidate_transcripts
folder_embeddings = dir_scratch + "---output-folder---"
os.mkdir(folder_embeddings)

# Load segments
segments = pd.read_csv(folder_transcripts + "---input-file---")

### --- sentence-transformers/all-mpnet-base-v2 --- ###
# https://huggingface.co/sentence-transformers/all-mpnet-base-v2
# based on the pretrained microsoft/mpnet-base model
# fine-tuned in on a 1B sentence pairs dataset

# Load model
model_sbert_mpnet = SentenceTransformer(
    'sentence-transformers/all-mpnet-base-v2',
    cache_folder=dir_modelcache,
    device='cuda'
)
model_sbert_mpnet.max_seq_length = 512

# Embed segments
embeddings_sbert_mpnet = model_sbert_mpnet.encode(segments["text"])

# Save segments and embeddings
# see also https://www.sbert.net/examples/applications/computing-embeddings/README.html
with open(folder_embeddings + "---embeddings-file---", "wb") as fOut:
    pickle.dump({
        'transcript': segments["transcript"],
        'start_id': segments["start_id"],
        'start_time': segments["start_time"],
        'end_id': segments["end_id"],
        'end_time': segments["end_time"],
        'text': segments["text"],
        'embeddings_sbert_mpnet': embeddings_sbert_mpnet
    }, fOut, protocol=pickle.HIGHEST_PROTOCOL)
