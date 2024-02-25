import json

from transformers import pipeline
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import torch

from insanely_fast_whisper.utils.diarization_pipeline import diarize
from insanely_fast_whisper.utils.result import build_result


def transcribe(model_name, file_name, transcript_path, device_id, batch_size, timestamp, hf_token, language, task,):
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_name,
        torch_dtype=torch.float16,
        device="mps" if device_id == "mps" else f"cuda:{device_id}",
        model_kwargs={"attn_implementation": "flash_attention_2"} if args.flash else {"attn_implementation": "sdpa"},
    )

    if args.device_id == "mps":
        torch.mps.empty_cache()
    # elif not args.flash:
    # pipe.model = pipe.model.to_bettertransformer()

    ts = "word" if args.timestamp == "word" else True

    language = None if args.language == "None" else args.language

    generate_kwargs = {"task": args.task, "language": language}

    if args.model_name.split(".")[-1] == "en":
        generate_kwargs.pop("task")

    with Progress(
            TextColumn("🤗 [progress.description]{task.description}"),
            BarColumn(style="yellow1", pulse_style="white"),
            TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Transcribing...", total=None)

        outputs = pipe(
            args.file_name,
            chunk_length_s=30,
            batch_size=args.batch_size,
            generate_kwargs=generate_kwargs,
            return_timestamps=ts,
        )

    if args.hf_token != "no_token":
        speakers_transcript = diarize(args, outputs)
        with open(args.transcript_path, "w", encoding="utf8") as fp:
            result = build_result(speakers_transcript, outputs)
            json.dump(result, fp, ensure_ascii=False)

        print(
            f"Voila!✨ Your file has been transcribed & speaker segmented go check it out over here 👉 {args.transcript_path}"
        )
    else:
        with open(args.transcript_path, "w", encoding="utf8") as fp:
            result = build_result([], outputs)
            json.dump(result, fp, ensure_ascii=False)

        print(
            f"Voila!✨ Your file has been transcribed go check it out over here 👉 {args.transcript_path}"
        )
