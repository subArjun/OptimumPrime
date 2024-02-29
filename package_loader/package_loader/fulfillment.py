import rclpy
from pymycobot.mycobot import MyCobot
from rclpy.node import Node
import time
import json
import serial

class fulfillment_robot(Node):
    def __init__(self):
        super().__init__("fulfillment_bot")
        self.mc = MyCobot("/dev/ttyAMA0", 115200)
        self.init_pose = [[0, 0, 0, 0, 0, 0], 100]
        self.mc.send_angles(*self.init_pose)
        
        self.record_list = []
        self.arduino = serial.Serial('/dev/arduino', 9600)
        
        #self.pick_black()
        self.mc.send_angles(*self.init_pose)
        self.pick_blue()
        self.mc.send_angles(*self.init_pose)
        self.pick_green()
        self.mc.send_angles(*self.init_pose)
        self.pick_red()
        self.mc.send_angles(*self.init_pose)
    
    def pick_black(self):
        f = open("/home/er/ros2_ws/src/package_loader/package_loader/black.txt", "r")
        data = json.load(f)
        self.record_list = data
        f.close()
        i = 0        
        for angles in self.record_list:
            if (i == 100):
                self.arduino.write('c'.encode('utf-8'))
                time.sleep(1.5)
            elif (i == 300):
                self.arduino.write('o'.encode('utf-8'))
                time.sleep(1.5)
            # print(angles)
            self.mc.set_encoders_drag(angles[0], angles[1])
            time.sleep(0.055)
            
    def pick_blue(self):
        f = open("/home/er/ros2_ws/src/package_loader/package_loader/blue.txt", "r")
        data = json.load(f)
        self.record_list = data
        f.close()
        i=0
        for angles in self.record_list:
            if (i == 100):
                    self.arduino.write('c'.encode('utf-8'))
                    time.sleep(1.5)
            elif (i == 300):
                self.arduino.write('o'.encode('utf-8'))
                time.sleep(1.5)
            # print(angles)
            self.mc.set_encoders_drag(angles[0], angles[1])
            time.sleep(0.055)
            
    def pick_green(self):
        f = open("/home/er/ros2_ws/src/package_loader/package_loader/green.txt", "r")
        data = json.load(f)
        self.record_list = data
        f.close()
        i=0        
        for angles in self.record_list:
            if (i == 100):
                self.arduino.write('c'.encode('utf-8'))
                time.sleep(1.5)
            elif (i == 300):
                self.arduino.write('o'.encode('utf-8'))
                time.sleep(1.5)
            # print(angles)
            self.mc.set_encoders_drag(angles[0], angles[1])
            time.sleep(0.055)
            
    def pick_red(self):
        f = open("/home/er/ros2_ws/src/package_loader/package_loader/red.txt", "r")
        data = json.load(f)
        self.record_list = data
        f.close()
        i=0        
        for angles in self.record_list:
            if (i == 100):
                self.arduino.write('c'.encode('utf-8'))
                time.sleep(1.5)
            elif (i == 300):
                self.arduino.write('o'.encode('utf-8'))
                time.sleep(1.5)
            # print(angles)
            self.mc.set_encoders_drag(angles[0], angles[1])
            time.sleep(0.055)

        
    
def main():
    rclpy.init()
    robot = fulfillment_robot()
    rclpy.spin(robot)
    rclpy.shutdown()  
