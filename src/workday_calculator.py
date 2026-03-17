from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from holiday_registry import HolidayRegistry


class WorkdayCalculator:
    def __init__(self, start_time, end_time, registry: HolidayRegistry):
        self._start_time = start_time
        self._end_time = end_time
        self._registry = registry
        self._duration = end_time.hour * 60 + end_time.minute - start_time.hour * 60 - start_time.minute

    def add_workdays(self, start: datetime, workdays: float) -> datetime:
        workdays = Decimal(str(workdays))
        forward  = workdays >= 0
        step     = timedelta(days=1 if forward else -1)
        duration = Decimal(self._duration)

        # Figure out where we are in the workday (minutes from 08:00)
        day_start_min = self._start_time.hour * 60 + self._start_time.minute
        day_end_min   = self._end_time.hour * 60 + self._end_time.minute
        actual_min    = start.hour * 60 + start.minute

        if actual_min <= day_start_min:
            position = Decimal(0)       # before work 
        elif actual_min >= day_end_min:
            position = duration         # after work  
        else:
            position = Decimal(actual_min - day_start_min)

        # Find first valid workday 
        current_date = start.date()
        if forward and position >= duration:
            current_date += step        
            position = Decimal(0)
        while not self._is_workday(current_date):
            current_date += step

        # iterate workdays until we've used up all the minutes
        minutes_remaining = (abs(workdays) * duration).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        while minutes_remaining > 0:
            available_today = (duration - position) if forward else position

            if minutes_remaining < available_today:
                break   

            if minutes_remaining == available_today:
                if forward:
                    current_date += step
                    while not self._is_workday(current_date):
                        current_date += step
                return self._to_datetime(current_date, Decimal(0), forward)

            # Use up all minutes available then move on
            minutes_remaining -= available_today
            current_date += step
            while not self._is_workday(current_date):
                current_date += step
            position = Decimal(0) if forward else duration

        final_position = position + minutes_remaining if forward else position - minutes_remaining
        return self._to_datetime(current_date, final_position, forward)

    def _is_workday(self, d: date) -> bool:
        return d.weekday() < 5 and not self._registry.is_holiday(d)

    def _to_datetime(self, d: date, minutes_from_start: Decimal, forward: bool) -> datetime:
        # FLOOR going forward, CEILING going backward
        rounding = "ROUND_FLOOR" if forward else "ROUND_CEILING"
        minutes  = int(minutes_from_start.to_integral_value(rounding=rounding))
        hour, minute = divmod(self._start_time.hour * 60 + self._start_time.minute + minutes, 60)
        return datetime(d.year, d.month, d.day, hour, minute)