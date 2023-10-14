import aiogram


async def user_start(message: aiogram.types.Message):
    await message.reply("Hello, user! Send me a voice message and I'll try to recognize it and answer you.")


def register_user(dp: aiogram.Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
