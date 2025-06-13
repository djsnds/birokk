from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from settings import telegram_key
from gigachad.giga import agent, memorysave
from langchain_core.runnables import RunnableConfig
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import FSInputFile

dp = Dispatcher()
bot = Bot(token=telegram_key)


@dp.message(Command("start"))
async def start_bot(message: types.Message):
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/start")], [KeyboardButton(text="/reset")]],
        resize_keyboard=True,
    )

    welcome_text = """
    🌟 <b>Добро пожаловать в Биробиджанский колледж культуры и искусств, я умный помощник абитуриента!</b> 🌟

    Я помогу вам с поступлением и отвечу на все вопросы.

    ✨ <b>Чем я могу помочь?</b> ✨

    🎓 <b>Специальности</b> - Расскажу о всех направлениях набора
    📑 <b>Документы и условия</b> - Объясню что нужно подготовить
    🎭 <b>Вступительные испытания</b> - Дату и формат испытаний
    📝 <b>Шаблон заявления</b> - Отправлю готовый образец
    ⏳ <b>Контроль сроков</b> - Уведомлю за несколько дней до окончания приёма документов
    📊 <b>Конкурсная аналитика</b> - Подписка на еженедельную рассылку конкурсной аналитики

    🔹 <b>Как начать?</b> Просто спросите:
    • "Назови мне все специальности?"
    • "Какие вступительные испытания по специальности - Музыкальное образование?"
    • "Что нужно для поступления?"
    • "Дай шаблон заявления на поступление"
    • "Хочу получать еженедельную информацию с конкурсной аналитикой/Отпиши меня от рассылки"
    • "Отправь мне списки на зачисление в колледж"

    📌 <i>Уже выбрали направление? Назовите его - расскажу детали!</i>

    📞 <b>Приемная комиссия:</b>
    ☎ Телефоны:
    • <code>8 (42622) 2-17-44</code>
    • <code>+7 914 015-54-48</code>
    ✉ E-mail: <code>coolbokk@post.eao.ru</code>

    Для сброса диалога нажмите /reset
    """

    await message.answer(text=welcome_text, reply_markup=menu, parse_mode="HTML")


@dp.message(Command("reset"))
async def reset_memory(message: types.Message):
    if not message.from_user:
        await message.answer(
            "Извините, я работаю только в личных чатах с пользователями."
        )
        return
    user_id = str(message.from_user.id)

    memorysave.delete_thread(user_id)
    await message.answer("Контекст Gigachat возобновлен! Чем могу помочь?")


@dp.message(F.text)
async def handle_message(message: types.Message):
    if not message.from_user:
        await message.answer(
            "Извините, я работаю только в личных чатах с пользователями."
        )
        return
    user_id = str(message.from_user.id)

    result = await agent.ainvoke(
        {"messages": [("user", message.text)]},
        RunnableConfig(configurable={"thread_id": user_id}),
    )

    response = result["messages"][-1].content

    if response.endswith(".docx"):
        try:
            docx_file = FSInputFile(response)
            await message.answer_document(docx_file)
        except Exception as e:
            await message.answer(f"Произошла ошибка при отправке файла: {e}")
    else:

        await message.answer(response)


async def on_shutdown():
    await bot.session.close()
    await dp.storage.close()


async def run_tg():
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()
