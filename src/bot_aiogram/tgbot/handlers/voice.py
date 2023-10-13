import io
import typing

import aiogram
import aiohttp

import tgbot.settings as tgbot_settings


async def voice_response(message_voice: aiogram.types.Message):
    config = typing.cast(tgbot_settings.Settings, message_voice.bot.get("config"))

    voice_file_id: str = message_voice.voice.file_id
    file_info = await message_voice.bot.get_file(voice_file_id)
    file_path: str = file_info.file_path
    voice_data: io.BytesIO = io.BytesIO()
    voice_data.name = "voice.ogg"
    voice_data.seek(0)

    await message_voice.bot.download_file(file_path, destination=voice_data)
    await message_voice.bot.send_chat_action(message_voice.from_user.id, "typing")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{config.api.api_url}/api/v1/voice/",
            data={"voice": voice_data},
        ) as resp:
            if resp.status == 200:
                voice_answer: bytes = await resp.read()
                answer_io = io.BytesIO(voice_answer)
                answer_io.name = "answer_io.ogg"

                await message_voice.bot.send_chat_action(
                    message_voice.from_user.id, action=aiogram.types.ChatActions.RECORD_AUDIO
                )

                try:
                    await message_voice.answer_voice(voice=answer_io)
                except aiogram.exceptions.BadRequest:
                    await message_voice.answer(
                        "We were unable to send you a voice message. Please check your privacy settings."
                    )
            else:
                await message_voice.answer("Not recognized text")
        await session.close()
    return


def register_voice_response(dp: aiogram.Dispatcher):
    dp.register_message_handler(voice_response, content_types=aiogram.types.ContentType.VOICE)
