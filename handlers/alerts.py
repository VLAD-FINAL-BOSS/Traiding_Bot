from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from scripts.level_price_alert import SilentMoexPriceAlert
import asyncio

router = Router()
alert_system = SilentMoexPriceAlert()
subscribed_users = set()
class AlertState(StatesGroup):
    waiting_for_alert_data = State()



@router.message(F.text.startswith("/add_alert"))
async def start_alert_handler(message: Message, state: FSMContext):

    await message.answer(
        "📥 Добавление стоп-уровней (формат: тикер цена long/short)\n"
        "Пример: `GAZP 160 short` — сработает, если цена опустится ниже 160\n"
        "Пример: `SBER 300 long` — сработает, если цена поднимется выше 300",
        parse_mode="Markdown"
    )
    await state.set_state(AlertState.waiting_for_alert_data)


@router.message(AlertState.waiting_for_alert_data)
async def add_alert_handler(message: Message, state: FSMContext):
    try:
        parts = message.text.strip().split()
        if len(parts) != 3:
            await message.answer("⚠️ Неверный формат. Введите: `ТИКЕР ЦЕНА long/short`", parse_mode="Markdown")
            return

        ticker, price, direction = parts
        if direction.lower() not in ("long", "short"):
            await message.answer("⚠️ Направление должно быть `long` или `short`", parse_mode="Markdown")
            return

        alert_system.add_alert(chat_id=message.chat.id, ticker=ticker.upper(), price=price, direction=direction.lower())
        subscribed_users.add(message.chat.id)  # Сохраняем пользователя
        await message.answer(f"✅ Алерт добавлен: {ticker.upper()} {direction.lower()} {price} ₽")
    except Exception:
        await message.answer("⚠️ Ошибка при добавлении алерта")
    finally:
        await state.clear()

# ✅ Фоновая задача для отправки алертов
async def alert_monitoring_task(bot):
    while True:
        try:
            alert_messages = alert_system.check_alerts_once()
            for chat_id, messages in alert_messages.items():
                for msg in messages:
                    await bot.send_message(chat_id, msg)
        except Exception as e:
            print("Ошибка в alert_monitoring_task:", e)
        await asyncio.sleep(10)  # проверка каждые 10 сек

@router.message(F.text == "/my_alerts")
async def show_alerts_handler(message: Message):
    summary = alert_system.get_alerts_summary(chat_id=message.chat.id)
    await message.answer(summary)
