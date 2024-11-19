# Code

This folder includes the code used in *iteration 2* of the project. 

To execute the code in the `code` folder, first create the conda environment provided in `conda-env_whisper-cuda-12-1.yml` file in the `utils` folder for the automated transcription using the `001_whisper_transcript.py` and the environment provided in `conda-env_llm-cuda-12-1.yml` file for all the other scripts and notebook. Then, make a copy of the `local_dir_setup--example.py` file in the `code` folder and rename it to `local_dir_setup.py`. Modify the paths in the `local_dir_setup.py` file to match the location of your main storage, scratch and model cache folder in your local setup. Each script also requires the user to set the correct folder and file names within the scripts.

Run the scripts following their numerical order, making sure to first set the correct folder and file names within the scripts as well.