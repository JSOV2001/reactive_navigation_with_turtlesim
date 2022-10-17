#!/usr/bin/env python3
import rospy
import tf
from tf import transformations
from turtlesim.msg import Pose

class TurtleTransformBroadcaster:
    def __init__(self):
        self.turtle_name = "turtle1"
        self.pose_subscriber = rospy.Subscriber(f"/{self.turtle_name}/pose", Pose, self.pose_callback)
    
    def pose_callback(self, pose_message):
        translation = [pose_message.x, pose_message.y, 0]
        rotation_in_quaternions = transformations.quaternion_from_euler(0, 0, pose_message.theta)
        current_time = rospy.Time.now()

        tf_broadcaster = tf.TransformBroadcaster()
        child_frame = f"/{self.turtle_name}_frame"
        parent_frame = "/world"
        tf_broadcaster.sendTransform(translation, rotation_in_quaternions, current_time, child_frame, parent_frame)

if __name__ == "__main__":
    rospy.init_node("tf_broadcaster", anonymous= True)
    TurtleTransformBroadcaster()
    rospy.spin()