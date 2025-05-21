import asyncio
from aiogram import Bot, Dispatcher
from constants import TG_BOT_TOKEN
from handlers import start, price, alerts
from handlers.alerts import alert_monitoring_task


async def main():
    bot = Bot(token=TG_BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(start.router, price.router, alerts.router)

    # Запускаем фоновую задачу мониторинга алертов
    asyncio.create_task(alert_monitoring_task(bot))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())