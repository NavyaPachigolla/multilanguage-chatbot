import edge_tts

async def generate_voice(
    text,
    output_file,
    voice
):

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    await communicate.save(
        output_file
    )