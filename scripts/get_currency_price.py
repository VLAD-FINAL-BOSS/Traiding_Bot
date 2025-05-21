
import requests
from datetime import datetime
from constants import URL

def get_current_price(securities: list):
    """
    Получает текущие котировки 2-х и более заданных инструментов через API ИСС
    """
    params = {
        "iss.meta": "off",
        "securities": ",".join(securities),
        "marketdata.columns": "SECID,LAST"
    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Парсим ответ
        marketdata = data["marketdata"]["data"]
        quotes = {}
        for item in marketdata: # Каждый item в списке — это массив вида ['SBER', 280.50].
            ticker = item[0]
            last_price = item[1]
            quotes[ticker] = last_price if last_price is not None else "Данные не найдены"

        return quotes

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def main():
    print("Программа для получения котировок с Московской Биржи")
    print("Введите инструменты через запятую:")

    tickers = input("> ").strip().upper().split(",")
    tickers = [ticker.strip() for ticker in tickers if ticker.strip()]  # Удаляем пустые значения

    if not tickers:
        print("Ошибка: не введено ни одного тикера!")
        return

    quotes = get_current_price(tickers)
    if quotes:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\n{current_time} Котировки:")
        for ticker, price in quotes.items():
            print(f"{ticker}: {price} руб.")
    else:
        print("Не удалось получить данные. Проверьте тикеры или подключение к сети.")
