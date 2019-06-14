import rospy
from geometry_msgs.msg import Twist

class Velocity:
    def set_velocity(self,linear_x,linear_y,linear_z,angular_x,angular_y,angular_z):
        self.vel_msg.linear.x = linear_x
        self.vel_msg.linear.y = linear_y
        self.vel_msg.linear.z = linear_z
        self.vel_msg.angular.x = angular_x
        self.vel_msg.angular.y = angular_y
        self.vel_msg.angular.z = angular_z
    def __init__(self):
        self.pub = rospy.Publisher("/cmd_vel",Twist,queue_size=10)
        self.rate = rospy.Rate(10)
        self.vel_msg = Twist()
        #self.__set_velocity(0,0,0,0,0,0)
        #self.__pub__()
    def start_motion(self):
        self.__pub__()
    def __pub__(self):
        while not rospy.is_shutdown():
            self.pub.publish(self.vel_msg)
            self.rate.sleep()


#if __name__ =="__main__":
#    rospy.init_node('velocity_test', anonymous=True)
#    v=Velocity()
#    v.set_velocity(6,0,0,0,0,0)
#    v.start_motion()
