import deepspeech
model_file_path = 'checkpoint\deepspeech\deepspeech-0.9.3-models.pbmm'
model = deepspeech.Model(model_file_path)

#scorer(not sure if useful)
scorer_file_path = 'checkpoint\deepspeech\deepspeech-0.9.3-models.scorer'

model.enableExternalScorer(scorer_file_path)

lm_alpha = 0.75
lm_beta = 1.85
model.setScorerAlphaBeta(lm_alpha, lm_beta)
beam_width = 500
model.setBeamWidth(beam_width)

import wave
filename = 'audio/2830-3980-0043.wav'
w = wave.open(filename, 'r')
rate = w.getframerate()
frames = w.getnframes()
buffer = w.readframes(frames)
print(rate)
print(model.sampleRate())
import numpy as np
data16 = np.frombuffer(buffer, dtype=np.int16)
type(data16)
text = model.stt(data16)
print(text)