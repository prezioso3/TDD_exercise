import unittest
from unittest.mock import patch

from ParkingGarage import ParkingGarage
from ParkingGarageError import ParkingGarageError

import mock.GPIO as GPIO
from mock.RTC import RTC


class ParkingGarageTest(unittest.TestCase):
    @patch.object(GPIO, "input")
    def test_check_occupancy(self, mock_sensor_value):
        mock_sensor_value.return_value = 49
        garage = ParkingGarage()
        res = garage.check_occupancy(mock_sensor_value)
        self.assertTrue(res)
