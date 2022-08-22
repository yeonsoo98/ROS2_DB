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

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan 

import pymysql 

# DB config
HOST = 'localhost'
USER = 'root'
PASSWORD = 'mynewpassword'
DB = 'study_db'

class DBSubscriber(Node):

    def __init__(self):
        # db connection
        self.db_connection()

        # ros init
        super().__init__('db_subscriber')
        self.cmd_vel_subscription = self.create_subscription(
            Twist,
            'robot_namespace_0/cmd_vel',
            self.cmd_vel_callback,
            10)
        self.cmd_vel_subscription  # prevent unused variable warning

        self.front_laser_subscription = self.create_subscription(
            LaserScan,
            'robot_namespace_0/scan',
            self.scan_callback,
            10)
        self.front_laser_subscription

    def db_connection(self):
        """
        @brief  DB연결관련 함수
        """
        self.con = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        self.cur = self.con.cursor()

    def cmd_vel_callback(self, msg):
        """
        @brief  속도 토픽 콜백
        """
        self.get_logger().info('linear x: "%s"' % msg.linear.x)
        self.get_logger().info('linear y: "%s"' % msg.linear.y)
        self.get_logger().info('angular x: "%s"' % msg.angular.z)

    def scan_callback(self, msg):
        if msg.ranges[180] < 1.0 :
            self.get_logger().warn('front :"%f"' % msg.ranges[180])
            sql = "INSERT INTO robot (robot_namespace_id, speed) VALUES (%s, %s)"
            with self.con:
                with self.con.cursor() as self.cur:
                    self.cur.execute(sql, ('5', '7.1'))
                    self.con.commit()

    # info warn error fatal <log type>  
def main(args=None):
    rclpy.init(args=args)

    db_subscriber = DBSubscriber()

    rclpy.spin(db_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    db_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
# first