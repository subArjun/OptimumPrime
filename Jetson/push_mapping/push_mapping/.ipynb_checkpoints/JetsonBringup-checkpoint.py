#!/usr/bin/env python3
# pylint: skip-file
import rclpy
from rclpy.node import Node
import time
from geometry_msgs.msg import Twist, TwistWithCovariance
#from std_msgs.msg import Int
from nav_msgs.msg import Odometry
import serial  





class jetsonBringup(Node):
    def __init__(self):
        super().__init__('jetsonBringup')
        #Voltage publisher
       # self.voltagePub = self.create_publisher(Int,'/jetson/voltage',10)
        
        #twist subscriber
        self.twistSub = self.create_subscription(Twist, '/cmd_vel', self.twistSub, 10)
        self.twistSub
        self.odomSub = self.create_subscription(Odometry, '/odom', self.odomSub, 10)
        self.odomSub
        
        self.arduino = serial.Serial('/dev/arduino',9600)

        self.linear = 0.0
        self.angular = 0.0
        #PID gains
        self.p_l = 3
        self.i_l = 0.0
        self.d_l = 0.0
        
        self.p_a = 3
        self.i_a = 0.0
        self.d_a = 0.0

        #derivatives and integrals
        self.l_derivative = 0.0
        self.l_integral = 0.0
        
        self.a_derivative = 0.0
        self.a_integral = 0.0

        #time deltas
        self.time_delta = 0.0
        self.prev_time = 0.0
        self.prev_error_l = 0.0
        self.prev_error_a = 0.0

        #motor throttle
        self.motor_l_throttle = 0.0
        self.motor_r_throttle = 0.0
        self.throttle = 0.0
        self.steer = 0.0
        

       
            
       
    def twistSub(self, msg):
        self.linear = msg.linear.x 
        self.angular = msg.angular.z
        #self.get_logger().info(self.linear)
        #print('hi')
    
    def odomSub(self, msg):
        currentTime = time.time()
        #print('hi')
        #self.get_logger().info(str(msg.twist.twist.linear))
        error_l = self.linear - msg.twist.twist.linear.x
        error_a = self.angular - msg.twist.twist.angular.z
        #print(error_l, error_a)
        if (self.prev_time == 0.0):
            self.time_delta = 0.0001
            self.a_derivative = 0.0
            self.l_derivative = 0.0
            self.a_integral = 0.0
            self.l_integral = 0.0
        else:
            self.time_delta = currentTime - self.prev_time
            self.l_integral = error_l * self.time_delta
            self.a_integral = error_a * self.time_delta
            self.l_derivative = (error_l - self.prev_error_l) / self.time_delta
            self.a_derivative = (error_a - self.prev_error_a) / self.time_delta
        
        throttle = self.throttle + self.p_l * error_l + self.i_l * self.l_integral + self.d_l * self.l_derivative
        steer = self.steer + self.p_a * error_a + self.i_a * self.a_integral + self.d_a * self.a_derivative

        self.prev_time = currentTime
        self.prev_error_a = error_a
        self.prev_error_l = error_l
        
        self.move_base(throttle, steer)

    def move_base(self, throttle, steer):
        self.motor_l_throttle = int(self.motor_l_throttle + throttle + steer)
        self.motor_r_throttle = int(self.motor_r_throttle + throttle - steer)

    #TODO voltage scaling
    # self.motor_l_throttle *= (self.max_volts / self.current_voltage)
    # self.motor_r_throttle *= (self.max_volts / self.current_voltage)
        if (self.motor_l_throttle >= 100): 
            self.motor_l_throttle = 100
        if (self.motor_l_throttle <= -100): 
            self.motor_l_throttle = -100
        if (self.motor_r_throttle >= 100): 
            self.motor_r_throttle = 100
        if (self.motor_r_throttle <= -100): 
            self.motor_r_throttle = -100
        
        l_throttle = str(self.motor_l_throttle)
        r_throttle = str(self.motor_r_throttle)
        
	
        self.arduino.write((l_throttle + 'o' + r_throttle + '\n').encode('utf-8'))
        
        #while(self.arduino.in_waiting > 1):
            #print(self.arduino.readline(), self.motor_l_throttle, self.motor_r_throttle)

def main():
    rclpy.init()
    jetson = jetsonBringup()
    rclpy.spin(jetson)
    jetson.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
