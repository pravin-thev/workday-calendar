# Workday Calendar

This repository is my solution for the Workday Calendar case.

## Problem

Calculate the resulting datetime when adding or subtracting a number of working days from a given start datetime.

A working day is Monday–Friday, excluding holidays. The result must always fall on a working day and within configured working hours.

## Example

```
Workday: 08:00–16:00
Recurring holiday: 17 May
Single holiday: 27 May 2004

24-05-2004 18:05 + (-5.5 days) = 14-05-2004 12:00
```

## Project Structure

```
workday_calendar/
├── holidays.py             # SingleHoliday and RecurringHoliday
├── holiday_registry.py     # Collects and checks holidays
├── workday_calculator.py   # Core calculation logic
├── workday_calendar.py     # Public-facing interface
├── main.py                 # Runs the spec examples
└── test_workday_calendar.py
```

## Design

The solution is split into small classes with a single responsibility each:

- **`SingleHoliday`** – matches one specific date
- **`RecurringHoliday`** – matches the same month/day every year
- **`HolidayRegistry`** – holds all holidays and answers `is_holiday(date)`
- **`WorkdayCalculator`** – does the actual day/minute calculations
- **`WorkdayCalendar`** – the entry point 

## Running

```bash
python main.py
```

## Tests

```bash
python -m unittest test_workday_calendar.py -v
```