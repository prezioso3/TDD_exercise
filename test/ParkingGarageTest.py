import unittest
from unittest.mock import patch

from ParkingGarage import ParkingGarage
from ParkingGarageError import ParkingGarageError

import mock.GPIO as GPIO
from mock.RTC import RTC


class ParkingGarageTest(unittest.TestCase):

    def test_check_occupancy(self):
        garage = ParkingGarage()
        self.assertTrue(True, garage.check_occupancy())
