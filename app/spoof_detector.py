import torch
import torchaudio
import os
from pathlib import Path
import sys

AASIST_PATH = Path("../aasist")

# Add AASIST path to system path for importing modules
sys.path.append(str(AASIST_PATH))



def get_spoof_score(audio_path: str) -> float:
    # from inference import perform_inference
    from aasist.evaluation import evaluation

    """
    Get the spoof score for the given audio file.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file {audio_path} does not exist.")
    
    config_file = str(AASIST_PATH / "config" / "AASIST.conf")
    results = evaluation(config_file=config_file, data_path=audio_path)
    return results['score']  # Assuming 'score' is the key for the spoof score

    # Load the audio file
    # waveform, sample_rate = torchaudio.load(audio_path)
    
    # Perform inference using AASIST model
    score = perform_inference(
        # waveform, sample_rate
        model_path=str(AASIST_PATH / "weights" / "AASIST.pt"),
        audio_path=audio_path
        )
    
    return score # Higher = more likely real
    # return score.item()  # Return as a Python float
