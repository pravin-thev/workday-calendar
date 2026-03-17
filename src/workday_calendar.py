from datetime import date, datetime, time

from holiday_registry import HolidayRegistry
from holidays import SingleHoliday, RecurringHoliday
from workday_calculator import WorkdayCalculator


class WorkdayCalendar:
    def __init__(self):
        self._registry = HolidayRegistry()
        self._start_time = None
        self._end_time = None

    def set_workday_start_and_stop(self, start: time, stop: time):
        self._start_time = start
        self._end_time = stop

    def set_holiday(self, holiday_date: date):
        self._registry.add_holiday(SingleHoliday(holiday_date))

    def set_recurring_holiday(self, month: int, day: int):
        self._registry.add_holiday(RecurringHoliday(month, day))

    def get_workday_increment(self, start_date: datetime, increment: float) -> datetime:
        if self._start_time is None or self._end_time is None:
            raise RuntimeError("Call set_workday_start_and_stop() first.")

        calculator = WorkdayCalculator(self._start_time, self._end_time, self._registry)
        return calculator.add_workdays(start_date, increment)