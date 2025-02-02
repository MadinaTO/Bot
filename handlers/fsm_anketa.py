from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keybords import client_kb


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    gender = State()
    region = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.name.set()
        await message.answer('Name?', reply_markup=client_kb.cancel_markup)
    else:
        await message.answer('Talk face to face')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = message.from_user.username
        data['name'] = message.text
        print(data)
    await FSMAdmin.next()
    await message.answer('Age?', reply_markup=client_kb.cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Only numbers!")
    elif not 17 < int(message.text) < 100:
        await message.answer("Access is restricted!")
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer("Gender?",
                             reply_markup=client_kb.gender_markup)


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await FSMAdmin.next()
    await message.answer("Where are u from?", reply_markup=client_kb.cancel_markup)


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    await FSMAdmin.next()
    await message.answer("Your photo", reply_markup=client_kb.cancel_markup)


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await message.answer_photo(
            data["photo"],
            caption=f"{data['name']} {data['age']} {data['gender']} "
                    f"{data['region']}\n\n{data['username']}"
        )
    await FSMAdmin.next()
    await message.answer("Все верно?",
                         reply_markup=client_kb.submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "yeah":
        await message.answer("Bye", reply_markup=client_kb.start_markup)
        await state.finish()
    elif message.text.lower() == "repeat":
        await FSMAdmin.name.set()
        await message.answer("Name?", reply_markup=client_kb.cancel_markup)
    else:
        await message.answer('What!?')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Canceled", reply_markup=client_kb.start_markup)


def register_handlers_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_reg,
                                Text(equals="cancel", ignore_case=True),
                                state="*")

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_region, state=FSMAdmin.region)
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(submit, state=FSMAdmin.submit)
