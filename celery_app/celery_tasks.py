from langchain_gigachat.chat_models import GigaChat
from settings import gigachat_key
from celery_app.celery_app import celery_app
from langchain_core.messages import HumanMessage, SystemMessage
from utils import extract_data
import telebot
from settings import telegram_key

celery_sync_bot = telebot.TeleBot(telegram_key)


@celery_app.task(
    name="send_notification",
    bind=True,
    max_retries=1,
)
def send_notification(self, user_id: str, day: int) -> None:
    print("функция send_notification вызвалась")
    text = f"Напоминаем, что через {day} суток заканчивается прием документов"
    try:
        celery_sync_bot.send_message(chat_id=user_id, text=text)
        print(f"Пользователь {user_id} получил уведомление")
    except Exception as exc:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {exc}")
        self.retry(exc=exc, countdown=5)


@celery_app.task(
    name="send_information",
    bind=True,
    max_retries=1,
)
def send_information(self, user_id: str) -> None:
    data = extract_data("docs/competition.txt")
    giga = GigaChat(
        credentials=gigachat_key,
        model="GigaChat",
        verify_ssl_certs=False,
        timeout=1200,
    )
    messages = [
        SystemMessage(content="Ты умный аналитик"),
        HumanMessage(
            content=(
                f"""
                Твоя задача дать краткую аналитику конкурса по всем направлениям на основе данных.\n
                Данные:\n\n{data}"""
            )
        ),
    ]
    res = giga.invoke(messages)
    messages.append(res)
    try:
        if user_id:
            celery_sync_bot.send_message(chat_id=user_id, text=str(res.content))
    except Exception as exc:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {exc}")
        self.retry(exc=exc, countdown=5)


@celery_app.task(
    name="send_admission_list",
    bind=True,
    max_retries=1,
)
def send_admission_list(self, user_id: str) -> None:
    print("функция send_notification вызвалась")
    try:
        with open("docs/admission_list.docx", "rb") as file:
            celery_sync_bot.send_document(chat_id=user_id, document=file)
        print(f"Пользователь {user_id} получил уведомление")
    except Exception as exc:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {exc}")
        self.retry(exc=exc, countdown=5)
