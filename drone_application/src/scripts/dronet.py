#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError
from keras.models import model_from_json
from ardrone_autonomy.msg import Navdata
from drone_application.msg import Dronet_out
import numpy as np
import controls

class dronet():
    def __init__(self):

        self.rate = rospy.Rate(15)
        self.sub_front_cam = rospy.Subscriber("/camera/left/image_raw",Image,self.callback_fun_front_cam)

        self.model_input_size = (320,240)
        self.front_image = np.zeros((200,200,1))
        self.dronet_pub = rospy.Publisher("dronet_pred",Dronet_out,queue_size = 10)
    def callback_fun_front_cam(self,msg):
        try:
            bridge = CvBridge()
            image = bridge.imgmsg_to_cv2(msg,"bgr8")
            image = cv2.resize(image,self.model_input_size)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = self.central_image_crop(image)
            image = np.expand_dims(image,axis = 0)
            image = image*np.float32(1.0/255.0)
            self.front_image = image
        except CvBridgeError as e:
            print(e)
    def load_model(self,model_struct_path = "dronet/model_struct.json", model_weights_path="dronet/best_weights.h5"):
        if model_struct_path:
            model_file = open(model_struct_path)
        model_string = model_file.read()
        model = model_from_json(model_string)
        model.load_weights(model_weights_path)
        model.compile(loss = 'mse',optimizer = 'sgd')
        self.model = model
    def central_image_crop(self,img, crop_width = 200, crop_heigth=200):
        half_the_width = img.shape[1] / 2
        img = img[(img.shape[0] - crop_heigth): img.shape[0],
            (half_the_width - (crop_width / 2)): (half_the_width + (crop_width / 2))]
        img = img.reshape(img.shape[0], img.shape[1], 1)
        return img
    def eval_model(self):
        while not rospy.is_shutdown():
            model_input = self.front_image
            #model_input = np.expand_dims(model_input,axis = 0)
            outs = self.model.predict_on_batch(model_input)
            #print(outs)
            collision_prob = outs[1][0]
            #print("this is ",collision_prob[0])
            steering_ang = outs[0][0]
            msg = Dronet_out()
            msg.steering_ang = steering_ang[0]
            msg.collision_prob = collision_prob[0]
            self.dronet_pub.publish(msg)
            '''v_new = np.abs(self.smooth_forward_velocity(collision_prob))
            yaw_new = self.smooth_yaw(steering_ang)
            controls.set_velocity(linear_x = v_new , angular_z= yaw_new)
            #else:
             #   controls.set_velocity(angular_z = yaw_new)
            
            print("new forward velocity : ",v_new ,  " collision prob : " ,collision_prob )
            self.rate.sleep()'''
if __name__ == "__main__":
    rospy.init_node("dronet_node",anonymous = True)
    d = dronet()
    d.load_model()
    d.eval_model()