#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import time

from action.launch_action_server import LaunchActionServer
from action.rotate_action_server import RotateActionServer
from action.x_action_server import XActionServer
from action.y_action_server import YActionServer
from action.z_action_server import ZActionServer
from action.move_action_server import MoveActionServer
from action.command_action_server import CommandActionServer
from sensor.battery_publisher import BatteryPublisher
from sensor.telemetry_sensor import TelemetrySensor
from sensor.image_sensor import ImageSensor
from server.keepalive_server import KeepaliveServer

from djitellopy import Tello, TelloException

    

def tello_node():
    # Initialize the ROS node
    rospy.init_node('tello', anonymous=True)
    rospy.loginfo("starting tello node")
    # init tello driver
    drone = Tello()
    connected = False
    # block till drone is connected
    while not connected:
        try:
           drone.connect()
        except TelloException as e:
           pass
        #rospy.loginfo('connected %s', drone.get_current_state())
        print(drone.get_current_state())
        if drone.get_current_state():
            connected = True
        time.sleep(1)

    rospy.loginfo("connected: %s %s", drone.query_sdk_version(), drone.query_active())

    # start sensor publishers
    tel = TelemetrySensor(drone)
    rospy.Timer(rospy.Duration(1), tel.publish)

    img = ImageSensor(drone)
    rospy.Timer(rospy.Duration(0.5), img.publish)


    # start action servers
    command = CommandActionServer('command', drone)
    launch = LaunchActionServer('launch', drone)
    rotate = RotateActionServer('rotate', drone)
    x = XActionServer('x', drone)
    y = YActionServer('y', drone)
    z = ZActionServer('z', drone)
    move = MoveActionServer('move', drone)



    # send keepalive messages
    keep = KeepaliveServer(drone)
    rospy.Timer(rospy.Duration(10.0), keep.keepalive)

    rospy.spin()
    
if __name__ == '__main__':
    try:
        tello_node()
    except rospy.ROSInterruptException:
        pass
