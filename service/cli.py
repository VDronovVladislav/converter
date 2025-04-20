import argparse

def configure_argument_parser():
    """Функция-конфигуратор парсера агрументов командной строки."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--rub", help="Количество рублей", type=float, default=0.0)
    parser.add_argument("--usd", help="Количество долларов", type=float, default=0.0)
    parser.add_argument("--eur", help="Колиество евро", type=float, default=0.0)
    parser.add_argument("--period", help="Период в минутах", type=int, default=1)
    parser.add_argument(
        "--debug",
        help="Включить отладку (выводить содержимое `request`/`response` веб-сервера в консоль)",
        choices=["0", "1", "true", "false", "True", "False", "y", "n", "Y", "N"],
        default="false",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Дефолтный хост")
    parser.add_argument("--port", default=8000, help="Дефолтный порт")
    return parser