from aiogram.dispatcher.router import Router
from aiogram.filters.command import Command
from aiogram.types.message import Message
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

router = Router()


@router.message(Command("start", "help"))
async def start_message(message: Message):
    await message.reply(
        text="👋 Привет! Я создан чтобы проверить твой уровень владения английского.\n\n"
             "Я думаю уже стоит начинать. Поэтому используй команду /tests! Удачи 🤝",
    )


@router.message(Command("tests"))
async def tests_message(message: Message):
    kb = [
        [
            KeyboardButton(
                text="Test A2",

            ),
            KeyboardButton(
                text="Test A1"
            )
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите уровень теста"
    )

    await message.answer(
        text="Вам были предложены уровни теста, выберите один.",
        reply_markup=keyboard
    )
