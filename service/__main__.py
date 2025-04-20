import logging
import uvicorn

from .cli import configure_argument_parser
from .schemas import Amount
from .api import create_app
from .utils import parse_debug_flag


def main():
    """Основная функция сервиса."""
    parser = configure_argument_parser()
    args = parser.parse_args()

    debug = parse_debug_flag(args.debug)
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    logging.info("Запуск сервиса...")

    initial_amount = Amount(usd=args.usd, eur=args.eur, rub=args.rub)
    app = create_app(
        period_minutes=args.period,
        initial_amount=initial_amount,
        debug=debug,
    )
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()