from aiogram import types, Dispatcher
from config import bot, ADMINS


async def ban(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer('You are not my boss')
        elif not message.reply_to_message:
            await message.answer('Команда должна быть ответом на сообщение!')
        else:
            await bot.kick_chat_member(message.chat.id,
                                       message.reply_to_message.from_user.id)
            await message.answer(f'{message.from_user.first_name} bratan kicknul '
                                 f'{message.reply_to_message.from_user.first_name}')
    else:
        await message.answer('Пиши в группу')


async def ban_2(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer('You are not my boss')
        elif not message.from_user.username:
            await message.answer('Команда должна быть @username')
        else:
            await bot.kick_chat_member(message.chat.id, message.from_user.username)
            await message.answer(f'Он вышел сам')
    else:
        await message.answer('Пиши в группу')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!/')
    dp.register_message_handler(ban_2, commands=['banban'], commands_prefix='!/')