# Whisper ASR Utilities (supports openai-whisper or faster-whisper)
import os
import re
from typing import Tuple

def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[a-z0-9\\u0900-\\u0d7f\\s]+', ' ', text) # Keep latin and indic ranges
    text = re.sub(r'\\s+',' ', text) # Normalize whitespace
    return text.strip()

def similarity(a: str, b: str) -> float:
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()

def _load_faster_whisper():
    from faster_whisper import WhisperModel
    model_name = os.getenv('WHISPER_MODEL', 'small')
    return WhisperModel(model_name, device="auto")

def _load_telugu_whisper():
    # import torch
    # from transformers import pipeline

    # device = "cpu"

    # transcribe = pipeline(task="automatic-speech-recognition", model="vasista22/whisper-telugu-base", chunk_length_s=30, device=device)
    # transcribe.model.config.forced_decoder_ids = transcribe.tokenizer.get_decoder_prompt_ids(language="te", task="transcribe")

    # return transcribe

    import jax.numpy as jnp
    from whisper_jax import FlaxWhisperForConditionalGeneration, FlaxWhisperPipline

    transcribe = FlaxWhisperPipline("vasista22/whisper-telugu-base", batch_size=16)
    transcribe.model.config.forced_decoder_ids = transcribe.tokenizer.get_decoder_prompt_ids(language="te", task="transcribe")
    return transcribe

_whisper_impl = os.getenv("WHISPER_IMPL", "faster")
_model_cache = None

def transcribe(audio_path: str, language: str = None) -> str:
    global _model_cache
    if language == "te":
        te_transcribe = _load_telugu_whisper()

        transcription = te_transcribe(audio_path)["text"]
        print('Telugu transcription: ', transcription)
        return transcription
    
    if _whisper_impl == "faster":
        if _model_cache is None:
            _model_cache = _load_faster_whisper()
        model = _model_cache
        segments, _ = model.transcribe(audio_path, language=language)
        return ' '.join([segment.text for segment in segments]).strip()
    # else:
    #     import whisper
    #     model = whisper.load_model(os.getenv('WHISPER_MODEL', 'small'))
    #     result = model.transcribe(audio_path, language=language)
    #     return result['text']

def verify_phrase(audio_path: str, expected_phrase: str, langauge: str = None, thresh: float = 0.80) -> Tuple[bool, float, str]:
    text = transcribe(audio_path, langauge)
    sim = similarity(text, expected_phrase)
    return sim >= thresh, sim, text
