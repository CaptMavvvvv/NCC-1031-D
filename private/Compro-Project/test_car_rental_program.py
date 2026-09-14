import unittest

from Car_rental_program import (
    validate_phone,
    validate_email,
    validate_date_range,
    get_customer_rental_history,
    get_car_rental_history,
    is_car_available_for_period,
)


class FakeRentalManager:
    """
    Simple fake manager used for testing.

    It avoids creating/modifying real .bin files.
    """

    def __init__(self, rentals):
        self.rentals = rentals

    def get_all_records(self):
        return self.rentals

    def get_active_records(self):
        return [
            r for r in self.rentals
            if r.get('IsActive')
        ]


class TestValidation(unittest.TestCase):

    def test_valid_phone(self):
        self.assertTrue(validate_phone("0812345678"))

    def test_phone_with_letters(self):
        self.assertFalse(validate_phone("08123ABC78"))

    def test_phone_too_short(self):
        self.assertFalse(validate_phone("12345"))

    def test_valid_email(self):
        self.assertTrue(validate_email("test@example.com"))

    def test_empty_email_is_allowed(self):
        self.assertTrue(validate_email(""))

    def test_invalid_email(self):
        self.assertFalse(validate_email("test@"))

    def test_valid_date_range(self):
        self.assertTrue(
            validate_date_range(15012026, 20012026)
        )

    def test_invalid_date_range(self):
        self.assertFalse(
            validate_date_range(20012026, 15012026)
        )

    def test_invalid_date(self):
        self.assertFalse(
            validate_date_range(99999999, 20012026)
        )


class TestRentalHistory(unittest.TestCase):

    def setUp(self):
        self.rentals = [
            {
                'IsActive': True,
                'ID': 1,
                'CustomerID': 10,
                'CarID': 5,
                'StartDate': 10012026,
                'EndDate': 15012026,
                'TotalPrice': 500.0,
            },
            {
                'IsActive': False,
                'ID': 2,
                'CustomerID': 10,
                'CarID': 7,
                'StartDate': 20012026,
                'EndDate': 25012026,
                'TotalPrice': 700.0,
            },
            {
                'IsActive': True,
                'ID': 3,
                'CustomerID': 20,
                'CarID': 5,
                'StartDate': 1022026,
                'EndDate': 5022026,
                'TotalPrice': 400.0,
            },
        ]

        self.rental_mgr = FakeRentalManager(self.rentals)

    def test_customer_history(self):
        history = get_customer_rental_history(
            self.rental_mgr,
            10
        )

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['ID'], 1)
        self.assertEqual(history[1]['ID'], 2)

    def test_customer_without_history(self):
        history = get_customer_rental_history(
            self.rental_mgr,
            999
        )

        self.assertEqual(history, [])

    def test_car_history(self):
        history = get_car_rental_history(
            self.rental_mgr,
            5
        )

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['CustomerID'], 10)
        self.assertEqual(history[1]['CustomerID'], 20)

    def test_car_without_history(self):
        history = get_car_rental_history(
            self.rental_mgr,
            999
        )

        self.assertEqual(history, [])


class TestCarAvailability(unittest.TestCase):

    def setUp(self):
        self.rentals = [
            {
                'IsActive': True,
                'ID': 1,
                'CustomerID': 10,
                'CarID': 5,
                'StartDate': 10012026,
                'EndDate': 15012026,
                'TotalPrice': 500.0,
            },
            {
                'IsActive': False,
                'ID': 2,
                'CustomerID': 20,
                'CarID': 5,
                'StartDate': 20012026,
                'EndDate': 25012026,
                'TotalPrice': 700.0,
            },
        ]

        self.rental_mgr = FakeRentalManager(self.rentals)

    def test_available_before_existing_rental(self):
        result = is_car_available_for_period(
            self.rental_mgr,
            5,
            1012026,
            9012026
        )

        self.assertTrue(result)

    def test_unavailable_when_dates_overlap(self):
        result = is_car_available_for_period(
            self.rental_mgr,
            5,
            12012026,
            18012026
        )

        self.assertFalse(result)

    def test_available_after_existing_rental(self):
        result = is_car_available_for_period(
            self.rental_mgr,
            5,
            16012026,
            19012026
        )

        self.assertTrue(result)

    def test_different_car_is_available(self):
        result = is_car_available_for_period(
            self.rental_mgr,
            99,
            10012026,
            15012026
        )

        self.assertTrue(result)

    def test_closed_rental_does_not_block_car(self):
        result = is_car_available_for_period(
            self.rental_mgr,
            5,
            20012026,
            25012026
        )

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()