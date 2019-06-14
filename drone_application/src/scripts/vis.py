#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
import sensors
from sensors import front_camera_image
from cv_bridge import CvBridge,CvBridgeError

def vis_front_camera():
    rospy.Subscriber("/ardrone/front/image_raw",Image,callback_fun)
    rospy.spin()

def callback_fun(msg):
    try:
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(msg,"bgr8")
        cv2.imshow("front_camera",image)
        cv2.waitKey(3)
    except CvBridgeError as e:
		print(e)

if __name__ == "__main__":
    rospy.init_node("visualization",anonymous = True)
    vis_front_camera()
