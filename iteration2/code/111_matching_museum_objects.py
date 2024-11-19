# This script is designed to calculate all similarities between
# the embeddings created for the transcript sections and
# the embeddings created for the museum object descriptions
# one-by-one to minimise memory usage so that it can be run on a normal laptop
# (takes longer).
# Depends on:
#     code/analysis/101_segments_embeddings.py
#     code/analysis/102_museum_objects_embeddings.py

# Local setup
from local_dir_setup import *

# Libraries
import pandas as pd
import pickle
from sentence_transformers import util

# Setup
file_trans_mpnet = dir_scratch + "---transcripts-embeddings-file---" # Folder with the embeddings from 101_segments_embeddings.py
file_museum_mpnet = dir_scratch + "---museum-objects-embeddings-file---" # Folder with the embeddings from 102_museum_objects_embeddings.py
folder_similarities_output = dir_scratch + "---output-folder---"

# Load embeddings
# see also https://www.sbert.net/examples/applications/computing-embeddings/README.html

with open(file_trans_mpnet, "rb") as fIn:
   data_trans_mpnet = pickle.load(fIn)
   trans_id_mpnet = data_trans_mpnet['transcript']
   trans_start_id_mpnet = data_trans_mpnet['start_id']
   trans_start_time_mpnet = data_trans_mpnet['start_time']
   trans_end_id_mpnet = data_trans_mpnet['end_id']
   trans_end_time_mpnet = data_trans_mpnet['end_time']
   trans_text_mpnet = data_trans_mpnet['text']
   trans_embeddings_mpnet = data_trans_mpnet['embeddings_sbert_mpnet']

with open(file_museum_mpnet, "rb") as fIn:
   data_museum_mpnet = pickle.load(fIn)
   museum_id_mpnet = data_museum_mpnet['id_number']
   museum_desc_mpnet = data_museum_mpnet['brief_description']
   museum_emb_mpnet = data_museum_mpnet['embeddings_sbert_mpnet']

# Save similarity matrix
with open(folder_similarities_output + "---output-csv-file---", "w", encoding="utf-8") as fOut:
    fOut.write("trans_id,trans_start_id,trans_end_id,museum_id,similarity_mpnet\n")

    for trans_idx in range(len(trans_embeddings_mpnet)):
        print(trans_idx)
        for museum_idx in range(len(museum_emb_mpnet)):

            # Compute similarity
            similarity = util.cos_sim(trans_embeddings_mpnet[trans_idx], museum_emb_mpnet[museum_idx])

            # Save row
            similarity_row = "\"" + str(trans_id_mpnet[trans_idx]) + "\"," + \
                str(int(trans_start_id_mpnet[trans_idx])) + "," + str(int(trans_end_id_mpnet[trans_idx])) + "," + \
                "\"" + str(museum_id_mpnet[museum_idx]) + "\"," + \
                str(similarity.numpy()[0, 0]) + "\n"
            fOut.write(similarity_row)
