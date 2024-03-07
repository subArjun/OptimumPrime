import rclpy
from pymycobot.mycobot import MyCobot
from rclpy.node import Node
import time
import json
import serial
import websocket
import ssl
import json
import asyncio

class fulfillment_robot(Node):
    def __init__(self):
        super().__init__("fulfillment_bot")
        self.mc = MyCobot("/dev/ttyAMA0", 115200)
        self.init_pose = [[0, 0, 0, 0, 0, 0], 100]
        self.mc.send_angles(*self.init_pose)
        
        self.record_list = []
        self.arduino = serial.Serial('/dev/arduino', 9600)

        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})  # connect to gyropalm web socket server at port 3200
        self.ws.connect("wss://gyropalm.com:3200")

        welcomeMessage = self.ws.recv()  # save result of receiving message into variable called welcomeMessage
        welcomeMessage = json.loads(welcomeMessage)  # convert the result from json into a String
        print("\n%s\n" % welcomeMessage)  # print the message received from the web socket, which asks for GyroPalm credentials
        authorizationMessage = json.dumps({'action':"sub", 'wearableID':"gp20906498", 'apiKey':"gp57277569125c1b08"}, sort_keys = True, indent = 4) # save the matching authorization message into variable called authorizationMessage
        print("%s\n" % authorizationMessage) # print authorization message
        self.ws.send(authorizationMessage) # send authorization message including action, wearableID and apiKey of wearable
        confirmationMessage = self.ws.recv() #receive confirmation message from GyroPalm web socket server
        confirmationMessage = json.loads(confirmationMessage) # convert the result from json into a String
        print("%s\n" % confirmationMessage) # print the message received from the web socket server, which confirms the connection

        self.timer = self.create_timer(1,self.timer_action)
        # #self.pick_black()
        # self.mc.send_angles(*self.init_pose)
        # self.pick_blue()
        # self.mc.send_angles(*self.init_pose)
        # self.pick_green()
        # self.mc.send_angles(*self.init_pose)
        # self.pick_red()
        # self.mc.send_angles(*self.init_pose)

    def timer_action(self):
        msg = self.ws.recv()
        msg = json.loads(msg)
        print("%s" % msg)
        self.order = msg["gp10222509"]  # if Home button is pressed on wearable, send robot to Home position
        self.order = self.order.split(",")
        for marker in self.order:
            if (marker == "apples"):
                self.mc.send_angles(*self.init_pose)
                self.pick_black()
                self.mc.send_angles(*self.init_pose)
            elif (marker == "oranges"):
                self.mc.send_angles(*self.init_pose)
                self.pick_blue()
                self.mc.send_angles(*self.init_pose)
            elif (marker == "bananas"):
                self.mc.send_angles(*self.init_pose)
                self.pick_green()
                self.mc.send_angles(*self.init_pose)
            elif (marker == "grapes"):
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
