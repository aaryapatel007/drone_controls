#!/usr/bin/env python
import rospy
import controls
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class KeyMappings():
    def __init__(self):
        self.TakeOff = QtCore.Qt.Key_Space
        self.Land = QtCore.Qt.Key_L
        self.PosX = QtCore.Qt.Key_E
        self.NegX = QtCore.Qt.Key_D
        self.PosY = QtCore.Qt.Key_F
        self.NegY = QtCore.Qt.Key_S
        self.PosZ = QtCore.Qt.Key_Q
        self.NegZ = QtCore.Qt.Key_A
        self.YawLeft = QtCore.Qt.Key_W
        self.YawRight = QtCore.Qt.Key_R
        self.AutoHover = QtCore.Qt.Key_H
        
class keyboard_input(QWidget):
    def __init__(self,parent = None):
        QWidget.__init__( self, parent )
        self.setGeometry(10,10,200,200)
        self.setWindowTitle( "Drone Keyboard Controller" )
        self.code_of_last_pressed_key  =  63
        self.setFocusPolicy( Qt.StrongFocus )
        self.KeyMaps = KeyMappings()
        self.velX = 0
        self.velY = 0
        self.velZ = 0
        self.yaw = 0
        self.minVel = -5
        self.maxVel = 5
        self.text = " Key : Action \n Space : Takeoff \n L : Land  \n H : Autohover \n E:+X \n D : -X \n Q: +Z \n A : -Z \n S:+Y \n F : -Y \n W: + Yaw \n R : - Yaw"
    def keyPressEvent( self, event ) :
        key = event.key()
        
        if key == self.KeyMaps.TakeOff:
            rospy.loginfo("SPACE PRESSED")
            controls.takeoff()
        elif key == self.KeyMaps.Land:
            rospy.loginfo("L PRESSED")
            controls.land()
        elif  key == self.KeyMaps.AutoHover:
            rospy.loginfo("SET TO AUTO HOVER")
            controls.auto_hover()
        else:
            if key == self.KeyMaps.PosX:
                self.velX = self.velX+1
            elif key == self.KeyMaps.NegX:
                self.velX += -1
            elif key == self.KeyMaps.PosY:
                self.velY += 1
            elif key == self.KeyMaps.NegY:
                self.velY += -1
            elif key == self.KeyMaps.PosZ:
                self.velZ += 1
            elif key == self.KeyMaps.NegZ:
                self.velZ += -1
            elif key == self.KeyMaps.YawLeft:
                self.yaw += 1
            elif key == self.KeyMaps.YawRight:
                self.yaw += -1
            controls.set_velocity(linear_x= self.velX , linear_y = self.velY , linear_z = self.velZ , angular_x = 0 , angular_y =0 , angular_z = self.yaw)    
        self.update()
    def keyReleaseEvent( self, event ) :
        key = event.key()

        if key == self.KeyMaps.PosX:
            self.velX = self.velX-1
        elif key == self.KeyMaps.NegX:
            self.velX += 1
        elif key == self.KeyMaps.PosY:
            self.velY += -1
        elif key == self.KeyMaps.NegY:
            self.velY += 1
        elif key == self.KeyMaps.PosZ:
            self.velZ += -1
        elif key == self.KeyMaps.NegZ:
            self.velZ += 1
        elif key == self.KeyMaps.YawLeft:
            self.yaw += -1
        elif key == self.KeyMaps.YawRight:
            self.yaw += 1
            controls.set_velocity(linear_x= self.velX , linear_y = self.velY , linear_z = self.velZ , angular_x = 0 , angular_y =0 , angular_z = self.yaw)    
        self.update()
        #print  "key release event"   #  This is Python 2.x statement.
        #print( "key release event" )  #  Python 3.x statement.
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
    def drawText(self,event,qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)


if __name__ == "__main__":

    rospy.init_node('drone_keyboard_gui' , log_level = rospy.DEBUG)
    rospy.loginfo("KEYBOARD GUI NODE CREATED")
    this_application = QApplication( sys.argv )
    app_win = keyboard_input()
    app_win.show()
    status = this_application.exec_()
    sys.exit(status)

