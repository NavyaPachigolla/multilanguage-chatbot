from faster_whisper import WhisperModel

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

def transcribe(audio_file, language):

    segments, info = model.transcribe(
        audio_file,
        language=language
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()