# Microservo plus object detection integration
# microservo_object_detect_integration.py 
# By: COVID_Killer_Robot Team
# January 15, 2021

# Using the mini pan tilt, and Maixduino pin number 9
# The servo should move about 180 degrees and the camera should look for desks

import time, sys
from machine import Timer,PWM
from fpioa_manager import board_info
from servo import Servo
import sensor,image,lcd
import KPU as kpu

# Set up timer, PWM, and servo
tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
pwm = PWM(tim0, freq=50, duty=0, pin = board_info.D[9])
myservo = Servo(pwm, dir=80)

increment = 5

# Set up camera and object detection
print("program starting")
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)
print("after sensor statements")
classes = ["desks"]
print("test1")
task = kpu.load(0xd00000) #change to "/sd/name_of_the_model_file.kmodel" if loading from SD card
print("test2")
a = kpu.set_outputs(task, 0, 7,7,30)   #the actual shape needs to match the last layer shape of your model(before Reshape)
print("test3")
anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
print("test4")
a = kpu.init_yolo2(task, 0.3, 0.3, 5, anchor) #tweak the second parameter if you're getting too many false positives
print("entering while loop")


while(True):

    img = sensor.snapshot().rotation_corr(z_rotation=90.0) #take picture
    a = img.pix_to_ai()
    code = kpu.run_yolo2(task, img)
    if code:
        detect = 1
        for i in code:
            a=img.draw_rectangle(i.rect(),color = (0, 255, 0))
            a = img.draw_string(i.x(),i.y(), classes[i.classid()], color=(255,0,0), scale=3)
        a = lcd.display(img)
    else:
        detect = 0
        a = lcd.display(img)

    if detect == 1:
        print("Desk has been detected!!!!!!!!!!")
        time.sleep(3)
    print(myservo.value)
    print()

    myservo.drive(increment)

    if (myservo.value == 100 ):
        increment = -5
    if (myservo.value == 0 ):
        increment = 5
    time.sleep_ms(250)

a = kpu.deinit(task)
