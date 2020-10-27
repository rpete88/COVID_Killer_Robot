# Untitled - By: Mark - Mon Oct 26 2020

import machine, time
from Maix import GPIO
from board import board_info
from fpioa_manager import fm


class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigpin, echopin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin.
        By default is based in sensor limit range (4m)
        """


        fm.register(trigpin, fm.fpioa.GPIO0, force=True) # 15 - trig_dispensor
        fm.register(echopin, fm.fpioa.GPIO1, force=True) # 17 - echo_dsipenser


        print("trigger gpio ", trigpin)
        print("echo gpio ", echopin)
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = GPIO(GPIO.GPIO0, GPIO.OUT)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_NONE)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)

        # if we never reach high level on echo pin, return -2 as timeout
        time_start = time.ticks_us()
        while (self.echo.value() != 1):
            if(time.ticks_us() - time_start >= self.echo_timeout_us):
                print("timeout waiting for hight")
                return -2
        time_pule_start = time.ticks_us()
        # if we never reach low value on echo pin
        while (self.echo.value() == 1):
            if(time.ticks_us() - time_start >= self.echo_timeout_us):
                print("timeout waiting for low")
                return -1

        time_pule_end = time.ticks_us()
        return (time_pule_end - time_pule_start)


        # try:
        #     pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
        #     return pulse_time
        # except OSError as ex:
        #     if ex.args[0] == 110: # 110 = ETIMEDOUT
        #         raise OSError('Out of range')
        #     raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()
        print("pulse time is : ", pulse_time)

        # To calculate the distance we get the pulse_time and divide it by 2
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms

ultrasonic = HCSR04(trigpin=board_info.D[13], echopin=board_info.D[12])

while(True):
    ultrasonic.distance_cm()
