#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
#from ardrone_autonomy.msg import Navdata
from drone_application.msg import Dronet_out

class auto:
    def __init__(self):
        self.steering_ang = 0
        self.collision_prob = 0
        self.vmax = 1
        self.alpha = 0.7
        self.beta = 0.5
        self.vx = self.vmax
	self.az = 0
        self.rate = rospy.Rate(15)
        self.dronet_sub = rospy.Subscriber("/dronet_pred",Dronet_out,self.pred_callback)
        self.navdata_sub = rospy.Subscriber("drone/gt_vel",Twist,self.nav_callback)
        self.vel_pub = rospy.Publisher("/drone/cmd_val",Twist,queue_size=10)
    def pred_callback(self,msg):
        self.steering_ang = msg.steering_ang
        self.collision_prob = msg.collision_prob
    def nav_callback(self,msg):
        self.vx = msg.linear.x
        self.az = msg.angular.z
    def smooth_forward_velocity(self):
        v_new = (1-self.alpha)*self.vx + self.alpha*(1-self.collision_prob)*self.vmax
        return v_new
    def smooth_yaw(self):
        yaw_new = (1-self.beta)*self.az*0.0175433 + self.beta*self.steering_ang*1.5708
        return yaw_new
    def set_velocity(self,linear_x =0 ,linear_y = 0,linear_z = 0,angular_x = 0,angular_y = 0,angular_z = 0):
        vel_msg = Twist()
        vel_msg.linear.x = linear_x
        vel_msg.linear.y = linear_y
        vel_msg.linear.z = linear_z
        vel_msg.angular.x = angular_x
        vel_msg.angular.y = angular_y
        vel_msg.angular.z = angular_z
        self.vel_pub.publish(vel_msg)

    def eval_func(self):
        while not rospy.is_shutdown():
            x = (1-self.collision_prob)*self.vmax
            if(x <= 0):
                x = 0
            v_new = self.smooth_forward_velocity()
            #if(v_new < ((1 - self.collision_prob) * self.vmax)):
            #    v_new = 0
            yaw_new = self.smooth_yaw()
            print(v_new,yaw_new)
            self.set_velocity(linear_x=v_new,angular_z=yaw_new)
            self.rate.sleep()
if __name__ == "__main__":
    rospy.init_node("auto_node",anonymous = True)
    a = auto()
    a.eval_func()
            
        

    
