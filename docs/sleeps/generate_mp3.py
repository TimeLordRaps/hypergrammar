#!/usr/bin/env python3
"""Generate docs/days/04092026.mp3 from narration text using VoxCPM2.

Strategy:
  - Split text into chunks at the 8192-token boundary.
  - Chunk 1: generate_streaming with voice-design style descriptor.
    Collect all audio, write to output file, and save as reference.wav.
  - Chunks 2-N: generate_streaming with reference_wav_path pointing to
    chunk 1's audio, so all subsequent chunks share the identical voice
    timbre and prosodic style throughout.
  - Stream each chunk's audio incrementally to the output WAV file so
    memory pressure stays flat regardless of total narration length.

Usage:
    pip install voxcpm soundfile pydub
    python docs/days/generate_mp3.py

Requires ~8 GB VRAM (NVIDIA GPU with CUDA 12+).
"""

import os
import pathlib
import re
import tempfile

import numpy as np
import soundfile as sf
from voxcpm import VoxCPM

VOICE_STYLE = (
    "(A deep, calm, close male voice; dark-lux bedtime tone, velvety and soothing, "
    "west coast sandman vibe, soft sandalwood warmth, light ocean mist, relaxed tide-like rhythm, "
    "slow pacing, gentle breath, clean low resonance, comforting, dreamy, hypnotic, safe, elegant, "
    "midnight shoreline ambience) "
)

DAYS_DIR = pathlib.Path(__file__).parent
TEXT_FILE = DAYS_DIR / "04092026.md"
WAV_FILE = DAYS_DIR / "04092026.wav"
MP3_FILE = DAYS_DIR / "04092026.mp3"

# Approximate max words per generation pass to stay under the 8192-token
# sequence length limit (the model's "LM Token Rate" is 6.25 Hz).
# ~600 words ≈ ~780 tokens — well inside the limit with margin.
CHUNK_WORDS = 600


def split_into_chunks(text: str, max_words: int) -> list[str]:
    """Split narration text at paragraph boundaries into chunks under max_words."""
    paragraphs = [p.strip() for p in re.split(r"\n\n+", text) if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_count = 0

    for para in paragraphs:
        para_words = para.split()
        if current_count + len(para_words) > max_words and current:
            chunks.append(" ".join(current))
            current = list(para_words)
            current_count = len(para_words)
        else:
            current.extend(para_words)
            current_count += len(para_words)

    if current:
        chunks.append(" ".join(current))

    return chunks


def stream_to_array(model: "VoxCPM", **kwargs) -> np.ndarray:
    """Call generate_streaming, collect all chunks, return concatenated array."""
    parts = []
    for chunk in model.generate_streaming(**kwargs):
        parts.append(chunk)
    return np.concatenate(parts) if parts else np.array([], dtype=np.float32)


def main() -> None:
    print("Loading narration text...")
    raw_text = TEXT_FILE.read_text(encoding="utf-8")
    total_words = len(raw_text.split())
    print(f"  {total_words:,} words ({total_words / 130:.1f} min at 130 wpm)")

    chunks = split_into_chunks(raw_text, CHUNK_WORDS)
    print(f"  Split into {len(chunks)} generation chunks")

    print("Loading VoxCPM2 model (openbmb/VoxCPM2)...")
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)
    sample_rate = model.tts_model.sample_rate
    print(f"  Sample rate: {sample_rate} Hz")

    # Temp file to hold the reference audio from chunk 1 for voice cloning.
    reference_wav = pathlib.Path(tempfile.mktemp(suffix="_ref.wav"))

    print(f"Writing output WAV → {WAV_FILE.name}...")
    total_samples = 0

    with sf.SoundFile(str(WAV_FILE), mode="w", samplerate=sample_rate, channels=1) as out_f:
        for i, chunk in enumerate(chunks, 1):
            word_count = len(chunk.split())
            print(f"  Streaming chunk {i}/{len(chunks)} ({word_count} words)...")

            if i == 1:
                # First chunk: use voice-design style descriptor.
                audio = stream_to_array(
                    model,
                    text=VOICE_STYLE + chunk,
                    cfg_value=2.0,
                    inference_timesteps=10,
                )
                # Save as reference for all subsequent chunks.
                sf.write(str(reference_wav), audio, sample_rate)
                print(f"    Reference voice saved ({len(audio) / sample_rate:.1f}s)")
            else:
                # Subsequent chunks: clone voice from chunk 1 + style control.
                audio = stream_to_array(
                    model,
                    text=VOICE_STYLE + chunk,
                    reference_wav_path=str(reference_wav),
                    cfg_value=2.0,
                    inference_timesteps=10,
                )

            out_f.write(audio)
            total_samples += len(audio)
            duration_so_far = total_samples / sample_rate
            print(f"    Cumulative: {duration_so_far / 60:.1f} min")

    duration_min = total_samples / sample_rate / 60
    print(f"\nFull audio: {duration_min:.1f} min at {sample_rate} Hz")

    # Clean up reference wav.
    if reference_wav.exists():
        reference_wav.unlink()

    # Convert to MP3 via pydub (requires ffmpeg on PATH).
    try:
        from pydub import AudioSegment  # type: ignore[import-untyped]

        print(f"Converting WAV → MP3 ({MP3_FILE.name}, 192 kbps)...")
        seg = AudioSegment.from_wav(str(WAV_FILE))
        seg.export(str(MP3_FILE), format="mp3", bitrate="192k")
        print("MP3 saved.")
        os.remove(WAV_FILE)
        print(f"WAV removed. Final artifact: {MP3_FILE}")
    except ImportError:
        print("pydub not installed — WAV artifact kept, MP3 conversion skipped.")
        print(f"To convert manually: ffmpeg -i {WAV_FILE} -b:a 192k {MP3_FILE}")
    except Exception as exc:  # noqa: BLE001
        print(f"MP3 conversion failed ({exc}) — WAV artifact kept.")
        print(f"To convert manually: ffmpeg -i {WAV_FILE} -b:a 192k {MP3_FILE}")

    print(f"\nDone. {duration_min:.1f} min of audio.")


if __name__ == "__main__":
    main()
