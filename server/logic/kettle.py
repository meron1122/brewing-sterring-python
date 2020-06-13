import _thread
from w1thermsensor import W1ThermSensor
import time
import RPi.GPIO as GPIO

from logic.regulators.PID import PID


class Kettle:
    def __init__(self, heater_pin, paddle_pin):
        """

        :param heater_pin: Pin number on R-pi, based on BCM numeration
        :param paddle_pin: Pin number on R-pi, based on BCM numeration
        """
        self.temp = None
        self.__setpoint = None
        self.__paddle = False

        self.__heater_pin = heater_pin
        self.__paddle_pin = paddle_pin
        _thread.start_new_thread(self.__read_temp, ())
        _thread.start_new_thread(self.__pid_loop, ())

        self.__prepare_io()

    def __pid_loop(self):
        pid = PID(0.1, 0, 100, 0.59, 0.150, 0.4)  # todo move kp,ki,kd to settings
        value = 0
        heater = GPIO.PWM(self.__heater_pin, 50)
        while 1:
            if self.temp and self.__setpoint:
                value = pid.calc(self.__setpoint, self.temp)
                print("Pid out:" + str(value))

            heater.ChangeDutyCycle(value)
            time.sleep(0.1)

    def get_setpoint(self):
        return self.__setpoint

    def set_setpoint(self, setpoint):
        self.__setpoint = setpoint

    def get_paddle(self) -> bool:
        return self.__paddle

    def set_paddle(self, paddle) -> None:
        """
        Set paddle state(Enabled/Disabled)
        :param paddle: bool value for state
        :return:
        """
        self.__paddle = paddle
        GPIO.output(self.__paddle_pin, self.__paddle)

    def __read_temp(self) -> float:
        sensor = W1ThermSensor()
        while 1:
            try:
                self.temp = sensor.get_temperature()
                print(self.temp)
            except:  # todo proper logging
                self.temp = None
            time.sleep(0.1)

    def emergency_stop(self) -> None:
        """
        Emergency stop kettle -> Disable all devices, set setpoint to low value to prevent pid
        :return:
        """
        GPIO.output(self.__paddle_pin, 0)
        GPIO.output(self.__heater_pin, 0)
        self.__setpoint = 0.1

    def __prepare_io(self) -> None:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__paddle_pin, GPIO.OUT)
        GPIO.setup(self.__heater_pin, GPIO.OUT)
