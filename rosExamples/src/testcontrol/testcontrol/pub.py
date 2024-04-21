# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
import serial
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import pandas as pd

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('delta')
        self.ser = serial.Serial('/dev/ttyACM0', 9600,stopbits=serial.STOPBITS_ONE,timeout=1)
        self.x = 0
        self.y = 0
        self.z =-300
        self.a = 0
        self.b = 0
        self.c = 0

        self.driver = webdriver.Chrome()
        self.driver.get("https://www.marginallyclever.com/other/samples/fk-ik-test.html")

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "f"))
            )
        finally:
            pass
        # input in field with id f 115
        base = self.driver.find_element(By.ID, "f")
        bass = self.driver.find_element(By.ID, "e")
        bicep = self.driver.find_element(By.ID, "rf")
        forearm = self.driver.find_element(By.ID, "re")
        baseToFloor = self.driver.find_element(By.ID, "b")
        self.x_elem = self.driver.find_element(By.ID, "x")
        self.y_elem = self.driver.find_element(By.ID, "y")
        self.z_elem = self.driver.find_element(By.ID, "z")
        self.t1 = self.driver.find_element(By.ID, "t1")
        self.t2 = self.driver.find_element(By.ID, "t2")
        self.t3 = self.driver.find_element(By.ID, "t3")

        base.clear()
        bass.clear()
        bicep.clear()
        forearm.clear()
        baseToFloor.clear()

        base.send_keys("70") #f
        bass.send_keys("35") #e
        bicep.send_keys("75") #rf
        forearm.send_keys("313") #re
        baseToFloor.send_keys("407") #b
        # self.publisher1_ = self.create_publisher(Int16, 'servo1', 10)
        # self.timer = self.create_timer(timer_period, self.timer_callback1)
        
        self.timer = self.create_timer(0.5, self.pos_timer)
        self.timer = self.create_timer(0.05, self.ard_update)
        self.i = 0
        self.subscription = self.create_subscription(
            Twist,
            '/turtle1/cmd_vel',
            self.listener_callback,
            10)
        self.subscription
        self.get_logger().info('Publishing: ')
    def digit_len(self,num):
        num = str(num)
        if len(num) == 1:
            return '00'+num
        elif len(num) == 2:
            return '0'+num
        else:
            return num
    def pos_timer(self):
        out = self.IK(self.x,self.y,self.z)
        self.a = int(float(out[0]))+90
        self.b = int(float(out[1]))+90
        self.c = int(float(out[2]))+90
        
        #use pyserial to send a b c on port /dev/ttyACM0
        
        
        
        
    def ard_update(self):
        msg=self.digit_len(self.a)+','+self.digit_len(self.b)+','+self.digit_len(self.c)+'\n'
        self.ser.write(msg.encode())
        print(self.a,self.b,self.c)
        
        
    def IK(self,xv,yv,zv):
        self.x_elem.clear()
        self.y_elem.clear()
        self.z_elem.clear()
        self.x_elem.send_keys(xv)
        self.y_elem.send_keys(yv)
        self.z_elem.send_keys(zv)
        ls=[]
        ls.append(self.t1.get_attribute("value"))
        ls.append(self.t2.get_attribute("value"))
        ls.append(self.t3.get_attribute("value"))
        return ls 




    # def timer_callback1(self):
    #     msg = Int16()
    #     msg.data = self.a
    #     self.publisher1_.publish(msg)
    #     msg.data = self.b
    #     self.publisher2_.publish(msg)
    #     msg.data = self.c
    #     self.publisher3_.publish(msg)
    #     self.get_logger().info('Publishing: "%d"' % msg.data)
    #     self.i += 1


    def listener_callback(self, msg):
        if(msg.linear.x>0):
            self.x+=15
        elif(msg.linear.x<0):
            self.x-=15
        if(msg.angular.z>0):
            self.y+=15
        elif(msg.angular.z<0):
            self.y-=15
        out = self.IK(self.x,self.y,self.z)
        self.a = int(float(out[0]))+90
        self.b = int(float(out[1]))+90
        self.c = int(float(out[2]))+90
        msg=self.digit_len(self.a)+','+self.digit_len(self.b)+','+self.digit_len(self.c)+'\n'
        self.ser.write(msg.encode())
        print(self.a,self.b,self.c)

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
