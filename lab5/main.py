import argparse
from decimal import Decimal, InvalidOperation

from num2words import num2words


def uah_number_to_words(amount: Decimal) -> str:
    """
    Функція для перетворення числового представлення грошової суми в пропис.

    Гривня виводиться прописом, копійки - цифрами.

    :param amount: Число, яке потрібно перетворити, в форматі x.yy, де x - гривні, yy - копійки.
    :raises TypeError: Якщо amount не є Decimal.
    :rtype: str
    :return: Рядок, що представляє суму прописом українською мовою.

    Приклади:

    >>> uah_number_to_words(Decimal("1234.56"))
    'Одна тисяча двісті тридцять чотири гривні 56 копійок.'

    >>> uah_number_to_words(Decimal("0.91"))
    'Нуль гривень 91 копійка.'

    >>> uah_number_to_words(Decimal("21.05"))
    'Двадцять одна гривня 5 копійок.'

    >>> uah_number_to_words(Decimal("-100000.03"))
    'Мінус сто тисяч гривень 3 копійки.'

    >>> uah_number_to_words(Decimal("999999.99"))
    "Дев'ятсот дев'яносто дев'ять тисяч дев'ятсот дев'яносто дев'ять гривень 99 копійок."

    >>> uah_number_to_words(0)
    Traceback (most recent call last):
        ...
    TypeError: amount must be Decimal
    """
    if not isinstance(amount, Decimal):
        raise TypeError("amount must be Decimal")
    kopecks = abs(int((amount % 1) * 100))
    result = num2words(amount, lang="uk", to="currency", currency="UAH", cents=False)
    # convert word representation of kopecks to number
    result = result.split(", ")
    result[1] = str(kopecks) + " " + result[1].split()[-1]
    return " ".join(result).capitalize() + "."


def main() -> None:
    arg_parser = argparse.ArgumentParser(
        description="Перетворює числове представлення грошової суми в суму прописом. Без аргументів читає суму з клавіатури.",
    )
    arg_parser.add_argument(
        "amount", type=str, help="грошова сума числом формату x.yy", nargs="?"
    )
    args = arg_parser.parse_args()
    if args.amount is None:
        args.amount = input("Введіть грошову суму у форматі x.yy: ")
    if len(parts := (args.amount.split("."))) != 2 or len(parts[1]) != 2:
        arg_parser.error("Неправильний формат грошової суми. Введіть у форматі x.yy")
    try:
        args.amount = Decimal(args.amount)
    except InvalidOperation:
        arg_parser.error("Неправильний формат грошової суми. Введіть у форматі x.yy")
    print(uah_number_to_words(args.amount))


if __name__ == "__main__":
    main()
