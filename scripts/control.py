#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

class StopNearWall:
    def __init__(self):
        # Khởi tạo node
        rospy.init_node('stop_near_wall', anonymous=True)

        # Ngưỡng khoảng cách đến tường (mét)
        self.distance_threshold = 0.2

        # Publisher để gửi lệnh điều khiển
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # Subscriber để đọc dữ liệu từ LIDAR
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)

        # Subscriber để đọc lệnh từ teleop_twist_keyboard
        self.teleop_sub = rospy.Subscriber('/cmd_vel', Twist, self.teleop_callback)

        # Lưu trữ lệnh teleop hiện tại
        self.current_cmd_vel = Twist()

    def laser_callback(self, data):
        # Lấy khoảng cách nhỏ nhất từ LIDAR
        min_distance = np.min([x for x in data.ranges if not np.isnan(x)])

        # Nếu khoảng cách nhỏ hơn ngưỡng
        if min_distance < self.distance_threshold:
            # Gửi lệnh dừng robot
            stop_cmd = Twist()
            stop_cmd.linear.x = 0.0
            stop_cmd.angular.z = 0.0
            self.cmd_vel_pub.publish(stop_cmd)
        else:
            # Chuyển tiếp lệnh từ teleop
            self.cmd_vel_pub.publish(self.current_cmd_vel)

    def teleop_callback(self, data):
        # Lưu trữ lệnh từ teleop_twist_keyboard
        self.current_cmd_vel = data

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        node = StopNearWall()
        node.run()
    except rospy.ROSInterruptException:
        pass