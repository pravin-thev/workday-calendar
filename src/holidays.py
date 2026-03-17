from datetime import date

class SingleHoliday:
    def __init__(self, holiday_date: date):
        self.date = holiday_date

    def is_holiday(self, target: date) -> bool:
        return self.date == target


class RecurringHoliday:
    def __init__(self, month: int, day: int):
        date(2000, month, day)  # validates month/day combination
        self.month = month
        self.day = day

    def is_holiday(self, target: date) -> bool:
        return target.month == self.month and target.day == self.day