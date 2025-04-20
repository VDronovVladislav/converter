# Асинхронный сервис курсов валют и портфеля

### Стек: python3.8-3.11, asyncio, argparse, logging, fastapi, pydantic, httpx

###  Запуск:
```
python3 -m service --rub 1000 --usd 2000 --eur 3000 --period 10 [--debug y/n] [--host HOST] [--port PORT]
```
#

### Пример:
```
python3 -m service --rub 1000 --usd 200 --eur 50 --period 5 --debug y --host 127.0.0.1 --port 8
```