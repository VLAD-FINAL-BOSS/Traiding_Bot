from aiogram import Router, F
from aiogram.types import Message
from scripts.get_currency_price import get_current_price
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

# Добавим класс состояния
class PriceState(StatesGroup):
    waiting_for_tickers = State()


@router.message(F.text.startswith("/price"))
async def start_price_handler(message: Message, state: FSMContext):
    await message.answer("Введите инструменты через запятую:", parse_mode="Markdown")

    # Переводим в состояние ожидания тикеров
    await state.set_state(PriceState.waiting_for_tickers)

@router.message(PriceState.waiting_for_tickers)
async def price_handler(message: Message, state: FSMContext):
    try:

        tickers = message.text.strip().upper().split(",")
        tickers = [ticker.strip() for ticker in tickers if ticker.strip()]

        if not tickers:
            await message.answer("Ошибка: не введено ни одного тикера!")
            return

        quotes = get_current_price(tickers)

        if quotes:
            current_time = datetime.now().strftime("%H:%M:%S")
            await message.answer(f"\n{current_time} Котировки:")
            for ticker, price in quotes.items():
                await message.answer(f"{ticker}: {price} руб.")
        else:
            await message.answer("⚠️ Не удалось получить данные. Неверный ввод тикеров")

    except Exception as e:
        await message.answer("⚠️ Ошибка обработки команды. Использование: /price TICKER")

    # Завершаем состояние
    await state.clear()
