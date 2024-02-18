29#!/usr/bin/env python3

import Jetson.GPIO as gpio
import time


gpio.setmode(gpio.BOARD)
in1l = 29
in2l = 12
in3l = 13
in4l = 16
in1r = 18
in2r = 19
in3r = 21
in4r = 22
enar = 23
enal = 24

gpio.setup(in1l, gpio.OUT, initial=gpio.LOW)
gpio.setup(in1r, gpio.OUT, initial=gpio.LOW)
gpio.setup(in2l, gpio.OUT, initial=gpio.HIGH)
gpio.setup(in2r, gpio.OUT, initial=gpio.LOW)
gpio.setup(in3l, gpio.OUT, initial=gpio.LOW)
gpio.setup(in3r, gpio.OUT, initial=gpio.LOW)
gpio.setup(in4l, gpio.OUT, initial=gpio.LOW)
gpio.setup(in4r, gpio.OUT, initial=gpio.LOW)
            
#motor_l = gpio.PWM(32, 50) # TODO
#motor_r = gpio.PWM(33, 50)
#motor_l.start(0)
#motor_r.start(0)

for j in range(5):
#	gpio.output(in1l, gpio.HIGH)
#	gpio.output(in3l, gpio.HIGH)
	gpio.output(in2l, gpio.LOW)
	time.sleep(2)
	gpio.output(in2l, gpio.HIGH)
	time.sleep(2)
	
#for i in range(100):
#	motor_l.ChangeDutyCycle(int(i))
#	motor_r.ChangeDutyCycle(int(i))
	
#	gpio.output(in2l, gpio.HIGH)
#	gpio.output(in4l, gpio.HIGH)
#	gpio.output(in1l, gpio.LOW)
#	gpio.output(in3l, gpio.LOW)

#for i in range(100):
#	motor_l.ChangeDutyCycle(int(i))
#	motor_r.ChangeDutyCycle(int(i))
gpio.cleanup()
