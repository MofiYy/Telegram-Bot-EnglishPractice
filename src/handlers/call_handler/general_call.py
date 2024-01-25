from asyncio import sleep

from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.types.message import Message
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.callback_query import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from src.variables.questions import questions

router = Router()


_score: int = 0
_current_questions: int = 1


async def send_question(message: Message):
    question = (questions[str(_current_questions)])
    options = "\n".join([f"{i}) {option}" for i, option in enumerate(question["options"], start=1)])

    buttons = [InlineKeyboardButton(text=option, callback_data=option) for option in question["options"]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

    await message.answer(
        text=f"{question['question']}\n{options}",
        reply_markup=keyboard
    )


@router.message(F.text)
async def handler_message(message: Message):
    global _score, _current_questions
    if message.text == "Test A2":
        _score = 0
        _current_questions = 1
        await message.reply(
            text="Получаем данный о тесте, у вас есть 5 секунд чтобы подготовиться."
        )
        await sleep(5.0)
        await send_question(message=message)
    elif message.text == "Test A1":
        await message.reply(
            text="Приносим свои извинения, но в данный сейчас не доступен."
        )


@router.callback_query()
async def process_callback_answer(callback_query: CallbackQuery):
    global _score, _current_questions

    question = questions[str(_current_questions)]

    try:
        if callback_query.data == question["answer"]:
            _score += 1
            await callback_query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="✅", callback_data="correct_answer"
                            )
                        ]
                    ]
                )
            )
        else:
            await callback_query.message.edit_reply_markup(
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="❌", callback_data="wrong_answer")
                        ]
                    ]
                )
            )
            await callback_query.message.answer(
                text=f"Ваш ответ не правильный, правильный ответ: {question['answer']}"
            )

        if _current_questions < len(questions):
            _current_questions += 1
            await send_question(message=callback_query.message)
        else:
            percent_score = round((_score / 5) * 100)
            await callback_query.message.answer(
                text=f"🎉 Поздравляем!\n"
                     f"Вы успешно прошли тест на: {percent_score}% из 100%\n\n"
                     f"- Всего вопросов: {len(questions)}\n"
                     f"- Правильных ответов: {_score}"
            )
    except TelegramBadRequest:
        ...
