import torch
from pyannote.audio import Pipeline


def diarize(path, token, model="pyannote/speaker-diarization-3.1", device="mps"):
    pipeline = Pipeline.from_pretrained(model, use_auth_token=token)
    pipeline.to(torch.device(device))

    diarization = pipeline(path)

    ret = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        ret.append({"start": turn.start, "stop": turn.end, "speaker": speaker})
    return ret
