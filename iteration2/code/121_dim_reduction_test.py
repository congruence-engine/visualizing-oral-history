# Dimensionality reduction tests
# This script is used to reduce the dimensionality of the embeddings to 2
# and check the quality of the UMAP output using scatterplot and density plots
# Depends on:
#     code/analysis/101_segments_embeddings.py

# Local setup
from local_dir_setup import *

# Libraries
# Core libraries
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pickle
# NLP
import torch
from umap import UMAP


# Set device
if torch.cuda.is_available():
    print('Run on CUDA')
    print(f'Device count: {torch.cuda.device_count()}')
    print(f'Current device: {torch.cuda.current_device()}')
    print(f'Current device name: {torch.cuda.get_device_name(torch.cuda.current_device())}')
else:
    print('Run on CPU')

# Setup and folders
folder_embeddings = dir_scratch + "---input-folder---"
folder_plots = dir_scratch + "---output-folder---"
os.mkdir(folder_plots)

# Load data
with open(folder_embeddings + "---transcripts-embeddings-file---", "rb") as fIn:
    stored_data = pickle.load(fIn)
    embeddings_sbert_mpnet = stored_data['embeddings_sbert_mpnet']

for i in range(10):
    for j in range(2):
        umap_neighbors = 2**(i+1) + (j * 2**(i))
        print(f'Dimensionality reduction using UMAP, n_neighbors={umap_neighbors}')

        # Model
        reducer = UMAP(n_neighbors=umap_neighbors, n_components=2, min_dist=0.0, metric='cosine')

        # Calculate reduced embeddings
        reduced_embeddings = reducer.fit_transform(embeddings_sbert_mpnet)

        # Scatterplot
        plt.scatter(
            reduced_embeddings[:, 0],
            reduced_embeddings[:, 1],
            s=3
        )
        plt.gca().set_aspect('equal', 'datalim')
        plt.title(f"Plot embeddings for n_neighbors={umap_neighbors}")
        # Figure size 40 cm x 40 cm
        plt.gcf().set_size_inches(40 / 2.54, 40 / 2.54)
        plt.savefig(folder_plots + f'/embeddings-sbert-mpnet_reduced_{umap_neighbors:04}nn.png', dpi=300)
        plt.clf()

        # Density plot
        plt.hist2d(
            reduced_embeddings[:, 0],
            reduced_embeddings[:, 1],
            bins=200, norm=LogNorm()
        )
        plt.colorbar()
        plt.gca().set_aspect('equal', 'datalim')
        plt.title(f"Plot for summaries embeddings n_neighbors={umap_neighbors}")
        # Figure size 40 cm x 40 cm
        plt.gcf().set_size_inches(40 / 2.54, 40 / 2.54)
        plt.savefig(folder_plots + f'/embeddings-sbert-mpnet__reduced_{umap_neighbors:04}nn_density.png', dpi=300)
        plt.clf()

        del reducer, reduced_embeddings