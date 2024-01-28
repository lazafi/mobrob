#! /usr/bin/env python3

import rospy
import actionlib
import time

import tello.msg
from action import ActionServer

from djitellopy import Tello

class YActionServer(ActionServer):
   

    def __init__(self, name, drone):
        #start action server
        self._feedback = tello.msg.YFeedback()
        self._result = tello.msg.YResult()
        super().__init__(name,drone, tello.msg.YAction)
 


    def execute_cb(self, goal):
        rospy.loginfo('%s %i' % (self._action_name, goal.distance))
        self._feedback.progress = []
        self._feedback.progress.append(True)        
        
        if (20 <= goal.distance <= 500):
            self.command('right %d' % goal.distance)
        elif (-20 >= goal.distance >= -500):
            self.command('left %d' % abs(goal.distance))
        else:
            rospy.loginfo("distance out of range: %d", goal.distance)
            self.success_cb(False)
                
    def success_cb(self, success):
        self._result.success = success
        self._as.set_succeeded(self._result)
        rospy.loginfo('end: %s %s' % (self._action_name, success))

    def feedback_cb(self):
        print('.', end =" ")
        self._feedback.progress.append(True)
        self._as.publish_feedback(self._feedback)    


if __name__ == '__main__':
    rospy.init_node('y')
    drone = Tello()
    drone.connect()
    print("launching server:", rospy.get_name())
    server = YActionServer(rospy.get_name(), drone)
    rospy.spin()
