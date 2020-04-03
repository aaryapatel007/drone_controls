# drone_controls
ROS package for using steering angle and collision probability predicted via pre-trained ResNet model for drone navigation from one point to another using ROS Kinetic in Gazebo 3D environment.

## Introduction

The bridge between the drone_controls Keras code and the AR.Drone control is implemented in ROS. Taken inspiration from this [repo](https://github.com/uzh-rpg/rpg_public_dronet).

## Installation and Setup

### Step 1: Install ROS

It is necessary for you to install [ROS](http://wiki.ros.org/ROS/Installation) to have the basic tools available. The project was tested under ROS [kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu), but you can use any other version without problems.

### Step 2: Build your workspace

The folder containing all the related code for a project is usually defined as `workspace'.
Create your own workspace following [these instructions](http://wiki.ros.org/catkin/Tutorials/create_a_workspace) and call it ```sim_ws```.

### Step 3: Setup AR.Drone Autonomy

In this step, we will bridge our ROS workspace with the bebop drone.
To do it, just follow [these instructions](https://github.com/AutonomyLab/ardrone_autonomy).

___Be sure to read properly all the instructions about how to run the driver, how to send commands and how to read data from the drone available on the website!___

### Step 4: Some tests

To make sure that everything is as expected, try to run some tests. Example:

1) See if you can connect to the drone

* Open the terminal and run ```drone.bash```.

2) See if you can receive images from it with [rqt_img_view](http://wiki.ros.org/rqt_image_view)

3) See if you can publish control commands [through the terminal](http://bebop-autonomy.readthedocs.io/en/latest/piloting.html)

4) Try to run the DroNet network:

* Open the terminal and run `run_dronet.sh`.
