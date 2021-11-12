import deepspeech
import numpy as np
import soundfile as sf
import struct
import wave
import os
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

def splitVoiceAndSave(musicFileName):
    # minimal voice value
    voiceMinValue = 0.01
    # Time interval between two sentences（second）
    voiceMaxDistanceSecond = 0.4
    # The minimum time length of a single audio（second）
    voiceMinSecond = 0.1
    sig, sample_rate = sf.read(musicFileName)
    print('loading:%s' % musicFileName)
    print("sample rate：%d" % sample_rate)
    print("time：%s" % (sig.shape[0] / sample_rate), '秒')

    # 
    inputData = sig

    dd = {}
    for k, v in enumerate(inputData):
        if abs(v) < voiceMinValue:
            dd[k] = 0
        else:
            dd[k] = v

    x = [i / sample_rate for i in range(len(inputData))]
    y = list(dd.values())

    # delect space
    for key in list(dd):
        if dd[key] == 0:
            dd.pop(key)

    # define voice distance
    voiceSignalTime = list(dd.keys())
    list1 = []
    list2 = []
    for k, v in enumerate(voiceSignalTime[:-2]):
        list2.append(v)
        if voiceSignalTime[k + 1] - v > voiceMaxDistanceSecond * sample_rate:
            list1.append(list2)
            list2 = []

    if len(list1) == 0:
        list1.append(list2)

    if len(list1) > 0 and (
            voiceSignalTime[-1] - voiceSignalTime[-2]) < voiceMaxDistanceSecond * sample_rate:
        list1[-1].append(voiceSignalTime[-2])

    voiceTimeList = [x for x in list1 if len(x) > voiceMinSecond * sample_rate]
    print('total segement：', len(voiceTimeList))
    result_audio_list = []
    for voiceTime in voiceTimeList:
        voiceTime1 = int(max(0, voiceTime[0] - 0.8 * sample_rate))
        voiceTime2 = int(min(sig.shape[0], voiceTime[-1] + 0.8 * sample_rate))
        temp_audio = inputData[voiceTime1:voiceTime2]
        temp_path = os.path.join("data",os.path.splitext(os.path.split(musicFileName)[-1])[0] + '_%d_%d_%s_split.wav' % (voiceTime1, voiceTime2, sample_rate))
        with wave.open(temp_path,"wb") as outwave:
            nchannels = 1
            sampwidth = 2
            fs = sample_rate
            data_size = len(temp_audio)
            framerate = int(fs)
            nframes = data_size
            comptype = "NONE"
            compname = "not compressed"
            outwave.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
            for v in temp_audio:
                outwave.writeframes(struct.pack('h', int(v * 64000 / 2)))
        result_audio_list.append(temp_path)
    return result_audio_list

def speech_to_text(audio_file_path,model):
    result_text_list = []
    result_audio_list = splitVoiceAndSave(audio_file_path)
    for temp_path in result_audio_list:
        with wave.open(temp_path, 'r') as w:
            rate = w.getframerate()
            frames = w.getnframes()
            buffer = w.readframes(frames)
            # print(rate)
            # print(model.sampleRate())
            data16 = np.frombuffer(buffer, dtype=np.int16)
            type(data16)
            text = model.stt(data16)
            result_text_list.append(text)
        os.remove(temp_path)
    return result_text_list

model = load_model()