#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
def takeoff(): 
	pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10 )
	rospy.loginfo("TAKING OFF")
	pub.publish(Empty()) 
def land():
	pub = rospy.Publisher("ardrone/land", Empty, queue_size=10 )
	rospy.loginfo("LANDING")
	pub.publish(Empty())
def auto_hover():
	pub = rospy.Publisher("/cmd_vel",Twist,queue_size=10)
	vel_msg = Twist()
	vel_msg.linear.x = 0
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0
	pub.publish(vel_msg)
def set_velocity(linear_x,linear_y,linear_z,angular_x,angular_y,angular_z):
	pub = rospy.Publisher("/cmd_vel",Twist,queue_size=10)
	vel_msg = Twist()
	vel_msg.linear.x = linear_x
	vel_msg.linear.y = linear_y
	vel_msg.linear.z = linear_z
	vel_msg.angular.x = angular_x
	vel_msg.angular.y = angular_y
	vel_msg.angular.z = angular_z
	pub.publish(vel_msg)

#rospy.init_node('takeoff', anonymous=True)
#takeoff()
#land()
