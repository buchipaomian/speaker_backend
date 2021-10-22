import deepspeech
import numpy as np
import wave
model_file_path = 'checkpoint\deepspeech\deepspeech-0.9.3-models.pbmm'
scorer_file_path = 'checkpoint\deepspeech\deepspeech-0.9.3-models.scorer'
def load_model(scorer_activate=False):
    model = deepspeech.Model(model_file_path)
    if scorer_activate:
        model.enableExternalScorer(scorer_file_path)
        lm_alpha = 0.75
        lm_beta = 1.85
        model.setScorerAlphaBeta(lm_alpha, lm_beta)
        beam_width = 500
        model.setBeamWidth(beam_width)
    return model

def speech_to_text(audio_file_path,model):
    w = wave.open(audio_file_path, 'r')
    rate = w.getframerate()
    frames = w.getnframes()
    buffer = w.readframes(frames)
    # print(rate)
    # print(model.sampleRate())
    data16 = np.frombuffer(buffer, dtype=np.int16)
    type(data16)
    text = model.stt(data16)
    return text

model = load_model()