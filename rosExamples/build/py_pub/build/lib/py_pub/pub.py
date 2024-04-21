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

# from std_msgs.msg import String
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import pandas as pd




class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('delta')
        # self.x = 0
        # self.y = 0
        # self.z =-300
        # self.a = 0
        # self.b = 0
        # self.c = 0
        # self.model = Sequential()
        # self.model.add(Dense(64,activation='relu',input_shape=(3,)))
        # self.model.add(Dense(64,activation='relu'))
        # self.model.add(Dense(64,activation='relu'))
        # self.model.add(Dense(3))
        # self.model.compile(optimizer=Adam(),loss=MeanSquaredError())
        # self.model.load_weights('model.h5')
        # self.publisher1_ = self.create_publisher(int, 'servo1', 10)
        # self.publisher2_ = self.create_publisher(int, 'servo2', 10)
        # self.publisher3_ = self.create_publisher(int, 'servo3', 10)
        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0
        # self.subscription = self.create_subscription(
        #     String,
        #     '/turtle1/cmd_vel',
        #     self.listener_callback,
        #     10)
        # self.subscription
        self.get_logger().info('Publishing: ')
    # def timer_callback1(self):
    #     out = self.model.predict([[self.x,self.y,self.z]])
    #     self.a = int(out[0][0])
    #     self.b = int(out[0][1])
    #     self.c = int(out[0][2])
    #     msg = int()
    #     msg.data = a
    #     self.publisher1_.publish(msg)
    #     msg.data = b
    #     self.publisher2_.publish(msg)
    #     msg.data = c
    #     self.publisher3_.publish(msg)
    #     self.get_logger().info('Publishing: "%s"' % msg.data)
    #     self.i += 1

    # def timer_callback2(self):
    #     out = self.model.predict([[self.x,self.y,self.z]])
    #     self.a = int(out[0][0])
    #     self.b = int(out[0][1])
    #     self.c = int(out[0][2])
    #     msg = int()
    #     msg.data = a
    #     self.publisher1_.publish(msg)
    #     msg.data = b
    #     self.publisher2_.publish(msg)
    #     msg.data = c
    #     self.publisher3_.publish(msg)
    #     self.get_logger().info('Publishing: "%s"' % msg.data)
    #     self.i += 1

    # def timer_callback3(self):
    #     out = self.model.predict([[self.x,self.y,self.z]])
    #     self.a = int(out[0][0])
    #     self.b = int(out[0][1])
    #     self.c = int(out[0][2])
    #     msg = int()
    #     msg.data = a
    #     self.publisher1_.publish(msg)
    #     msg.data = b
    #     self.publisher2_.publish(msg)
    #     msg.data = c
    #     self.publisher3_.publish(msg)
    #     self.get_logger().info('Publishing: "%s"' % msg.data)
    #     self.i += 1

    # def listener_callback(self, msg):
    #     self.get_logger().info('I heard: "%s"' % msg.data)


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
