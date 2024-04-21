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

import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import serial
import time


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
        self.model = Sequential()
        self.model.add(Dense(64,activation='relu',input_shape=(3,)))
        self.model.add(Dense(64,activation='relu'))
        self.model.add(Dense(64,activation='relu'))
        self.model.add(Dense(3))
        self.model.compile(optimizer=Adam(),loss=MeanSquaredError())
        self.model.load_weights('model.h5')

        # self.publisher1_ = self.create_publisher(Int16, 'servo1', 10)
        # self.timer = self.create_timer(timer_period, self.timer_callback1)
        
        self.timer = self.create_timer(0.5, self.pos_timer)
        self.timer = self.create_timer(0.3, self.ard_update)
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
        out = self.model.predict([[self.x,self.y,self.z]])
        self.a = int(out[0][0])+90
        self.b = int(out[0][1])+90
        self.c = int(out[0][2])+90
        
        #use pyserial to send a b c on port /dev/ttyACM0
        
        
        
        
    def ard_update(self):
        msg='a'+self.digit_len(self.a)
        self.ser.write(msg.encode())
        
        msg='b'+self.digit_len(self.b)
        self.ser.write(msg.encode())
        
        msg='c'+self.digit_len(self.c)
        self.ser.write(msg.encode())
        

        print(self.a,self.b,self.c)
        
        
        




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
            self.x+=10
        elif(msg.linear.x<0):
            self.x-=10
        if(msg.angular.z>0):
            self.y+=10
        elif(msg.angular.z<0):
            self.y-=10

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
