from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    row_width=2
)

start_button = KeyboardButton('/start')
info_button = KeyboardButton('/info')
quiz_button = KeyboardButton('/quiz')
reg_button = KeyboardButton("/reg")

share_location = KeyboardButton('Share location', request_location=True)
share_contact = KeyboardButton('Share contact', request_contact=True)
user = KeyboardButton('user', request_user=None)


start_markup.add(start_button, info_button, quiz_button, reg_button,
                 share_location, share_contact, user)


cancel_button = KeyboardButton("CANCEL")

submit_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(
    KeyboardButton("Yeah"),
    KeyboardButton("Repeat"),
    cancel_button
)


gender_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(
    KeyboardButton("Man"),
    KeyboardButton("Woman"),
    KeyboardButton("Dont know"),
    cancel_button
)

cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(
    cancel_button
)
