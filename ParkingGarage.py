import time
import mock.GPIO as GPIO
from mock.RTC import RTC
from ParkingGarageError import ParkingGarageError


class ParkingGarage:
    # Pin number declarations
    INFRARED_PIN1 = 11
    INFRARED_PIN2 = 12
    INFRARED_PIN3 = 13
    RTC_PIN = 15
    SERVO_PIN = 16
    LED_PIN = 18

    def __init__(self):
        """
        Constructor
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.INFRARED_PIN1, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN2, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN3, GPIO.IN)
        GPIO.setup(self.RTC_PIN, GPIO.IN)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        self.rtc = RTC(self.RTC_PIN)
        self.pwm = GPIO.PWM(self.SERVO_PIN, 50)
        self.pwm.start(0)

    def check_occupancy(self, pin: int) -> bool:
        """
        Checks whether one of the infrared distance sensor detects something in front of it.
        :param pin: The data pin of the sensor that is being checked (e.g., INFRARED_PIN1).
        :return: True if the infrared sensor detects something, False otherwise.
        """
        check_value = GPIO.input(pin)

        if pin not in [self.INFRARED_PIN1, self.INFRARED_PIN2, self.INFRARED_PIN3]:
            raise ParkingGarageError

        if check_value == 0:
            return False
        else:
            return True

    def get_occupied_spots(self) -> int:
        """
        Calculates the number of occupied parking spots in the garage.
        :return: The number of occupied spots.
        """
        count = 0
        for pin in [self.INFRARED_PIN1, self.INFRARED_PIN2, self.INFRARED_PIN3]:
            if GPIO.input(pin) > 0:
                count += 1
            else:
                raise ParkingGarageError

        return count

    def calculate_parking_fee(self, entry_time: str) -> float:
        """
        Uses the RTC to calculate the amount of money to be paid by the customer of the garage
        For each hour spent in the garage, there is a flat cost of 2.50 €;
        additionally, during the weekend (Saturday and Sunday)
        an additional 25% fee is applied to the total of the parking ticket.
        Even when customers do not exceed a full hour, they will still be charged 2.50 €.
        :param entry_time: A string in the format "hh:mm:ss" containing the entry time of a
        vehicle in the garage
        :return: The total amount to be paid by the customer
        """
        time_now = self.rtc.get_current_time_string()
        day = self.rtc.get_current_day()

        hour_now = int(time_now[0] + time_now[1])
        hour_entry = int(entry_time[0] + entry_time[1])

        minute_now = int(time_now[3] + time_now[4])
        minute_entry = int(entry_time[3] + entry_time[4])

        hours = hour_now - hour_entry
        print(hours)

        minutes = minute_now - minute_entry
        print(minutes)

        if hours < 0 or (hours <= 0 and (minutes <= 0)):
            raise ParkingGarageError

        if minutes > 0:
            hours += 1

        fee = hours * 2.50

        if day in ['SATURDAY', 'SUNDAY']:
            fee += fee * 0.25

        return fee


    def open_garage_door(self) -> None:
        """
        Opens the garage door using the servo motor
        A motor angle of 180 degrees corresponds to a fully open door
        """
        pass

    def close_garage_door(self) -> None:
        """
        Closes the garage door using the servo motor
        A motor angle of 0 degrees corresponds to a fully closed door
        """
        pass

    def turn_light_on(self) -> None:
        """
        Turns on the smart lightbulb
        """
        pass

    def turn_light_off(self) -> None:
        """
        Turns off the smart lightbulb
        """
        pass

    def change_servo_angle(self, duty_cycle):
        """
        Changes the servo motor's angle by passing him the corresponding PWM duty cycle signal
        :param duty_cycle: the length of the duty cycle
        """
        GPIO.output(self.SERVO_PIN, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        GPIO.output(self.SERVO_PIN, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
