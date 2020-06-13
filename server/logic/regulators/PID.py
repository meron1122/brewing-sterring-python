# Based on -> https://gist.github.com/bradley219/5373998
class PID:
    def __init__(self, dt, min, max, kp, kd, ki):
        self.__dt = dt
        self.__min = min
        self.__max = max
        self.__kp = kp
        self.__kd = kd
        self.__ki = ki
        self.__integral = 0
        self.__pre_error = 0

    def calc(self, setpoint, pv):
        error = setpoint - pv
        pout = self.__kp * error

        self.__integral += error * self.__dt
        iout = self.__ki * self.__integral

        derivative = (error- self.__pre_error) / self.__dt
        dout = self.__kd * derivative

        out = pout + iout +dout

        if out > self.__max:
            out = self.__max
        if out < self.__min:
            out = self.__min

        self.__pre_error = error
        return out