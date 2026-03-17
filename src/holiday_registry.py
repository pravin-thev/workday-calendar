from datetime import date

class HolidayRegistry:
    def __init__(self):
        self._holidays = []

    def add_holiday(self, holiday):
        self._holidays.append(holiday)

    def is_holiday(self, target: date) -> bool:
        return any(h.is_holiday(target) for h in self._holidays)