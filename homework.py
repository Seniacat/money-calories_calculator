import datetime as dt
from typing import Optional


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
            if date else dt.datetime.now().date())


class Calculator:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: list = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self) -> float:
        return sum(
            record.amount for record in self.records
            if record.date == dt.datetime.now().date())

    def get_today_remained(self) -> float:
        return self.limit - self.get_today_stats()

    def get_week_stats(self) -> float:
        current_date = dt.datetime.now().date()
        cut_off_date = dt.datetime.now().date() - dt.timedelta(weeks=1)
        return sum(
            record.amount for record in self.records
            if record.date <= current_date
            and record.date > cut_off_date)


class CashCalculator(Calculator):
    USD_RATE = 73.25
    EURO_RATE = 86.96

    RATES = {
        'usd': ('USD_RATE', 'USD'),
        'eur': ('EURO_RATE', 'Euro')
    }

    def get_today_cash_remained(self, currency: str) -> str:
        if currency == 'rub':
            cash_remained = round(super().get_today_remained(), 2)
            value = 'руб'
        else:
            divider = getattr(
                CashCalculator, CashCalculator.RATES.get(currency)[0])
            cash_remained = round(
                super().get_today_remained() / divider, 2)
            value = CashCalculator.RATES.get(currency)[1]
        if cash_remained > 0:
            return f'На сегодня осталось {cash_remained} {value}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        else:
            debt = abs(cash_remained)
            return f'Денег нет, держись: твой долг - {debt} {value}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        calories_remained = super().get_today_remained()
        allow_msg = (
            'Сегодня можно съесть что-нибудь ещё, но с'
            f' общей калорийностью не более {calories_remained} кКал'
        )
        stop_msg = 'Хватит есть!'
        return allow_msg if calories_remained > 0 else stop_msg
