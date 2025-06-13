import json
import random
import uuid
from langchain.tools import tool
from gigachad.embendings import init_retriever
from langchain_core.runnables import RunnableConfig
from celery_app.celery_app import celery_app
from dbase.db import get_db
from celery_sqlalchemy_scheduler.models import (
    PeriodicTask,
    CrontabSchedule,
    PeriodicTaskChanged,
)
from settings import DATABASE_URL
from datetime import datetime, timedelta, timezone


@tool(return_direct=True)
def schedule_notification(config: RunnableConfig, day: int) -> str:
    """
    Отправляет уведомление пользователю.

    Args:
        day: int - За сколько дней до наступления события пользователь должен получить уведомление.

    """
    print("schedule_notification")
    print(type(day))
    days = int(day)
    user_id = config.get("configurable", {}).get("thread_id")
    request_time = datetime.now(timezone.utc)

    target_date = datetime(2025, 8, 8, tzinfo=timezone.utc)  # 8 августа 2025
    notification_date = (target_date - timedelta(days=days)).replace(
        hour=request_time.hour,
        minute=request_time.minute,
    )

    celery_app.send_task(
        "send_notification",
        args=[user_id, day],
        eta=notification_date,
    )

    return f"✅ Уведомление запланировано на {notification_date.strftime('%d.%m.%Y')}"


@tool(return_direct=True)
def send_admission_list(config: RunnableConfig) -> str:
    """
    Отправляет пользователю списки на зачисление в колледж.
    """
    print("send_admission_list")
    request_time = datetime.now(timezone.utc)

    user_id = config.get("configurable", {}).get("thread_id")
    target_date = datetime(2025, 8, 20, tzinfo=timezone.utc)  # 20 августа 2025
    notification_date = (target_date).replace(
        hour=request_time.hour,
        minute=request_time.minute,
    )

    celery_app.send_task(
        "send_admission_list",
        args=[user_id],
        eta=notification_date,
    )

    return "Списки на зачисление будут направлены вам сразу после их формирования и утверждения. Пожалуйста, ожидайте дальнейших уведомлений."


@tool(return_direct=True)
def subscribe_newsletter(config: RunnableConfig) -> str:
    """
    Пользователь подписывается на еженедельную рассылку с конкурсной аналитикой
    
    """
    user_id = config.get("configurable", {}).get("thread_id")
    delay_hours = random.randint(0, 23)
    print("subscribe")
    with get_db() as session:

        schedule = (
            session.query(CrontabSchedule)
            .filter_by(
                minute="0",
                hour=str(delay_hours),
                day_of_week="1",
                day_of_month="*",
                month_of_year="*",
                timezone="UTC",
            )
            .first()
        )

        if not schedule:

            schedule = CrontabSchedule(
                minute="0",  # type: ignore
                hour=str(delay_hours),  # type: ignore
                day_of_week="1",  # type: ignore
                day_of_month="*",  # type: ignore
                month_of_year="*",  # type: ignore
                timezone="UTC",  # type: ignore
            )
            session.add(schedule)

        task = PeriodicTask(
            name=f"send_info_to_{user_id}_{uuid.uuid4().hex[:8]}",  # type: ignore
            crontab=schedule,  # type: ignore
            task="send_information",  # type: ignore
            args=json.dumps([user_id]),  # type: ignore
            enabled=True,  # type: ignore
            expires=None,  # type: ignore
        )
        session.add(task)

    return "Отлично! Теперь вы в курсе всех событий!Каждую неделю мы будем делиться с вами динамикой конкурса"


@tool(return_direct=True)
def unsubscribe_newsletter(config: RunnableConfig) -> str:
    """
    Пользователь отписывается от еженедельной рассылки с конкурсной аналитикой.
    """
    user_id = config.get("configurable", {}).get("thread_id")
    print("unsubscribe")
    with get_db() as session:
        session.query(PeriodicTask).filter(
            PeriodicTask.name.like(f"send_info_to_{user_id}_%")  # type: ignore
        ).delete(synchronize_session=False)

        PeriodicTaskChanged.update_changed(
            mapper=None, connection=session.connection(), target=None
        )

    return "Вы успешно отписались от рассылки об этапах конкурса!"


@tool(return_direct=True)
def send_application_template() -> str:
    """
    Отправляет шаблон заявления на поступление в колледж.
    """
    return "docs/app_example.docx"


@tool
async def get_college_details(question: str) -> str:
    """
    Ищет информацию о колледже в векторной базе знаний.

    """
    print("get_college_details is called")
    retriever = init_retriever
    relevant_docs = await retriever.ainvoke(question)

    return str(relevant_docs) if relevant_docs else "Информация не найдена"


tools = [
    get_college_details,
    send_application_template,
    schedule_notification,
    schedule_notification,
    subscribe_newsletter,
    unsubscribe_newsletter,
    send_admission_list,
]
