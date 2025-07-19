from speechbrain.pretrained import SpeakerRecognition
import torchaudio

speaker_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir = "models/ecapa"
)

def extract_embedding(audio_path):
    signal, fs = torchaudio.load(audio_path)
    # 192 / 512 dimentional vector for storing the speaker voice
    embedding = speaker_model.encode_batch(signal).squeeze().detach().numpy() # squeeze to remove extra dimensions, detach to remove gradients, numpy to convert to numpy array
    return embedding
