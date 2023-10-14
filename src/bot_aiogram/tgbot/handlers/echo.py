import aiogram


async def bot_echo(message: aiogram.types.Message):
    text = ["Эхо без состояния.", "Сообщение:", message.text]

    await message.answer("\n".join(text))


def register_echo(dp: aiogram.Dispatcher):
    dp.register_message_handler(bot_echo)
