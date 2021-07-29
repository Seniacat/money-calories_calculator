import datetime as dt
from typing import Optional, Union


class Record:
    def __init__(
            self,
            amount: float,
            comment: str,
            date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        self.date = (
            dt.datetime.strptime(date, '%d.%m.%Y').date()
            if date else Calculator.current_date)


class Calculator:
    current_date = dt.datetime.now().date()
    cut_off_date = current_date - dt.timedelta(weeks=1)

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: list = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        return sum([record.amount for record in self.records
                    if record.date == Calculator.current_date])

    def get_today_remained(self) -> float:
        return self.limit - self.get_today_stats()

    def get_week_stats(self) -> float:
        return sum([record.amount for record in self.records
                    if record.date <= Calculator.current_date
                    and record.date > Calculator.cut_off_date])


class CashCalculator(Calculator):
    USD_RATE = 73.25
    EURO_RATE = 86.96

    def get_today_cash_remained(self, currency: str) -> Union[float, str]:
        if currency == 'rub':
            cash_remained = round(super().get_today_remained(), 2)
            value = 'руб'
        elif currency == 'usd':
            cash_remained = round(
                super().get_today_remained() / CashCalculator.USD_RATE, 2)
            value = 'USD'
        else:
            cash_remained = round(
                super().get_today_remained() / CashCalculator.EURO_RATE, 2)
            value = 'Euro'
        if cash_remained > 0:
            return f'На сегодня осталось {cash_remained} {value}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        else:
            debt = abs(cash_remained)
            return f'Денег нет, держись: твой долг - {debt} {value}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> Union[float, str]:
        calories_remained = super().get_today_remained()
        allow_msg = (
            f'Сегодня можно съесть что-нибудь ещё, но с'
            f' общей калорийностью не более {calories_remained} кКал'
        )
        stop_msg = 'Хватит есть!'
        return allow_msg if calories_remained > 0 else stop_msg
