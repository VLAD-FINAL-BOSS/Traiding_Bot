from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

router = Router()

# Клавиатура со списком команд
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📋 Список команд")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите команду"
)

# Обработчик команды /start
@router.message(Command("start"))
async def welcome_send(message: Message):
    await message.answer_sticker(
        "CAACAgIAAxkBAAPwaBSSG-ozMlR-Z8B0etlQkzszyR0AAiIDAAKc1ucKohGDiN2j9cs2BA")
    # await message.answer_sticker(
    #     "CAACAgIAAxkBAAP2aBSUg9Xhh9dBmO1t6C8j33_zzXIAAi8DAAKc1ucKnvFbx-60ZUc2BA")
    welcome_text = """
    📈 Привет! Я бот для мониторинга котировок акций с Московской Биржи.

    Основные команды:
    /price - Получить текущие котировки
    /add_alert - Добавить заявку на уровне (Выводить пуш-уведомление при достижении заданного уровня цены)
    /my_alerts - Показать мои текущие заявки
    /help - Руководство пользователя
    """
    await message.answer(welcome_text, reply_markup=main_keyboard)


@router.message(F.text == "📋 Список команд")
async def help_handler(message: Message):
    help_text = (
        " /price — Получить текущие котировки с Московской Биржи\n"
        " /add_alert — Добавить заявку на уровне (бот уведомит, когда цена достигнет заданного уровня)\n"
        " /my_alerts — Посмотреть список ваших активных заявок\n"
        " /help — Руководство пользователя"
    )
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text == "/help")
async def help_handler(message: Message):
    help_text = ("""
    Функционал бота позволяет:
    1) Получать текущие котировки акций с Московской Биржи\n
    2) Добавлять стоп-заявки(алерты) на определённом уровне цены (бот уведомит, когда цена достигнет заданного уровня)\n
    Для пользования командой нажмите на на ёё гиперссылку в сообщении бота, например: /price\n
    При неверном вводе котировок либо ошибке со стороны бота воспользуйтесь кнопкой на клавиатуре "📋 Список команд", 
    затем выберите истерисующую команду и повторите ввод снова\n
    Приятного пользования!
    """
    )
    await message.answer(help_text, parse_mode="HTML")