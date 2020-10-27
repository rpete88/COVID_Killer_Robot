# Untitled - By: Mark - Mon Oct 19 2020

PWMLOW = 3.5
PWMHIGH = 11.2

from machine import Timer, PWM
import time
from fpioa_manager import board_info

tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode = Timer.MODE_PWM)
servo = PWM(tim, freq = 50, duty = 5, pin = board_info.D[10])
#servo.duty(PWMLOW)
#print(servo.duty)
#time.sleep_ms(500)
#servo.duty(PWMHIGH)
#time.sleep_ms(500)
#servo.duty(7)

dir = True
duty = PWMLOW

while(True):

    if dir:
        duty += .2
        servo.duty(duty)
        time.sleep_ms(50)
    else:
        duty -= .2
        servo.duty(duty)
        time.sleep_ms(50)
    if duty>PWMHIGH:
        dir = False
    elif duty<PWMLOW:
        dir = True



