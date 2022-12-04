import unittest
from unittest.mock import patch

from ParkingGarage import ParkingGarage
from ParkingGarageError import ParkingGarageError

import mock.GPIO as GPIO
from mock.RTC import RTC


class ParkingGarageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.garage = ParkingGarage()

    @patch.object(GPIO, "input")
    def test_check_occupancy_spot1_parked(self, mock_sensor_value):
        mock_sensor_value.return_value = 49
        res = self.garage.check_occupancy(self.garage.INFRARED_PIN1)
        self.assertTrue(res)

    @patch.object(GPIO, "input")
    def test_check_occupancy_spot1_non_parked(self, mock_sensor_value):
        mock_sensor_value.return_value = 0
        res = self.garage.check_occupancy(self.garage.INFRARED_PIN1)
        self.assertFalse(res)

    def test_invalid_pin(self):
        self.assertRaises(ParkingGarageError, self.garage.check_occupancy, -1)

    @patch.object(GPIO, "input")
    def test_occupied_spots_3(self, mock_spot_values):
        #red phase
        #num_occ = self.garage.get_occupied_spots()
        #self.assertEqual(3, num_occ)

        #green phase
        mock_spot_values.side_effect = [3, 2, 3]
        num_occ = self.garage.get_occupied_spots()
        self.assertEqual(3, num_occ)

    @patch.object(GPIO, "input")
    def test_occupied_spots_0(self, mock_spot_values):
        # red phase
        # num_occ = self.garage.get_occupied_spots()
        # self.assertEqual(3, num_occ)

        # green phase
        mock_spot_values.side_effect = [0, 0, 0]
        num_occ = self.garage.get_occupied_spots()
        self.assertEqual(0, num_occ)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_calculate_parking_fee_example1(self, mock_time_rtc, mock_day_rtc):
        mock_day_rtc.return_value = 'MONDAY'
        mock_time_rtc.return_value = "15:24:54"
        fee = self.garage.calculate_parking_fee('12:30:15')
        self.assertEqual(7.5, fee)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_calculate_parking_fee_example2(self, mock_time_rtc, mock_day_rtc):
        mock_day_rtc.return_value = 'SATURDAY'
        mock_time_rtc.return_value = "18:12:28"
        fee = self.garage.calculate_parking_fee('10:15:08')
        self.assertEqual(25, fee)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_calculate_parking_fee_example3(self, mock_time_rtc, mock_day_rtc):
        mock_day_rtc.return_value = 'MONDAY'
        mock_time_rtc.return_value = "11:20:28"
        fee = self.garage.calculate_parking_fee('10:15:08')
        self.assertEqual(5, fee)

    @patch.object(RTC, 'get_current_time_string')
    def test_invalid_calculate_parking_fee(self, mock_time_rtc):
        mock_time_rtc.return_value = '12:19:56'
        self.assertRaises(ParkingGarageError, self.garage.calculate_parking_fee, '12:22:09')

    def test_open_garage_door(self):
        res = self.garage.open_garage_door()
        self.assertTrue(res)

    def test_close_garage_door(self):
        res = self.garage.close_garage_door()
        self.assertFalse(res)

    def test_turn_light_on(self):
        res = self.garage.turn_light_on()
        self.assertTrue(res)