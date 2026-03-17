import unittest
from datetime import date, datetime, time

from holidays import SingleHoliday, RecurringHoliday
from workday_calendar import WorkdayCalendar


def make_calendar() -> WorkdayCalendar:
    cal = WorkdayCalendar()
    cal.set_workday_start_and_stop(time(8, 0), time(16, 0))
    cal.set_recurring_holiday(5, 17)
    cal.set_holiday(date(2004, 5, 27))
    return cal


class TestHolidays(unittest.TestCase):
    def test_single_holiday_matches_only_its_date(self):
        h = SingleHoliday(date(2004, 5, 27))
        self.assertTrue(h.is_holiday(date(2004, 5, 27)))
        self.assertFalse(h.is_holiday(date(2005, 5, 27)))  

    def test_recurring_holiday_matches_every_year(self):
        h = RecurringHoliday(5, 17)
        self.assertTrue(h.is_holiday(date(2004, 5, 17)))
        self.assertTrue(h.is_holiday(date(2023, 5, 17)))
        self.assertFalse(h.is_holiday(date(2004, 5, 18)))

    def test_recurring_holiday_rejects_invalid_date(self):
        with self.assertRaises(ValueError):
            RecurringHoliday(2, 30)


class TestSpecificationExamples(unittest.TestCase):
    def setUp(self):
        self.cal = make_calendar()

    def test_main_example(self):
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 18, 5), -5.5)
        self.assertEqual(result, datetime(2004, 5, 14, 12, 0))

    def test_positive_large(self):
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 19, 3), 44.723656)
        self.assertEqual(result, datetime(2004, 7, 27, 13, 47))

    def test_negative_large(self):
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 18, 3), -6.7470217)
        self.assertEqual(result, datetime(2004, 5, 13, 10, 2))

    def test_positive_within_hours(self):
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 8, 3), 12.782709)
        self.assertEqual(result, datetime(2004, 6, 10, 14, 18))

    def test_early_start(self):
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 7, 3), 8.276628)
        self.assertEqual(result, datetime(2004, 6, 4, 10, 12))


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.cal = WorkdayCalendar()
        self.cal.set_workday_start_and_stop(time(8, 0), time(16, 0))

    def test_raises_if_not_configured(self):
        with self.assertRaises(RuntimeError):
            WorkdayCalendar().get_workday_increment(datetime(2004, 5, 24, 8, 0), 1.0)

    def test_start_before_hours_treated_as_day_start(self):
        # count from 08:00
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 7, 0), 0.5)
        self.assertEqual(result, datetime(2004, 5, 24, 12, 0))

    def test_start_after_hours_treated_as_next_workday(self):
        # count from 08:00 next day
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 18, 0), 0.5)
        self.assertEqual(result, datetime(2004, 5, 25, 12, 0))

    def test_skips_weekend(self):
        result = self.cal.get_workday_increment(datetime(2004, 5, 21, 8, 0), 1.0)
        self.assertEqual(result, datetime(2004, 5, 24, 8, 0))

    def test_skips_holiday(self):
        self.cal.set_holiday(date(2004, 5, 25))
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 8, 0), 1.0)
        self.assertEqual(result, datetime(2004, 5, 26, 8, 0))

    def test_negative_skips_weekend(self):
        result = self.cal.get_workday_increment(datetime(2004, 5, 24, 8, 0), -1.0)
        self.assertEqual(result, datetime(2004, 5, 21, 8, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)