# This script is designed to create embeddings from the collection descriptions
# using the sentence-transformers/all-mpnet-base-v2
# (see https://huggingface.co/sentence-transformers/all-mpnet-base-v2 )

# Local setup
from local_dir_setup import *

# Libraries
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
folder_museum_data = dir_scratch + "---museum-data-folder---" # Folder with the museum object descriptions

# Load museum object descriptions
museum_objects = pd.read_csv(folder_museum_data + "---museum-objects-csv-file---")

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

# Embed museum object descriptions
print(museum_objects["Brief Description"])
embeddings_sbert_mpnet = model_sbert_mpnet.encode(museum_objects["Brief Description"])

# Save museum object descriptions and embeddings
# see also https://www.sbert.net/examples/applications/computing-embeddings/README.html
with open(folder_museum_data + "---output-file---", "wb") as fOut:
    pickle.dump({
        'id_number': museum_objects["ID Number"],
        'brief_description': museum_objects["Brief Description"],
        'embeddings_sbert_mpnet': embeddings_sbert_mpnet
    }, fOut, protocol=pickle.HIGHEST_PROTOCOL)
