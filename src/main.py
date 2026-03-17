from datetime import date, datetime, time
from workday_calendar import WorkdayCalendar


def main():
    cal = WorkdayCalendar()
    cal.set_workday_start_and_stop(time(8, 0), time(16, 0))
    cal.set_recurring_holiday(5, 17)        # 17. mai every year
    cal.set_holiday(date(2004, 5, 27))      # single holiday

    print("Oppsett: 08:00–16:00 | Helligdager: 17. mai (fast), 27. mai 2004")
    print()

    cases = [
        (datetime(2004, 5, 24, 18,  5),  -5.5,       datetime(2004,  5, 14, 12,  0)),
        (datetime(2004, 5, 24, 19,  3),  44.723656,   datetime(2004,  7, 27, 13, 47)),
        (datetime(2004, 5, 24, 18,  3),  -6.7470217,  datetime(2004,  5, 13, 10,  2)),
        (datetime(2004, 5, 24,  8,  3),  12.782709,   datetime(2004,  6, 10, 14, 18)),
        (datetime(2004, 5, 24,  7,  3),   8.276628,   datetime(2004,  6,  4, 10, 12)),
    ]

    for start, increment, expected in cases:
        result = cal.get_workday_increment(start, increment)
        sign = "+" if increment >= 0 else ""
        status = ":)" if result == expected else f"x (forventet {expected.strftime('%d-%m-%Y %H:%M')})"
        print(f"  {start.strftime('%d-%m-%Y %H:%M')}  {sign}{increment:<12}  →  {result.strftime('%d-%m-%Y %H:%M')}  {status}")


if __name__ == "__main__":
    main()