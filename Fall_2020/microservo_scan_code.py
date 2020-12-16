# MicroServo Scan 
# By: COVID_Killer_Robot Team
# Thu Oct 22 2020

# Using the mini pan tilt, and Maixduino pin number 9
# The servo should move about 180 degrees

import time, sys
from machine import Timer,PWM
from fpioa_manager import board_info

# Servo Class Code modified from https://github.com/sipeed/MaixPy_scripts/blob/master/demo/gimbal/Gimbal.py
class Servo:
    def __init__(self, pwm, dir=50, duty_min=5, duty_max=10):
        self.value = dir
        self.pwm = pwm
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty_range = duty_max -duty_min
        self.enable(True)
        self.pwm.duty(self.value/100*self.duty_range+self.duty_min)

    def enable(self, en):
        if en:
            self.pwm.enable()
        else:
            self.pwm.disable()

    def dir(self, percentage):
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
        self.pwm.duty(percentage/100*self.duty_range+self.duty_min)

    def drive(self, inc):
        self.value += inc
        if self.value > 100:
            self.value = 100
        elif self.value < 0:
            self.value = 0
        self.pwm.duty(self.value/100*self.duty_range+self.duty_min)


tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
pwm = PWM(tim0, freq=50, duty=0, pin = board_info.D[9])
myservo = Servo(pwm, dir=80)

increment = 5

while(True):

    print(myservo.value)
    print()

    myservo.drive(increment)

    if (myservo.value == 100 ):
        increment = -5
    if (myservo.value == 0 ):
        increment = 5
    time.sleep_ms(250)
