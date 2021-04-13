# Full Robot Integration Code - Object Detection and Autonomous Robot
# by COVID-Killer-Robot Team
# This file should be renamed to boot.py and placed into root directory of the SD Card
# m.kmodel, servo.py, ultra.py, labels.txt, and startup.jpg should also be in root directory of SD Card

PWMLOW = 4.3
PWMHIGH = 10

from machine import Timer, PWM
#from fpioa_manager import board_info
from fpioa_manager import fm
from Maix import GPIO
from board import board_info
import machine, sensor, image, lcd, time
import KPU as kpu
import gc, sys
from servo import Servo
from ultra import HCSR04


def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=(224,224))
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

# main
def main(anchors, labels = None, model_addr="/sd/m.kmodel", sensor_window=(224, 224), lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)
    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    # Set up timer, PWM, and servo
    ultrasonicLeft = HCSR04(trigpin=10, echopin=3, FMGPIOTrig=fm.fpioa.GPIO0, FMGPIOEcho=fm.fpioa.GPIO1, GPIOTrig=GPIO.GPIO0, GPIOEcho=GPIO.GPIO1) #pin 12, 13 = board_info.D[12], board_info.D[13]
    ultrasonicRight = HCSR04(trigpin=12, echopin=11, FMGPIOTrig=fm.fpioa.GPIO2, FMGPIOEcho=fm.fpioa.GPIO3, GPIOTrig=GPIO.GPIO2, GPIOEcho=GPIO.GPIO3) #pin 10, 11 = board_info.D[10], board_info.D[11]

    tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode = Timer.MODE_PWM)
    tim1 = Timer(Timer.TIMER1, Timer.CHANNEL1, mode = Timer.MODE_PWM)
    tim2 = Timer(Timer.TIMER0, Timer.CHANNEL1, mode = Timer.MODE_PWM)

    leftWheelServo = PWM(tim0, freq = 50, duty = 7.32, pin = 14) #pin 8
    rightWheelServo = PWM(tim1, freq = 50, duty = 7.4, pin = 13) #pin 9
    scanPWM = PWM(tim2, freq=50, duty=0, pin = 15) # pin 7

    scanServo = Servo(scanPWM, dir=80)
    increment = 5 # value to increment the microservo (unit is degrees)

    '''
    Functions to control servos
    '''
    def turnRight():
        leftWheelServo.duty(PWMHIGH)
        rightWheelServo.duty(PWMHIGH)
        print("turn Right")
        time.sleep_ms(500)

    def turnLeft():
        leftWheelServo.duty(PWMLOW)
        rightWheelServo.duty(PWMLOW)
        print("Turn Left")
        time.sleep_ms(500)

    def driveForward():
        leftWheelServo.duty(PWMHIGH)
        rightWheelServo.duty(PWMLOW)
        print("drive forward")

    def driveForwardSlow():
        leftWheelServo.duty(9)
        rightWheelServo.duty(5.5)

    def slightAdjustRight():
        leftWheelServo.duty(7.40)
        rightWheelServo.duty(PWMLOW)
        print("slight right")
        time.sleep_ms(25)

    def slightAdjustLeft():
        leftWheelServo.duty(PWMHIGH)
        rightWheelServo.duty(7.40)
        print("slight left")
        time.sleep_ms(25)

    def ServoStop():
        leftWheelServo.duty(7.40)
        rightWheelServo.duty(7.40)
        print("stop")


    if not labels:
        with open('labels.txt','r') as f:
            exec(f.read())
    if not labels:
        print("no labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

    try:
        task = kpu.load(model_addr)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]
        while(True):
            # Ultasonic Readings
            # ultrasonicLeft.distance_in()
            # ultrasonicRight.distance_in()
            # Take screenshot and run yolo2 on image
            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            # If we detect a desk
            if objects:
                print("Desk has been detected!!!!!!!!!!")
                ServoStop()
                for obj in objects:
                    print(obj)
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    img.draw_string(pos[0], pos[1], "%s : %.2f" %(labels[obj.classid()], obj.value()), scale=2, color=(255, 0, 0))
                    save = img
                img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
                lcd.display(img)
                if scanServo.value > 52:
                    while scanServo.value > 52:
                        scanServo.drive(-2)
                        slightAdjustRight()
                elif scanServo.value < 48:
                    while scanServo.value < 48:
                        scanServo.drive(2)
                        slightAdjustLeft()
                ServoStop()
                img = sensor.snapshot()
                t = time.ticks_ms()
                objects = kpu.run_yolo2(task, img)
                t = time.ticks_ms() - t
                while not objects:
                    img = sensor.snapshot()
                    t = time.ticks_ms()
                    objects = kpu.run_yolo2(task, img)
                    t = time.ticks_ms() - t
                if objects:
                    driveForward()
                    time.sleep(10)
                    ServoStop()
                    time.sleep(10)
            else:
                # Increment the scan servo
                scanServo.drive(increment)
                # Modify the increment value if necessary
                if (scanServo.value == 100 ):
                    increment = -2
                if (scanServo.value == 0 ):
                    increment = 2

                # Control Robot based on ultrasonic readings
                if(ultrasonicRight.distance_in()>0 and ultrasonicRight.distance_in()<9 and ultrasonicLeft.distance_in()>0 and ultrasonicLeft.distance_in()<9):
                    ServoStop()
                    time.sleep_ms(500)
                    turnRight()
                elif((ultrasonicRight.distance_in()<0 or ultrasonicRight.distance_in()>9) and (ultrasonicLeft.distance_in()<0 or ultrasonicLeft.distance_in()>9)):
                    driveForward()
                elif((ultrasonicRight.distance_in()>0 and ultrasonicRight.distance_in()<9) and (ultrasonicLeft.distance_in()<0 or ultrasonicLeft.distance_in()>9)):
                    turnLeft()
                elif((ultrasonicRight.distance_in()<0 or ultrasonicRight.distance_in()>9) and (ultrasonicLeft.distance_in()>0 and ultrasonicLeft.distance_in()<9)):
                    turnRight()


    except Exception as e:
        print(e)
        raise e
    finally:
        kpu.deinit(task)


if __name__ == "__main__":
    try:
        labels = ["desks"]
        anchors = [1.8504418134689333, 1.2593817710876465, 2.9977920055389404, 3.847682237625122, 5.92604923248291, 4.488962650299072, 6.478476762771606, 6.562475204467773, 3.07891845703125, 1.9586095809936523]
        # main(anchors = anchors, labels=labels, model_addr=0x200000, lcd_rotation=0)
        main(anchors = anchors, labels=labels, model_addr="/sd/m.kmodel")
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
