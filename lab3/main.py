from decimal import Decimal

DEFAULT_DEPOSIT_DURATION = 24
PRECISION = Decimal("0.00")


def calculate(deposit_sum, interest_rate, duration):
    multiplier = 1 + interest_rate / 100
    monthly_balances = []
    for month in range(duration):
        deposit_sum *= multiplier
        monthly_balances.append(deposit_sum)
    return monthly_balances


def main():
    deposit_sum = Decimal(input("Deposit sum in $: "))
    interest_rate = Decimal(input("Interest rate in %: "))
    duration = int(
        input(f"Duration in months(default is {DEFAULT_DEPOSIT_DURATION}): ")
        or DEFAULT_DEPOSIT_DURATION
    )

    monthly_balances = calculate(deposit_sum, interest_rate, duration)
    for i, balance in enumerate(monthly_balances):
        print(
            f"Year {i // 12 + 1} Month {i % 12 + 1}:  {balance.quantize(PRECISION)} $"
        )
    print(f"Final balance: {monthly_balances[-1].quantize(PRECISION)} $")


if __name__ == "__main__":
    main()
