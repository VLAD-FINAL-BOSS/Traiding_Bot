import requests
import time
from threading import Thread
import asyncio
from constants import URL


class SilentMoexPriceAlert:
    def __init__(self, bot=None, chat_id=None):
        self.alerts = {}
        self.running = False
        # self.bot = bot
        self.chat_id = chat_id
        # self.loop = asyncio.new_event_loop() if bot else None

    def add_alert(self, chat_id, ticker, price, direction):
        if chat_id not in self.alerts:
            self.alerts[chat_id] = {}
        if ticker not in self.alerts[chat_id]:
            self.alerts[chat_id][ticker] = []
        self.alerts[chat_id][ticker].append({
            'price': float(price),
            'direction': direction.lower(),
            'triggered': False
        })

    def check_price(self, ticker):
        """Получает текущую цену акции с MOEX ISS API"""
        params = {
            "iss.meta": "off",
            "securities": ticker,
            "marketdata.columns": "SECID,LAST"
        }

        try:
            response = requests.get(URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            marketdata = data["marketdata"]["data"]
            return float(marketdata[0][1]) if marketdata and marketdata[0][1] else None
        except Exception:
            return None

    def stop_monitoring(self):
        """Останавливает мониторинг"""
        self.running = False

    def check_alerts_once(self):
        """Проверяет все тикеры один раз и возвращает список сработавших алертов"""
        messages = {}
        for chat_id, user_alerts in self.alerts.items():
            for ticker in list(user_alerts.keys()):
                price = self.check_price(ticker)
                if price is None:
                    continue

                for alert in user_alerts[ticker]:
                    if alert['triggered']:
                        continue

                    condition_met = (
                            (alert['direction'] == 'long' and price >= alert['price']) or
                            (alert['direction'] == 'short' and price <= alert['price'])
                    )

                    if condition_met:
                        alert['triggered'] = True
                        direction = "выше" if alert['direction'] == 'long' else "ниже"
                        message = (
                            f"🔔 АЛЕРТ! {ticker} достиг {alert['price']} руб. "
                            f"(текущая цена {price} руб., движение {direction} уровня)"
                        )
                        messages.setdefault(chat_id, []).append(message)

        return messages

    def get_alerts_summary(self, chat_id):
        """Возвращает текст со списком активных алертов пользователя"""
        if chat_id not in self.alerts or not self.alerts[chat_id]:
            return "🔕 У вас нет активных заявок."

        lines = ["📋 Ваши заявки:"]
        for ticker, alerts in self.alerts[chat_id].items():
            for alert in alerts:
                if not alert["triggered"]:
                    direction = "long" if alert["direction"] == "long" else "short"
                    lines.append(f"— {ticker}: {alert['price']} ₽ ({direction})")

        return "\n".join(lines) if len(lines) > 1 else "🔕 Все заявки уже сработали."
